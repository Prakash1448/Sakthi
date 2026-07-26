"""
===========================================
Interview Report Module
===========================================
"""

from config import (
    CANDIDATE_NAME,
    DOMAIN
)


def generate_report(
    current_level,
    question_list,
    reference_answers,
    candidate_answers,
    scores,
    average_score
):

    print("\n")
    print("=" * 70)
    print(f"LEVEL {current_level} REPORT")
    print("=" * 70)

    for i in range(len(question_list)):

        print("=" * 70)

        print(f"Question {i+1}")
        print(question_list[i])

        print()

        print("Reference Answer:")
        print(reference_answers[i])

        print()

        print("Candidate Answer:")
        print(candidate_answers[i])

        print()

        print(f"Score : {scores[i]} /10")

        print("=" * 70)

    # -------------------------------
    # Result
    # -------------------------------

    if average_score >= 7:

        result = "PASS"

        if current_level == 3:
            recommendation = "Interview Completed Successfully"
        else:
            recommendation = f"Proceed to LEVEL {current_level+1}"

    else:

        result = "FAIL"
        recommendation = f"Repeat LEVEL {current_level}"

    # -------------------------------
    # Final Summary
    # -------------------------------

    print()
    print("=" * 70)
    print("AI INTERVIEW REPORT")
    print("=" * 70)

    print(f"Candidate Name : {CANDIDATE_NAME}")
    print(f"Domain         : {DOMAIN}")
    print(f"Current Level  : Level {current_level}")
    print(f"Questions      : {len(question_list)}")
    print(f"Average Score  : {average_score} /10")
    print(f"Result         : {result}")
    print(f"Recommendation : {recommendation}")

    print("=" * 70)