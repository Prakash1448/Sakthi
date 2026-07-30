"""
=========================================
Evaluation Service
=========================================
"""

from groq_client import client

from config import (
    MODEL_NAME,
    ANSWER_TEMPERATURE,
    ANSWER_MAX_TOKENS
)


def evaluate_answer(question, reference_answer, candidate_answer):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate answer.

Question:
{question}

Reference Answer:
{reference_answer}

Candidate Answer:
{candidate_answer}

Evaluate carefully.

Return ONLY this JSON.

{{
    "correctness_score": 0-100,
    "feedback": "",
    "strengths": "",
    "missing_points": "",
    "recommendation": ""
}}

Do not return markdown.
Do not return explanation.
Return valid JSON only.
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=500

    )

    return response.choices[0].message.content.strip()