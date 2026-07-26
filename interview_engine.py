"""
===========================================
Interview Engine
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
        print("=" * 70)
        print(f"STARTING LEVEL {current_level}")
        print("=" * 70)

        difficulty = LEVELS[current_level]["difficulty"]
        pass_score = LEVELS[current_level]["pass_score"]

        # ---------------------------------------
        # Generate Questions
        # ---------------------------------------

        questions = generate_questions(difficulty)

        # ---------------------------------------
        # Generate Reference Answers
        # ---------------------------------------

        reference_answers = generate_reference_answers(
            questions
        )

        # ---------------------------------------
        # Candidate Evaluation
        # ---------------------------------------

        average_score, candidate_answers, scores = evaluate_candidate(
            questions,
            reference_answers
        )

        # ---------------------------------------
        # Generate Report
        # ---------------------------------------

        generate_report(
            current_level,
            questions,
            reference_answers,
            candidate_answers,
            scores,
            average_score
        )

        # ---------------------------------------
        # PASS / FAIL
        # ---------------------------------------

        if average_score >= pass_score:

            print("\n")
            print("✅ LEVEL PASSED")

            if current_level == 3:

                print("\n")
                print("=" * 70)
                print("🎉 CONGRATULATIONS!")
                print("Candidate Completed All Interview Levels")
                print("=" * 70)

                break

            else:

                current_level += 1

                print(f"\nMoving to LEVEL {current_level}...")

        else:

            print("\n")
            print("❌ LEVEL FAILED")

            print(f"Repeating LEVEL {current_level}...\n")

    print("\n")
    print("=" * 70)
    print("Interview Session Finished")
    print("=" * 70)