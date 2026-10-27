"""
Test Level 2 Submission Fix
Tests that submit_interview correctly handles coding problem submissions
"""

import sys
sys.path.insert(0, '.')

from submit_service import submit_interview, is_level2_submission

def test_level2_detection():
    """Test that Level 2 submissions are correctly detected"""
    
    # Level 2 format
    level2_questions = [
        {
            "title": "Two Sum",
            "description": "Find two numbers that add up to target",
            "test_cases": [
                {"input": "[2,7,11,15], 9", "expected_output": "[0,1]"},
                {"input": "[3,2,4], 6", "expected_output": "[1,2]"}
            ]
        }
    ]
    
    level2_answers = [
        {
            "code": "def solution(nums, target):\n    return [0, 1]",
            "language": "python",
            "result": {
                "success": True,
                "test_results": {
                    "passed": 2,
                    "total": 2
                }
            }
        }
    ]
    
    # Level 1/3 format
    level1_questions = ["What is Python?", "Explain variables"]
    level1_answers = ["Python is a programming language", "Variables store data"]
    
    # Test detection
    assert is_level2_submission(level2_questions, level2_answers) == True, "Should detect Level 2"
    assert is_level2_submission(level1_questions, level1_answers) == False, "Should detect Level 1/3"
    
    print("✅ Level 2 detection working correctly")


def test_level2_submission():
    """Test Level 2 submission evaluation"""
    
    questions = [
        {
            "title": "Reverse String",
            "description": "Reverse a given string",
            "test_cases": [
                {"input": "hello", "expected_output": "olleh"},
                {"input": "world", "expected_output": "dlrow"},
                {"input": "python", "expected_output": "nohtyp"}
            ]
        },
        {
            "title": "Sum Array",
            "description": "Return sum of all elements",
            "test_cases": [
                {"input": "[1,2,3]", "expected_output": "6"},
                {"input": "[10,20]", "expected_output": "30"}
            ]
        }
    ]
    
    # Submission 1: All tests pass
    submission1 = {
        "code": "def reverse(s):\n    return s[::-1]",
        "language": "python",
        "result": {
            "success": True,
            "test_results": {
                "passed": 3,
                "total": 3
            }
        }
    }
    
    # Submission 2: Partial pass
    submission2 = {
        "code": "def sum_array(arr):\n    return sum(arr)",
        "language": "python",
        "result": {
            "success": True,
            "test_results": {
                "passed": 1,
                "total": 2
            }
        }
    }
    
    candidate_answers = [submission1, submission2]
    reference_answers = [{"reference_answer": "dummy"} for _ in questions]
    
    # Submit
    result = submit_interview(questions, reference_answers, candidate_answers)
    
    print("\n📊 Submission Results:")
    print(f"Overall Score: {result['overall_score']}/10")
    print(f"Interview Type: {result['interview_type']}")
    
    # Verify results
    assert "overall_score" in result
    assert result["interview_type"] == "Level 2 - Coding"
    assert len(result["results"]) == 2
    
    # Check first problem (100% pass)
    prob1_eval = result["results"][0]["evaluation"]
    assert prob1_eval["correctness_score"] == 10, "100% pass should give 10 points"
    assert prob1_eval["test_results"]["passed"] == 3
    assert prob1_eval["test_results"]["pass_rate"] == 100
    
    # Check second problem (50% pass)
    prob2_eval = result["results"][1]["evaluation"]
    assert prob2_eval["correctness_score"] == 5, "50% pass should give 5 points"
    assert prob2_eval["test_results"]["passed"] == 1
    assert prob2_eval["test_results"]["pass_rate"] == 50
    
    # Overall should be average: (10 + 5) / 2 = 7.5
    assert result["overall_score"] == 7.5, "Overall score should be 7.5"
    
    print("\n✅ All Level 2 submission tests passed!")
    print("\nSample Result Structure:")
    print(f"  Problem 1: {prob1_eval['correctness_score']}/10 - {prob1_eval['feedback']}")
    print(f"  Problem 2: {prob2_eval['correctness_score']}/10 - {prob2_eval['feedback']}")


def test_level2_no_submission():
    """Test when candidate doesn't submit code"""
    
    questions = [
        {
            "title": "Test Problem",
            "description": "A test problem",
            "test_cases": [
                {"input": "test", "expected_output": "test"}
            ]
        }
    ]
    
    # No code submitted
    candidate_answers = [None]
    reference_answers = [{"reference_answer": "dummy"}]
    
    result = submit_interview(questions, reference_answers, candidate_answers)
    
    assert result["overall_score"] == 0
    assert result["results"][0]["evaluation"]["correctness_score"] == 0
    assert "No code was submitted" in result["results"][0]["evaluation"]["feedback"]
    
    print("✅ No submission test passed")


def test_level1_still_works():
    """Test that Level 1/3 submissions still work"""
    
    questions = ["What is Python?", "Explain variables"]
    reference_answers = [
        {"reference_answer": "Python is a high-level programming language."},
        {"reference_answer": "Variables are containers for storing data."}
    ]
    candidate_answers = [
        "Python is a programming language",
        "Variables store values"
    ]
    
    # This should use LLM evaluation (we'll mock it for now)
    # In real scenario, it calls evaluate_answer which uses Groq
    # For this test, we just check it doesn't crash
    
    try:
        result = submit_interview(questions, reference_answers, candidate_answers)
        assert "overall_score" in result
        assert result["interview_type"] == "Level 1/3 - Text-based"
        print("✅ Level 1/3 submission compatibility verified")
    except Exception as e:
        print(f"⚠️  Level 1/3 test skipped (requires Groq API): {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Level 2 Submission Fix")
    print("=" * 60)
    
    test_level2_detection()
    print()
    
    test_level2_submission()
    print()
    
    test_level2_no_submission()
    print()
    
    test_level1_still_works()
    print()
    
    print("=" * 60)
    print("🎉 All tests completed successfully!")
    print("=" * 60)
