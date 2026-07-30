"""
=========================================
Reference Answer Generator
=========================================
"""

from groq_client import client

from config import (
    MODEL_NAME,
    ANSWER_TEMPERATURE,
    ANSWER_MAX_TOKENS
)


def generate_reference_answers(question_list):

    reference_answers = []

    print("=" * 60)
    print("Generating Reference Answers...")
    print("=" * 60)

    for question in question_list:

        prompt = f"""
You are an expert technical interviewer.

Question:
{question}

Generate one ideal interview answer.

Rules:

1. Correct answer only.
2. Simple English.
3. Beginner Friendly.
4. Around 120-180 words.
5. No markdown.
6. No numbering.
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

        reference_answers.append({

            "question": question,

            "reference_answer": answer

        })

    print()

    print("Reference Answers Generated Successfully")

    print()

    return reference_answers


# -----------------------------
# Testing
# -----------------------------

if __name__ == "__main__":

    sample_questions = [

        "What is Array?",

        "Explain Stack."

    ]

    answers = generate_reference_answers(sample_questions)

    for item in answers:

        print("=" * 50)

        print(item["question"])

        print()

        print(item["reference_answer"])