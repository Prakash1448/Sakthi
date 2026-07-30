"""
===========================================
Reference Answer Generation Module
AI Interview Platform
===========================================
"""

from groq_client import client

from config import (
    MODEL_NAME,
    ANSWER_TEMPERATURE,
    ANSWER_MAX_TOKENS
)


def generate_reference_answers(question_list):

    print("=" * 60)
    print("Generating Reference Answers...")
    print("=" * 60)

    reference_answers = []

    for i, question in enumerate(question_list, start=1):

        print(f"Generating Answer {i}/{len(question_list)}...")

        prompt = f"""
You are an experienced Technical Interviewer.

Generate the IDEAL interview answer.

Question:

{question}

Rules:

1. Answer should be technically correct.
2. Maximum 120 words.
3. Easy English.
4. Suitable for freshers.
5. Include a simple real-world example whenever possible.
6. Return ONLY the answer.
"""

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=ANSWER_TEMPERATURE,

            max_tokens=ANSWER_MAX_TOKENS

        )

        answer = response.choices[0].message.content.strip()

        reference_answers.append(answer)

    print()
    print("=" * 60)
    print("Reference Answers Generated Successfully")
    print("=" * 60)

    return reference_answers


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample_questions = [

        "What is an Array?",

        "Explain Stack.",

        "What is Queue?"

    ]

    answers = generate_reference_answers(sample_questions)

    print()

    for i in range(len(sample_questions)):

        print("=" * 60)

        print(f"Question {i+1}")

        print(sample_questions[i])

        print()

        print("Reference Answer")

        print(answers[i])

        print()