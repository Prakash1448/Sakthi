from config import (
    PASS_MARK,
    CANDIDATE_NAME,
    DOMAIN,
    LEVEL
)

def print_report(
        question_list,
        reference_answers,
        candidate_answers,
        scores
):

    print("\n")

    print("=" * 60)
    print("QUESTION WISE EVALUATION")
    print("=" * 60)

    for i in range(len(question_list)):

        print("=" * 60)

        print(f"Question {i+1}")

        print(question_list[i])

        print()

        print("Reference Answer")

        print(reference_answers[i])

        print()

        print("Candidate Answer")

        print(candidate_answers[i])

        print()

        print(f"Score : {scores[i]} /10")

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    print("\n")
    print("=" * 60)

    print("FINAL LEVEL SCORE")

    print(f"{average_score} /10")

    if average_score >= PASS_MARK:

        result = "PASS"

        recommendation = "Proceed to LEVEL 2"

    else:

        result = "FAIL"

        recommendation = "Repeat LEVEL 1"

    print(result)
    print(recommendation)

    print("\n")
    print("=" * 60)

    print("AI INTERVIEW REPORT")

    print("=" * 60)

    print(f"Candidate Name : {CANDIDATE_NAME}")

    print(f"Domain         : {DOMAIN}")

    print(f"Current Level  : {LEVEL}")

    print(f"Questions      : {len(question_list)}")

    print(f"Average Score  : {average_score} /10")

    print(f"Result         : {result}")

    print(f"Recommendation : {recommendation}")

    print("=" * 60)