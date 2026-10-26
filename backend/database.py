"""
MongoDB Database Service
Stores user interview sessions, answers, scores, and proctoring data
"""

from pymongo import MongoClient
from datetime import datetime
from typing import Optional, Dict, List
import os

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "ai_interview_platform"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
sessions_collection = db["sessions"]
answers_collection = db["answers"]
proctoring_collection = db["proctoring_events"]


# ============================================================================
# User Management
# ============================================================================

def create_or_get_user(username: str, domain: str = None) -> Dict:
    """
    Create or retrieve user from database.
    
    Args:
        username: Candidate name
        domain: Technical domain (Python, Java, etc.)
    
    Returns:
        User document with _id
    """
    user = users_collection.find_one({"username": username})
    
    if user:
        return user
    
    # Create new user
    user_doc = {
        "username": username,
        "domain": domain,
        "created_at": datetime.now(),
        "total_sessions": 0,
        "completed_levels": [],
        "average_score": 0.0
    }
    
    result = users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    return user_doc


def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user by username."""
    return users_collection.find_one({"username": username})


def update_user_stats(username: str, completed_level: str, session_score: float):
    """Update user statistics after completing a level."""
    user = users_collection.find_one({"username": username})
    
    if not user:
        return
    
    completed_levels = user.get("completed_levels", [])
    if completed_level not in completed_levels:
        completed_levels.append(completed_level)
    
    total_sessions = user.get("total_sessions", 0) + 1
    
    # Calculate new average score
    all_sessions = list(sessions_collection.find({"username": username}))
    total_score = sum(s.get("total_score", 0) for s in all_sessions)
    avg_score = total_score / len(all_sessions) if all_sessions else 0
    
    users_collection.update_one(
        {"username": username},
        {
            "$set": {
                "completed_levels": completed_levels,
                "total_sessions": total_sessions,
                "average_score": round(avg_score, 2),
                "updated_at": datetime.now()
            }
        }
    )


# ============================================================================
# Session Management
# ============================================================================

def create_session(
    username: str,
    domain: str,
    level: str,
    questions: List[str],
    reference_answers: List[str],
    proctoring_session_id: str = None
) -> str:
    """
    Create a new interview session.
    
    Returns:
        session_id (str)
    """
    session_doc = {
        "username": username,
        "domain": domain,
        "level": level,
        "questions": questions,
        "reference_answers": reference_answers,
        "candidate_answers": [],
        "evaluations": [],
        "total_score": 0.0,
        "percentage": 0.0,
        "status": "in_progress",
        "proctoring_session_id": proctoring_session_id,
        "proctoring_warnings": 0,
        "proctoring_violations": [],
        "started_at": datetime.now(),
        "completed_at": None
    }
    
    result = sessions_collection.insert_one(session_doc)
    return str(result.inserted_id)


def get_session(session_id: str) -> Optional[Dict]:
    """Get session by ID."""
    from bson import ObjectId
    try:
        return sessions_collection.find_one({"_id": ObjectId(session_id)})
    except:
        return None


def update_session_answer(
    session_id: str,
    question_index: int,
    question: str,
    candidate_answer: str,
    evaluation: Dict
):
    """
    Store answer and evaluation for a specific question.
    
    Args:
        session_id: Session ID
        question_index: Question number (0-indexed)
        question: The question text
        candidate_answer: User's answer
        evaluation: Evaluation result (score, feedback, etc.)
    """
    from bson import ObjectId
    
    # Store in answers collection for detailed tracking
    answer_doc = {
        "session_id": session_id,
        "username": sessions_collection.find_one({"_id": ObjectId(session_id)})["username"],
        "question_index": question_index,
        "question": question,
        "candidate_answer": candidate_answer,
        "evaluation": evaluation,
        "answered_at": datetime.now()
    }
    
    answers_collection.insert_one(answer_doc)
    
    # Update session with answer
    session = get_session(session_id)
    if not session:
        return
    
    candidate_answers = session.get("candidate_answers", [])
    evaluations = session.get("evaluations", [])
    
    # Ensure lists are long enough
    while len(candidate_answers) <= question_index:
        candidate_answers.append("")
    while len(evaluations) <= question_index:
        evaluations.append({})
    
    candidate_answers[question_index] = candidate_answer
    evaluations[question_index] = evaluation
    
    # Calculate total score
    total_score = sum(
        eval_data.get("score", 0) 
        for eval_data in evaluations 
        if eval_data
    )
    
    percentage = (total_score / len(session["questions"]) * 100) if session["questions"] else 0
    
    sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {
            "$set": {
                "candidate_answers": candidate_answers,
                "evaluations": evaluations,
                "total_score": round(total_score, 2),
                "percentage": round(percentage, 2),
                "updated_at": datetime.now()
            }
        }
    )


def complete_session(session_id: str, proctoring_data: Dict = None):
    """
    Mark session as completed and update statistics.
    
    Args:
        session_id: Session ID
        proctoring_data: Final proctoring statistics
    """
    from bson import ObjectId
    
    session = get_session(session_id)
    if not session:
        return
    
    update_data = {
        "status": "completed",
        "completed_at": datetime.now()
    }
    
    if proctoring_data:
        update_data.update({
            "proctoring_warnings": proctoring_data.get("warning_count", 0),
            "proctoring_violations": proctoring_data.get("violations", []),
            "proctoring_status": proctoring_data.get("status", "normal")
        })
    
    sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )
    
    # Update user statistics
    update_user_stats(
        session["username"],
        session["level"],
        session.get("total_score", 0)
    )


def get_user_sessions(username: str) -> List[Dict]:
    """Get all sessions for a user."""
    return list(sessions_collection.find({"username": username}).sort("started_at", -1))


def get_user_level_sessions(username: str, level: str) -> List[Dict]:
    """Get all sessions for a specific level."""
    return list(sessions_collection.find({
        "username": username,
        "level": level
    }).sort("started_at", -1))


# ============================================================================
# Proctoring Events
# ============================================================================

def store_proctoring_event(
    session_id: str,
    proctoring_session_id: str,
    event_type: str,
    details: Dict
):
    """
    Store proctoring violation event.
    
    Args:
        session_id: Interview session ID
        proctoring_session_id: Proctoring session ID
        event_type: "warning", "tab_switch", "violation", etc.
        details: Event details (violation_type, confidence, etc.)
    """
    event_doc = {
        "session_id": session_id,
        "proctoring_session_id": proctoring_session_id,
        "event_type": event_type,
        "details": details,
        "timestamp": datetime.now()
    }
    
    proctoring_collection.insert_one(event_doc)


def get_session_proctoring_events(session_id: str) -> List[Dict]:
    """Get all proctoring events for a session."""
    return list(proctoring_collection.find({"session_id": session_id}).sort("timestamp", 1))


# ============================================================================
# Report Data
# ============================================================================

def get_user_report_data(username: str) -> Dict:
    """
    Get comprehensive report data for a user across all levels.
    
    Returns:
        Complete user data including all sessions, scores, proctoring data
    """
    user = get_user_by_username(username)
    if not user:
        return None
    
    sessions = get_user_sessions(username)
    
    # Group sessions by level
    level_data = {}
    for session in sessions:
        level = session["level"]
        if level not in level_data:
            level_data[level] = []
        level_data[level].append(session)
    
    # Calculate statistics
    total_questions = sum(len(s.get("questions", [])) for s in sessions)
    total_answered = sum(len([a for a in s.get("candidate_answers", []) if a]) for s in sessions)
    total_score = sum(s.get("total_score", 0) for s in sessions)
    total_warnings = sum(s.get("proctoring_warnings", 0) for s in sessions)
    
    return {
        "user": user,
        "sessions": sessions,
        "level_data": level_data,
        "statistics": {
            "total_sessions": len(sessions),
            "total_questions": total_questions,
            "total_answered": total_answered,
            "average_score": round(total_score / len(sessions), 2) if sessions else 0,
            "total_warnings": total_warnings,
            "completion_rate": round((total_answered / total_questions * 100), 2) if total_questions > 0 else 0
        }
    }


def get_level_report_data(username: str, level: str) -> Dict:
    """
    Get report data for a specific level (even if incomplete).
    
    Returns:
        Level session data for report generation
    """
    sessions = get_user_level_sessions(username, level)
    
    if not sessions:
        return None
    
    # Get the most recent session for this level
    latest_session = sessions[0]
    
    return {
        "username": username,
        "level": level,
        "session": latest_session,
        "all_level_sessions": sessions,
        "proctoring_events": get_session_proctoring_events(str(latest_session["_id"]))
    }


# ============================================================================
# Database Health Check
# ============================================================================

def check_connection() -> bool:
    """Check if MongoDB connection is working."""
    try:
        client.server_info()
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False


# ============================================================================
# Testing
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("MongoDB Database Service Test")
    print("="*60)
    
    # Check connection
    if check_connection():
        print("✅ MongoDB connected successfully")
        print(f"   Database: {DB_NAME}")
        print(f"   Collections: {db.list_collection_names()}")
    else:
        print("❌ MongoDB connection failed")
    
    # Test user creation
    user = create_or_get_user("Test User", "Python")
    print(f"\n✅ User created/retrieved: {user['username']}")
    
    # Test session creation
    session_id = create_session(
        username="Test User",
        domain="Python",
        level="Level 1 - Basic Fundamentals",
        questions=["Q1", "Q2"],
        reference_answers=["A1", "A2"]
    )
    print(f"✅ Session created: {session_id}")
    
    print("\n✓ Database service test complete")
