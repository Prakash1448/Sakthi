"""
=========================================
Submit Interview Service
=========================================
"""

from evaluation_service import evaluate_answer
import json


def submit_interview(questions, reference_answers, candidate_answers):

    results = []

    total_score = 0

    for i in range(len(questions)):

        # Get candidate answer
        answer = candidate_answers[i].strip()

        # If no answer given
        if answer == "":

            results.append({

                "question": questions[i],

                "candidate_answer": "",

                "evaluation": {

                    "correctness_score": 0,

                    "feedback": "No answer was provided.",

                    "strengths": "None",

                    "missing_points": "Candidate did not answer the question.",

                    "recommendation": "Attempt the question before submitting."

                }

            })

            continue

        # Evaluate answer
        evaluation = evaluate_answer(

            questions[i],

            reference_answers[i]["reference_answer"],

            answer

        )

        try:

            evaluation = json.loads(evaluation)

        except:

            pass

        results.append({

            "question": questions[i],

            "candidate_answer": answer,

            "evaluation": evaluation

        })

        if isinstance(evaluation, dict):

            total_score += evaluation.get("correctness_score", 0)

    overall_score = round(total_score / len(questions), 2)

    return {

        "overall_score": overall_score,

        "results": results

    }