from fastapi import APIRouter
from pydantic import BaseModel
from interview_service import start_interview
import json

from question_generation import generate_questions
from reference_generation import generate_reference_answers
from evaluation_service import evaluate_answer

router = APIRouter()


# -------------------------
# Request Models
# -------------------------

class QuestionRequest(BaseModel):
    difficulty: str


class ReferenceRequest(BaseModel):
    questions: list[str]

class InterviewRequest(BaseModel):
    difficulty: str
class EvaluationRequest(BaseModel):

    question: str

    reference_answer: str

    candidate_answer: str
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

    interview = start_interview(request.difficulty)

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