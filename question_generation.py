"""
===========================================
Question Generation Module
AI Interview Platform
===========================================
"""

from groq_client import client

from config import (
    DOMAIN,
    MODEL_NAME,
    QUESTION_TEMPERATURE,
    QUESTION_MAX_TOKENS
)


def generate_questions(difficulty):

    print("=" * 60)
    print("Generating Interview Questions...")
    print("=" * 60)

    prompt = f"""
You are an experienced Technical Interviewer.

Generate EXACTLY 10 interview questions.

Domain:
{DOMAIN}

Difficulty:
{difficulty}

Rules:

1. Return ONLY questions.
2. Number each question.
3. Do NOT generate answers.
4. Do NOT generate explanations.
5. Questions should be suitable for freshers.
6. Questions must be unique.
7. Questions should match the difficulty level.

Difficulty Meaning:

Fundamentals:
Definition, Basic Concepts, Examples

Application:
Implementation, Comparison, Use Cases

Problem Solving:
Scenario Based, Coding Logic, Design Thinking
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ],

        temperature=QUESTION_TEMPERATURE,

        max_tokens=QUESTION_MAX_TOKENS

    )

    generated_text = response.choices[0].message.content.strip()

    question_list = []

    for line in generated_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():

            question = line.split(".", 1)[1].strip()

            question_list.append(question)

    print()

    print("Questions Generated Successfully")

    print()

    return question_list


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    questions = generate_questions("Fundamentals")

    print("=" * 60)

    print("Generated Questions")

    print("=" * 60)

    for i, question in enumerate(questions, start=1):

        print(f"{i}. {question}")