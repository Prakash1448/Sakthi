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
    """
    Generate reference answers for questions.
    
    For Level 2 (coding problems), returns dummy references since
    evaluation is based on test cases, not reference comparison.
    
    For Level 1 & 3, generates LLM-based reference answers.
    """

    reference_answers = []

    print("=" * 60)
    print("Generating Reference Answers...")
    print("=" * 60)

    for question in question_list:
        
        # Check if this is a Level 2 coding problem (dict with 'title' key)
        if isinstance(question, dict) and 'title' in question:
            # For coding problems, store the problem itself as reference
            # Evaluation will use test_cases from the problem, not this reference
            reference_answers.append({
                "question": question.get('title', 'Coding Problem'),
                "reference_answer": f"This is a coding problem. Solution evaluated by test cases.",
                "is_coding_problem": True,
                "problem": question  # Store full problem for later use
            })
            continue

        # For text-based questions (Level 1 & 3)
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

            "reference_answer": answer,
            
            "is_coding_problem": False

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