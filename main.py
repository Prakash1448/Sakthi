from question_generation import generate_questions
from reference_generation import generate_reference_answers
from evaluation import evaluate
from report import print_report


def main():

    print("=" * 60)
    print("AI INTERVIEW PLATFORM")
    print("=" * 60)

    # -----------------------------------------------------
    # STEP 1 : Generate Questions
    # -----------------------------------------------------

    question_list = generate_questions()

    print("\nGenerated Questions\n")

    for i, question in enumerate(question_list):

        print(f"{i+1}. {question}")

    # -----------------------------------------------------
    # STEP 2 : Generate Reference Answers
    # -----------------------------------------------------

    reference_answers = generate_reference_answers(
        question_list
    )

    # -----------------------------------------------------
    # STEP 3 : Candidate Interview
    # -----------------------------------------------------

    candidate_answers = []

    print("\n")
    print("=" * 60)
    print("START INTERVIEW")
    print("=" * 60)

    for i, question in enumerate(question_list):

        print("\n")

        print("=" * 60)

        print(f"Question {i+1}")

        print(question)

        print("=" * 60)

        answer = input("Candidate Answer : ")

        candidate_answers.append(answer)

    # -----------------------------------------------------
    # STEP 4 : Evaluate
    # -----------------------------------------------------

    scores = evaluate(
        reference_answers,
        candidate_answers
    )

    # -----------------------------------------------------
    # STEP 5 : Generate Report
    # -----------------------------------------------------

    print_report(
        question_list,
        reference_answers,
        candidate_answers,
        scores
    )


if __name__ == "__main__":
    main()