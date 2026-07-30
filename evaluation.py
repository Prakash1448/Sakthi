"""
===========================================
Evaluation Module
AI Interview Platform
===========================================
"""

from groq_client import client

from config import (
    MODEL_NAME,
    EVALUATION_TEMPERATURE,
    EVALUATION_MAX_TOKENS
)


def evaluate_candidate(question_list, reference_answers):

    print("=" * 60)
    print("Candidate Interview Started")
    print("=" * 60)

    candidate_answers = []

    scores = []

    for i, question in enumerate(question_list):

        print("\n")
        print("=" * 60)
        print(f"Question {i+1}")
        print("=" * 60)

        print(question)

        print()

        candidate_answer = input("Candidate Answer : ")

        candidate_answers.append(candidate_answer)

        prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate answer.

Question:
{question}

Reference Answer:
{reference_answers[i]}

Candidate Answer:
{candidate_answer}

Instructions:

Evaluate only based on technical correctness.

Scoring Guide:

10 = Perfect answer

8-9 = Very Good

6-7 = Good

4-5 = Average

0-3 = Poor

Return ONLY the numeric score.

Examples:

8

7.5

9

Do NOT explain.
Do NOT write sentences.
Return ONLY one number.
"""

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=EVALUATION_TEMPERATURE,

            max_tokens=EVALUATION_MAX_TOKENS

        )

        result = response.choices[0].message.content.strip()

        try:

            score = float(result)

        except:

            try:

                score = float(result.split()[0])

            except:

                score = 0.0

        scores.append(score)

        print()

        print(f"AI Score : {score}/10")

    average_score = round(sum(scores) / len(scores), 2)

    return average_score, candidate_answers, scores


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    questions = [

        "What is an Array?"

    ]

    reference_answers = [

        "An array is a linear data structure that stores elements in contiguous memory."

    ]

    average_score, candidate_answers, scores = evaluate_candidate(

        questions,

        reference_answers

    )

    print()

    print("Average Score :", average_score)