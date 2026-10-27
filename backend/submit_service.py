"""
=========================================
Submit Interview Service
=========================================
Handles both text-based interviews (Level 1 & 3) 
and code-based interviews (Level 2)
"""

from evaluation_service import evaluate_answer
import json


def is_level2_submission(questions, candidate_answers):
    """
    Detect if this is a Level 2 (coding) submission.
    Level 2 has JSON object questions and code submission answers.
    """
    # Check if questions are objects (Level 2) or strings (Level 1/3)
    if len(questions) > 0:
        first_question = questions[0]
        # Level 2 questions are dict with 'title', 'description', 'test_cases'
        if isinstance(first_question, dict) and 'title' in first_question:
            return True
    
    # Also check if answers have code structure
    if len(candidate_answers) > 0:
        first_answer = candidate_answers[0]
        if isinstance(first_answer, dict) and 'code' in first_answer and 'language' in first_answer:
            return True
    
    return False


def evaluate_level2_coding(problems, code_submissions):
    """
    Evaluate Level 2 coding submissions based on test case results.
    
    Args:
        problems: List of coding problem dicts with test_cases
        code_submissions: List of submission dicts with code, language, result
    
    Returns:
        results list and overall score
    """
    results = []
    total_score = 0
    
    for i in range(len(problems)):
        problem = problems[i]
        submission = code_submissions[i]
        
        # Handle null/empty submissions
        if submission is None or not isinstance(submission, dict):
            results.append({
                "question": problem.get('title', f'Problem {i+1}'),
                "problem": problem,
                "candidate_answer": {
                    "code": "",
                    "language": "Not submitted",
                    "result": None
                },
                "evaluation": {
                    "correctness_score": 0,
                    "feedback": "No code was submitted for this problem.",
                    "strengths": "None",
                    "missing_points": "Problem was not attempted.",
                    "recommendation": "Submit code solution before finishing the interview.",
                    "test_results": {
                        "passed": 0,
                        "total": len(problem.get('test_cases', [])),
                        "pass_rate": 0
                    }
                }
            })
            continue
        
        # Extract test results from submission
        result = submission.get('result', {})
        
        # Calculate score based on test case pass rate
        if isinstance(result, dict) and 'test_results' in result:
            test_results = result['test_results']
            passed = test_results.get('passed', 0)
            total_tests = test_results.get('total', 0)
            
            if total_tests > 0:
                pass_rate = (passed / total_tests) * 100
                # Score: 10 points per problem, scaled by pass rate
                score = round((passed / total_tests) * 10, 2)
            else:
                pass_rate = 0
                score = 0
            
            # Generate feedback based on results
            if pass_rate == 100:
                feedback = "✅ Excellent! All test cases passed."
                strengths = f"Correct solution with {passed}/{total_tests} test cases passing."
                missing_points = "None"
                recommendation = "Great work! Consider optimizing for time/space complexity."
            elif pass_rate >= 60:
                feedback = f"⚠️ Partial solution. {passed}/{total_tests} test cases passed ({pass_rate:.0f}%)."
                strengths = f"Some test cases passed ({passed}/{total_tests})."
                missing_points = f"{total_tests - passed} test case(s) failing. Check edge cases and logic."
                recommendation = "Review failing test cases and fix the logic errors."
            else:
                feedback = f"❌ Solution needs work. Only {passed}/{total_tests} test cases passed ({pass_rate:.0f}%)."
                strengths = "Code was submitted and attempted."
                missing_points = f"Most test cases failing ({total_tests - passed}/{total_tests})."
                recommendation = "Reconsider the approach. Review problem requirements carefully."
            
            evaluation = {
                "correctness_score": score,
                "feedback": feedback,
                "strengths": strengths,
                "missing_points": missing_points,
                "recommendation": recommendation,
                "test_results": {
                    "passed": passed,
                    "total": total_tests,
                    "pass_rate": round(pass_rate, 2)
                },
                "execution_successful": result.get('success', False)
            }
            
            total_score += score
            
        else:
            # Execution failed or no result
            evaluation = {
                "correctness_score": 0,
                "feedback": "❌ Code execution failed or returned no results.",
                "strengths": "Code was submitted.",
                "missing_points": "Code did not execute successfully. Check for syntax errors or runtime issues.",
                "recommendation": "Fix execution errors and ensure code runs without errors.",
                "test_results": {
                    "passed": 0,
                    "total": len(problem.get('test_cases', [])),
                    "pass_rate": 0
                },
                "execution_successful": False,
                "error": result.get('error', 'Unknown error')
            }
        
        results.append({
            "question": problem.get('title', f'Problem {i+1}'),
            "problem": problem,
            "candidate_answer": {
                "code": submission.get('code', ''),
                "language": submission.get('language', 'unknown'),
                "result": result
            },
            "evaluation": evaluation
        })
    
    overall_score = round(total_score / len(problems), 2) if len(problems) > 0 else 0
    
    return results, overall_score


def submit_interview(questions, reference_answers, candidate_answers):
    """
    Submit interview and evaluate answers.
    
    Supports two modes:
    - Level 1 & 3: Text-based Q&A with LLM evaluation
    - Level 2: Coding problems with test case evaluation
    """
    
    # Detect submission type
    if is_level2_submission(questions, candidate_answers):
        print("🔵 Detected Level 2 (Coding) submission")
        results, overall_score = evaluate_level2_coding(questions, candidate_answers)
        return {
            "overall_score": overall_score,
            "results": results,
            "interview_type": "Level 2 - Coding"
        }
    
    # Level 1 & 3: Text-based evaluation (original logic)
    print("🔵 Detected Level 1/3 (Text-based) submission")
    
    results = []
    total_score = 0

    for i in range(len(questions)):

        # Get candidate answer
        answer = candidate_answers[i].strip() if isinstance(candidate_answers[i], str) else str(candidate_answers[i])

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

        # Evaluate answer with LLM
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

        "results": results,
        
        "interview_type": "Level 1/3 - Text-based"

    }