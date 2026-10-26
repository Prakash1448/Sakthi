"""
===========================================
Configuration File
AI Interview Platform
===========================================
"""

# ==========================================================
# Candidate Information
# ==========================================================

CANDIDATE_NAME = "Demo Candidate"

# ==========================================================
# Interview Domain
# ==========================================================

# Available domains - 15 comprehensive options
AVAILABLE_DOMAINS = [
    "Python Programming",
    "Data Structures & Algorithms (DSA)",
    "Machine Learning & AI",
    "Web Development - Frontend",
    "Web Development - Backend",
    "Full Stack Development",
    "React.js & Modern Frontend",
    "Node.js & Express",
    "Database & SQL",
    "Cloud Computing (AWS/Azure/GCP)",
    "DevOps & CI/CD",
    "Data Science & Analytics",
    "Cybersecurity",
    "Mobile App Development",
    "RAG (Retrieval Augmented Generation) & LLM Applications"
]

DOMAIN = "Python Programming"  # Default domain

# ==========================================================
# Groq Model
# ==========================================================

# Recommended Models (Free Tier Available):
# "openai/gpt-oss-20b" - Fast, free tier available
# "openai/gpt-oss-120b" - Slower but more capable
# "llama-3.3-70b-versatile" - Enterprise only
# "llama-3.1-8b-instant" - Enterprise only (no longer free)

MODEL_NAME = "openai/gpt-oss-20b"

# ==========================================================
# Interview Levels
# ==========================================================

LEVELS = {

    1: {

        "difficulty": "Fundamentals",

        "pass_score": 7.0

    },

    2: {

        "difficulty": "Application",

        "pass_score": 7.0

    },

    3: {

        "difficulty": "Problem Solving",

        "pass_score": 7.0

    }

}

# ==========================================================
# Question Generation
# ==========================================================

QUESTION_TEMPERATURE = 0.7

QUESTION_MAX_TOKENS = 600

# ==========================================================
# Reference Answer Generation
# ==========================================================

ANSWER_TEMPERATURE = 0.5

ANSWER_MAX_TOKENS = 500

# ==========================================================
# Evaluation
# ==========================================================

EVALUATION_TEMPERATURE = 0.0

EVALUATION_MAX_TOKENS = 300

# ==========================================================
# Global Pass Mark
# ==========================================================

PASS_MARK = 7.0