"""
===========================================
Interview Report Module
AI Interview Platform
===========================================
"""

from config import (
    PASS_MARK,
    CANDIDATE_NAME,
    DOMAIN
)


def generate_report(
    level,
    question_list,
    reference_answers,
    candidate_answers,
    scores,
    average_score
):

    print("\n")
    print("=" * 80)
    print(f"LEVEL {level} INTERVIEW REPORT")
    print("=" * 80)

    for i in range(len(question_list)):

        print("\n")
        print("-" * 80)

        print(f"Question {i+1}")

        print("-" * 80)

        print()

        print("Question")
        print(question_list[i])

        print()

        print("Reference Answer")
        print(reference_answers[i])

        print()

        print("Candidate Answer")
        print(candidate_answers[i])

        print()

        print(f"Score : {scores[i]}/10")

    print("\n")
    print("=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    print(f"Candidate Name : {CANDIDATE_NAME}")
    print(f"Domain         : {DOMAIN}")
    print(f"Current Level  : {level}")
    print(f"Questions      : {len(question_list)}")
    print(f"Average Score  : {average_score}/10")

    if average_score >= PASS_MARK:

        result = "PASS"

        if level == 1:

            recommendation = "Proceed to LEVEL 2"

        elif level == 2:

            recommendation = "Proceed to LEVEL 3"

        else:

            recommendation = "Interview Completed Successfully"

    else:

        result = "FAIL"

        recommendation = f"Repeat LEVEL {level}"

    print(f"Result         : {result}")
    print(f"Recommendation : {recommendation}")

    print("=" * 80)