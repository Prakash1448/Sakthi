"""
===========================================
Interview Engine
AI Interview Platform
===========================================
"""

from config import LEVELS

from question_generation import generate_questions
from reference_generation import generate_reference_answers
from evaluation import evaluate_candidate
from report import generate_report


def start_interview():

    current_level = 1

    while current_level <= 3:

        print("\n")
        print("=" * 80)
        print(f"STARTING LEVEL {current_level}")
        print("=" * 80)

        difficulty = LEVELS[current_level]["difficulty"]

        pass_score = LEVELS[current_level]["pass_score"]

        # =============================================
        # Question Generation
        # =============================================

        questions = generate_questions(difficulty)

        # =============================================
        # Reference Answer Generation
        # =============================================

        reference_answers = generate_reference_answers(
            questions
        )

        # =============================================
        # Candidate Evaluation
        # =============================================

        average_score, candidate_answers, scores = evaluate_candidate(

            questions,

            reference_answers

        )

        # =============================================
        # Generate Report
        # =============================================

        generate_report(

            level=current_level,

            question_list=questions,

            reference_answers=reference_answers,

            candidate_answers=candidate_answers,

            scores=scores,

            average_score=average_score

        )

        # =============================================
        # PASS / FAIL
        # =============================================

        if average_score >= pass_score:

            print("\n")

            print("✅ LEVEL PASSED")

            current_level += 1

            if current_level <= 3:

                print(f"\nMoving to LEVEL {current_level}...\n")

        else:

            print("\n")

            print("❌ LEVEL FAILED")

            print()

            print(f"Please repeat LEVEL {current_level}")

            print()

    print("\n")
    print("=" * 80)
    print("🎉 INTERVIEW COMPLETED SUCCESSFULLY")
    print("=" * 80)