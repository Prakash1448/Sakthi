from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from interview_service import start_interview
import json
from submit_service import submit_interview

from question_generation import generate_questions
from reference_generation import generate_reference_answers
from evaluation_service import evaluate_answer
from speech_to_text_service import transcribe_audio
from proctoring_service import (
    create_proctoring_session,
    process_monitoring_event,
    process_tab_switch_event,
    get_session_status,
    handle_camera_event,
    terminate_session
)

# MongoDB integration (optional - won't break if MongoDB not installed)
try:
    import database
    from pdf_report_generator import generate_user_report_pdf, generate_level_report_pdf
    from pdf_report_generator_enhanced import generate_enhanced_pdf_report
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠️  MongoDB not available. Install with: pip install pymongo reportlab pillow matplotlib")

router = APIRouter()


# -------------------------
# Request Models
# -------------------------

class QuestionRequest(BaseModel):
    difficulty: str
    domain: str = None  # Optional, defaults to config if not provided

class SubmitInterviewRequest(BaseModel):

    questions: list[str]

    reference_answers: list

    candidate_answers: list[str]
class ReferenceRequest(BaseModel):
    questions: list[str]

class InterviewRequest(BaseModel):
    difficulty: str
    domain: str = None  # Optional, defaults to config if not provided
    
class StartInterviewWithUserRequest(BaseModel):
    username: str
    domain: str
    level: str

class SaveAnswerRequest(BaseModel):
    session_id: str
    question_index: int
    question: str
    candidate_answer: str
    reference_answer: str

class CompleteSessionRequest(BaseModel):
    session_id: str
    proctoring_session_id: Optional[str] = None
class EvaluationRequest(BaseModel):

    question: str

    reference_answer: str

    candidate_answer: str

class MonitoringEventRequest(BaseModel):
    session_id: str
    face_detected: bool
    face_count: int
    violation_type: Optional[str] = None
    confidence: float
    timestamp: float
    event_id: Optional[str] = None

class TabSwitchRequest(BaseModel):
    session_id: str
    event_type: str  # "tab_switch" or "browser_minimize"
    event_id: str  # Prevents duplicate penalties
    timestamp: float

class CameraEventRequest(BaseModel):
    session_id: str
    event_type: str  # "disconnect" or "reconnect"
# -------------------------
# Health API
# -------------------------

@router.get("/health")
def health():
    return {
        "status": "Backend Running Successfully"
    }


# -------------------------
# Home API
# -------------------------

@router.get("/")
def home():
    return {
        "message": "AI Interview Platform API"
    }


# -------------------------
# Generate Questions API
# -------------------------

@router.post("/generate-questions")
def generate_questions_api(request: QuestionRequest):

    questions = generate_questions(request.difficulty)

    return {
        "difficulty": request.difficulty,
        "questions": questions
    }


# -------------------------
# Generate Reference Answers API
# -------------------------

@router.post("/generate-reference-answers")
def generate_reference_api(request: ReferenceRequest):

    reference_answers = generate_reference_answers(request.questions)

    return {
        "reference_answers": reference_answers
    }
@router.post("/start-interview")
def start_interview_api(request: InterviewRequest):

    interview = start_interview(request.difficulty, request.domain)

    return interview
# -----------------------------------------
# Evaluate Candidate Answer
# -----------------------------------------

@router.post("/evaluate-answer")
def evaluate_answer_api(request: EvaluationRequest):

    result = evaluate_answer(

        request.question,

        request.reference_answer,

        request.candidate_answer

    )

    try:

        result = json.loads(result)

    except:

        pass

    return {

        "evaluation": result

    }
    
    # -----------------------------------------
# Submit Interview
# -----------------------------------------

@router.post("/submit-interview")
def submit_interview_api(request: SubmitInterviewRequest):

    result = submit_interview(

        request.questions,

        request.reference_answers,

        request.candidate_answers

    )

    return result


# -----------------------------------------
# Speech-to-Text Transcription
# -----------------------------------------

@router.post("/transcribe-audio")
async def transcribe_audio_api(audio: UploadFile = File(...)):
    """
    Transcribe audio file to text using Groq Whisper API.
    
    Accepts: audio file (webm, wav, mp3, m4a, ogg, flac)
    Returns: transcribed text or error message
    """
    
    try:
        print("=== Transcribe Audio API Called ===")
        
        # Validate file exists
        if not audio:
            return {
                "success": False,
                "error": "No audio file provided"
            }
        
        print(f"Filename: {audio.filename}")
        print(f"Content type: {audio.content_type}")
        
        # Check file size (Groq has 25MB limit)
        content = await audio.read()
        file_size_bytes = len(content)
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        print(f"File size: {file_size_bytes} bytes ({file_size_mb:.3f} MB)")
        
        if file_size_mb > 25:
            return {
                "success": False,
                "error": f"Audio file too large ({file_size_mb:.1f}MB). Maximum is 25MB."
            }
        
        # VERY LENIENT size check - only 100 bytes minimum
        if file_size_bytes < 100:
            print(f"ERROR: File too small: {file_size_bytes} bytes")
            return {
                "success": False,
                "error": f"Audio file is empty or too small ({file_size_bytes} bytes). Please record for at least 1 second."
            }
        
        print("File size acceptable, proceeding to transcription...")
        
        # Create file-like object from bytes
        from io import BytesIO
        audio_file = BytesIO(content)
        
        # Transcribe using Groq Whisper
        print("Calling Groq Whisper API...")
        result = transcribe_audio(audio_file, audio.filename)
        
        print(f"Transcription result: {result.get('success')}")
        if result.get('success'):
            print(f"Transcribed text: {result.get('text')[:100]}...")
        else:
            print(f"Transcription error: {result.get('error')}")
        
        return result
        
    except Exception as e:
        print(f"Exception in transcribe_audio_api: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": f"Failed to process audio: {str(e)}"
        }


# -----------------------------------------
# Proctoring - Create Session
# -----------------------------------------

@router.post("/proctoring/create-session")
def create_proctoring_session_api():
    """
    Create a new proctoring session.
    Returns session ID to track monitoring state.
    """
    try:
        session_id = create_proctoring_session()
        return {
            "success": True,
            "session_id": session_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Proctoring - Process Monitoring Event
# -----------------------------------------

@router.post("/proctoring/process-event")
def process_monitoring_event_api(request: MonitoringEventRequest):
    """
    Process a monitoring event from the frontend.
    
    Accepts detection data and returns:
    - Warning status
    - Warning message if issued
    - Session status
    - Termination flag
    """
    try:
        detection_result = {
            "face_detected": request.face_detected,
            "face_count": request.face_count,
            "violation_type": request.violation_type,
            "confidence": request.confidence,
            "timestamp": request.timestamp,
            "event_id": request.event_id
        }
        
        result = process_monitoring_event(request.session_id, detection_result)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Proctoring - Process Tab Switch Event
# -----------------------------------------

@router.post("/proctoring/tab-switch")
def process_tab_switch_api(request: TabSwitchRequest):
    """
    Process browser tab switch or visibility change event.
    Applies immediate +3 warning penalty.
    """
    try:
        event_data = {
            "event_type": request.event_type,
            "event_id": request.event_id,
            "timestamp": request.timestamp
        }
        
        result = process_tab_switch_event(request.session_id, event_data)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Proctoring - Get Session Status
# -----------------------------------------

@router.get("/proctoring/session/{session_id}")
def get_proctoring_session_api(session_id: str):
    """
    Get current proctoring session status.
    """
    try:
        result = get_session_status(session_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Proctoring - Camera Event
# -----------------------------------------

@router.post("/proctoring/camera-event")
def handle_camera_event_api(request: CameraEventRequest):
    """
    Handle camera connection/disconnection events.
    """
    try:
        result = handle_camera_event(request.session_id, request.event_type)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Proctoring - Terminate Session
# -----------------------------------------

@router.post("/proctoring/terminate/{session_id}")
def terminate_proctoring_session_api(session_id: str, reason: str = "manual"):
    """
    Manually terminate a proctoring session.
    """
    try:
        result = terminate_session(session_id, reason)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ===========================================
# MongoDB Integration - New Endpoints
# ===========================================

@router.post("/interview/start-with-user")
def start_interview_with_user_api(request: StartInterviewWithUserRequest):
    """
    Start interview and create user + session in MongoDB.
    
    Returns session_id for tracking.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available. Install with: pip install pymongo reportlab pillow"
        }
    
    try:
        # Create or get user
        user = database.create_or_get_user(request.username, request.domain)
        
        # Generate questions
        questions = generate_questions(request.level, request.domain)
        reference_answers = generate_reference_answers(questions)
        
        # Create proctoring session
        proctoring_session_id = create_proctoring_session()
        
        # Create interview session in database
        session_id = database.create_session(
            username=request.username,
            domain=request.domain,
            level=request.level,
            questions=questions,
            reference_answers=reference_answers,
            proctoring_session_id=proctoring_session_id
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "proctoring_session_id": proctoring_session_id,
            "questions": questions,
            "reference_answers": reference_answers,
            "level": request.level,
            "domain": request.domain
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.post("/interview/save-answer")
async def save_answer_api(request: SaveAnswerRequest):
    """
    Save candidate answer and evaluation to database.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Evaluate answer
        evaluation_result = evaluate_answer(
            request.question,
            request.reference_answer,
            request.candidate_answer
        )
        
        # Parse evaluation if it's JSON string
        try:
            evaluation = json.loads(evaluation_result)
        except:
            evaluation = {"score": 0, "feedback": evaluation_result}
        
        # Save to database
        database.update_session_answer(
            session_id=request.session_id,
            question_index=request.question_index,
            question=request.question,
            candidate_answer=request.candidate_answer,
            evaluation=evaluation
        )
        
        # Store proctoring event if needed
        session = database.get_session(request.session_id)
        if session and session.get("proctoring_session_id"):
            database.store_proctoring_event(
                session_id=request.session_id,
                proctoring_session_id=session["proctoring_session_id"],
                event_type="answer_submitted",
                details={"question_index": request.question_index}
            )
        
        return {
            "success": True,
            "evaluation": evaluation,
            "session_id": request.session_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.post("/interview/complete")
def complete_interview_api(request: CompleteSessionRequest):
    """
    Mark interview as completed in database.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Get proctoring status
        proctoring_data = None
        if request.proctoring_session_id:
            proc_status = get_session_status(request.proctoring_session_id)
            if proc_status.get("success"):
                proctoring_data = {
                    "warning_count": proc_status.get("warning_count", 0),
                    "status": proc_status.get("monitoring_status", "normal"),
                    "violations": []
                }
        
        # Complete session
        database.complete_session(request.session_id, proctoring_data)
        
        # Get final session data
        session = database.get_session(request.session_id)
        
        return {
            "success": True,
            "session": {
                "total_score": session.get("total_score", 0),
                "percentage": session.get("percentage", 0),
                "proctoring_warnings": session.get("proctoring_warnings", 0),
                "status": session.get("status", "completed")
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/reports/user/{username}")
def get_user_report_api(username: str):
    """
    Get comprehensive user report data.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        report_data = database.get_user_report_data(username)
        
        if not report_data:
            return {
                "success": False,
                "error": "User not found"
            }
        
        return {
            "success": True,
            "data": report_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/reports/user/{username}/pdf")
def download_user_report_pdf_api(username: str):
    """
    Generate and download comprehensive PDF report for a user.
    Includes visual charts and graphs.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Get report data
        report_data = database.get_user_report_data(username)
        
        if not report_data:
            return {
                "success": False,
                "error": "User not found or no interview data"
            }
        
        # Generate enhanced PDF with charts
        pdf_path = generate_enhanced_pdf_report(report_data)
        
        # Return file for download
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{username}_interview_report.pdf"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": f"PDF generation failed: {str(e)}"
        }


@router.post("/interview/complete-and-generate-report")
def complete_and_generate_report_api(request: CompleteSessionRequest):
    """
    Complete interview session and automatically generate PDF report.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Complete the session first
        proctoring_data = None
        if request.proctoring_session_id:
            proc_status = get_session_status(request.proctoring_session_id)
            if proc_status.get("success"):
                proctoring_data = {
                    "warning_count": proc_status.get("warning_count", 0),
                    "status": proc_status.get("monitoring_status", "normal"),
                    "violations": []
                }
        
        database.complete_session(request.session_id, proctoring_data)
        
        # Get session to find username
        session = database.get_session(request.session_id)
        username = session.get("username")
        
        # Generate PDF report
        report_data = database.get_user_report_data(username)
        pdf_path = generate_enhanced_pdf_report(report_data)
        
        return {
            "success": True,
            "session": {
                "total_score": session.get("total_score", 0),
                "percentage": session.get("percentage", 0),
                "proctoring_warnings": session.get("proctoring_warnings", 0),
                "status": session.get("status", "completed")
            },
            "pdf_generated": True,
            "pdf_path": pdf_path,
            "download_url": f"/reports/user/{username}/pdf"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }
    """
    Generate and download comprehensive PDF report for user.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Get report data
        report_data = database.get_user_report_data(username)
        
        if not report_data:
            return {
                "success": False,
                "error": "User not found"
            }
        
        # Generate PDF
        pdf_path = generate_user_report_pdf(report_data)
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{username}_interview_report.pdf"
        )
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/reports/level/{username}/{level}")
def get_level_report_api(username: str, level: str):
    """
    Get report data for a specific level (even if incomplete).
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Replace underscores with spaces in level name
        level_name = level.replace("_", " ")
        
        report_data = database.get_level_report_data(username, level_name)
        
        if not report_data:
            return {
                "success": False,
                "error": "No sessions found for this level"
            }
        
        return {
            "success": True,
            "data": report_data
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/reports/level/{username}/{level}/pdf")
def download_level_report_pdf_api(username: str, level: str):
    """
    Generate and download PDF report for a specific level.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "error": "MongoDB not available"
        }
    
    try:
        # Replace underscores with spaces in level name
        level_name = level.replace("_", " ")
        
        # Get report data
        report_data = database.get_level_report_data(username, level_name)
        
        if not report_data:
            return {
                "success": False,
                "error": "No sessions found for this level"
            }
        
        # Generate PDF
        pdf_path = generate_level_report_pdf(report_data)
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{username}_{level}_report.pdf"
        )
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/database/health")
def database_health_api():
    """
    Check MongoDB connection status.
    """
    if not MONGODB_AVAILABLE:
        return {
            "success": False,
            "connected": False,
            "error": "MongoDB not installed. Install with: pip install pymongo"
        }
    
    try:
        connected = database.check_connection()
        return {
            "success": True,
            "connected": connected,
            "database": database.DB_NAME
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }