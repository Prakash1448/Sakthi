"""
=========================================
Interview Service
=========================================
"""

from question_generation import generate_questions
from reference_generation import generate_reference_answers


def start_interview(difficulty):

    questions = generate_questions(difficulty)

    reference_answers = generate_reference_answers(questions)

    return {

        "difficulty": difficulty,

        "questions": questions,

        "reference_answers": reference_answers

    }