"""
=========================================
Code Execution Service
AI Interview Platform - Level 2
=========================================
Executes code in sandboxed environment with test cases
"""

import subprocess
import tempfile
import os
import json
import time
from pathlib import Path


class CodeExecutor:
    """
    Execute code in multiple languages with timeout and test cases
    """
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        "python": {
            "extension": ".py",
            "compile_cmd": None,
            "run_cmd": ["python", "{file}"],
            "timeout": 5
        },
        "javascript": {
            "extension": ".js",
            "compile_cmd": None,
            "run_cmd": ["node", "{file}"],
            "timeout": 5
        },
        "java": {
            "extension": ".java",
            "compile_cmd": ["javac", "{file}"],
            "run_cmd": ["java", "{classname}"],
            "timeout": 10
        },
        "cpp": {
            "extension": ".cpp",
            "compile_cmd": ["g++", "{file}", "-o", "{output}"],
            "run_cmd": ["{output}"],
            "timeout": 10
        },
        "c": {
            "extension": ".c",
            "compile_cmd": ["gcc", "{file}", "-o", "{output}"],
            "run_cmd": ["{output}"],
            "timeout": 10
        }
    }
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="code_exec_")
    
    def execute_code(self, code, language, test_cases=None, timeout=5):
        """
        Execute code with test cases
        
        Args:
            code: Source code string
            language: Programming language (python, javascript, java, cpp, c)
            test_cases: List of {"input": "...", "expected_output": "..."}
            timeout: Maximum execution time in seconds
        
        Returns:
            {
                "success": bool,
                "output": str,
                "error": str,
                "execution_time": float,
                "test_results": [...]
            }
        """
        
        if language.lower() not in self.SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "error": f"Unsupported language: {language}. Supported: {', '.join(self.SUPPORTED_LANGUAGES.keys())}",
                "output": "",
                "execution_time": 0,
                "test_results": []
            }
        
        lang_config = self.SUPPORTED_LANGUAGES[language.lower()]
        
        try:
            # Create temporary file
            file_path = self._create_temp_file(code, lang_config["extension"])
            
            # Compile if needed
            if lang_config["compile_cmd"]:
                compile_result = self._compile_code(file_path, lang_config)
                if not compile_result["success"]:
                    return compile_result
            
            # Execute code
            if test_cases:
                return self._run_with_test_cases(file_path, lang_config, test_cases, timeout)
            else:
                return self._run_code(file_path, lang_config, timeout)
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "output": "",
                "execution_time": 0,
                "test_results": []
            }
        
        finally:
            self._cleanup()
    
    def _create_temp_file(self, code, extension):
        """Create temporary file with code"""
        file_path = os.path.join(self.temp_dir, f"code{extension}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return file_path
    
    def _compile_code(self, file_path, lang_config):
        """Compile code (for compiled languages)"""
        try:
            output_path = os.path.join(self.temp_dir, "output")
            classname = Path(file_path).stem
            
            cmd = []
            for part in lang_config["compile_cmd"]:
                cmd.append(
                    part.replace("{file}", file_path)
                        .replace("{output}", output_path)
                        .replace("{classname}", classname)
                )
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Compilation error:\n{result.stderr}",
                    "output": "",
                    "execution_time": 0,
                    "test_results": []
                }
            
            return {"success": True}
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Compilation timeout (10 seconds)",
                "output": "",
                "execution_time": 0,
                "test_results": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Compilation error: {str(e)}",
                "output": "",
                "execution_time": 0,
                "test_results": []
            }
    
    def _run_code(self, file_path, lang_config, timeout, input_data=""):
        """Run code without test cases"""
        try:
            output_path = os.path.join(self.temp_dir, "output")
            classname = Path(file_path).stem
            
            cmd = []
            for part in lang_config["run_cmd"]:
                cmd.append(
                    part.replace("{file}", file_path)
                        .replace("{output}", output_path)
                        .replace("{classname}", classname)
                )
            
            start_time = time.time()
            
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.temp_dir
            )
            
            execution_time = time.time() - start_time
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Runtime error:\n{result.stderr}",
                    "output": result.stdout,
                    "execution_time": execution_time,
                    "test_results": []
                }
            
            return {
                "success": True,
                "output": result.stdout,
                "error": "",
                "execution_time": execution_time,
                "test_results": []
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timeout ({timeout} seconds). Code took too long to run.",
                "output": "",
                "execution_time": timeout,
                "test_results": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Runtime error: {str(e)}",
                "output": "",
                "execution_time": 0,
                "test_results": []
            }
    
    def _run_with_test_cases(self, file_path, lang_config, test_cases, timeout):
        """Run code with multiple test cases"""
        test_results = []
        total_execution_time = 0
        all_passed = True
        
        for idx, test_case in enumerate(test_cases):
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "").strip()
            
            result = self._run_code(file_path, lang_config, timeout, input_data)
            
            if not result["success"]:
                test_results.append({
                    "test_case": idx + 1,
                    "passed": False,
                    "input": input_data,
                    "expected_output": expected_output,
                    "actual_output": result.get("output", ""),
                    "error": result.get("error", ""),
                    "execution_time": result.get("execution_time", 0)
                })
                all_passed = False
                total_execution_time += result.get("execution_time", 0)
                continue
            
            actual_output = result["output"].strip()
            passed = (actual_output == expected_output)
            
            test_results.append({
                "test_case": idx + 1,
                "passed": passed,
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "error": "",
                "execution_time": result["execution_time"]
            })
            
            if not passed:
                all_passed = False
            
            total_execution_time += result["execution_time"]
        
        passed_count = sum(1 for t in test_results if t["passed"])
        
        return {
            "success": all_passed,
            "output": f"{passed_count}/{len(test_cases)} test cases passed",
            "error": "" if all_passed else "Some test cases failed",
            "execution_time": total_execution_time,
            "test_results": test_results,
            "summary": {
                "total": len(test_cases),
                "passed": passed_count,
                "failed": len(test_cases) - passed_count
            }
        }
    
    def _cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Cleanup error: {e}")


# ===================================================
# Code Problem Generator
# ===================================================

def generate_coding_problems(domain, count=5):
    """
    Generate coding problems with test cases for Level 2
    
    Returns list of:
    {
        "title": "Problem title",
        "description": "Problem description",
        "difficulty": "Easy/Medium/Hard",
        "test_cases": [...],
        "starter_code": {...}
    }
    """
    from groq_client import client
    from config import MODEL_NAME
    
    prompt = f"""
You are an expert coding interview problem creator.

Generate EXACTLY {count} coding problems for domain: {domain}

Each problem should include:
1. Clear title
2. Detailed description
3. Input/output format
4. Constraints
5. Example test cases (3-4 cases)

Return as JSON array:
[
  {{
    "title": "Two Sum",
    "description": "Given an array of integers and a target, return indices of two numbers that add up to target.",
    "difficulty": "Easy",
    "input_format": "First line: array of integers\\nSecond line: target integer",
    "output_format": "Two space-separated indices",
    "constraints": "2 <= array length <= 1000\\n-10^9 <= numbers <= 10^9",
    "examples": [
      {{
        "input": "[2,7,11,15]\\n9",
        "output": "0 1",
        "explanation": "nums[0] + nums[1] = 2 + 7 = 9"
      }}
    ],
    "test_cases": [
      {{"input": "[2,7,11,15]\\n9", "expected_output": "0 1"}},
      {{"input": "[3,2,4]\\n6", "expected_output": "1 2"}},
      {{"input": "[3,3]\\n6", "expected_output": "0 1"}}
    ]
  }}
]

Problems should be:
- Relevant to {domain}
- Progressive difficulty (Easy → Medium)
- Clear and unambiguous
- Include edge cases in test cases

Return ONLY valid JSON, no extra text.
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        problems = json.loads(content)
        return problems
    
    except Exception as e:
        print(f"Error generating coding problems: {e}")
        # Return fallback problems
        return get_fallback_problems(domain)


def get_fallback_problems(domain):
    """Fallback coding problems if generation fails"""
    
    if "python" in domain.lower() or "dsa" in domain.lower():
        return [
            {
                "title": "Find Maximum in Array",
                "description": "Write a function that takes an array of integers and returns the maximum value.",
                "difficulty": "Easy",
                "input_format": "Space-separated integers",
                "output_format": "Single integer (maximum value)",
                "test_cases": [
                    {"input": "1 5 3 9 2", "expected_output": "9"},
                    {"input": "10 20 30", "expected_output": "30"},
                    {"input": "-5 -1 -10", "expected_output": "-1"}
                ]
            },
            {
                "title": "Reverse String",
                "description": "Write a function to reverse a string without using built-in reverse functions.",
                "difficulty": "Easy",
                "input_format": "Single line string",
                "output_format": "Reversed string",
                "test_cases": [
                    {"input": "hello", "expected_output": "olleh"},
                    {"input": "Python", "expected_output": "nohtyP"},
                    {"input": "12345", "expected_output": "54321"}
                ]
            },
            {
                "title": "Sum of Even Numbers",
                "description": "Calculate sum of all even numbers in an array.",
                "difficulty": "Easy",
                "input_format": "Space-separated integers",
                "output_format": "Single integer (sum)",
                "test_cases": [
                    {"input": "1 2 3 4 5 6", "expected_output": "12"},
                    {"input": "10 15 20 25", "expected_output": "30"},
                    {"input": "1 3 5 7", "expected_output": "0"}
                ]
            }
        ]
    
    return [
        {
            "title": "Basic Implementation",
            "description": f"Implement a basic function relevant to {domain}.",
            "difficulty": "Easy",
            "test_cases": [
                {"input": "test", "expected_output": "result"}
            ]
        }
    ]


# ===================================================
# Testing
# ===================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Code Execution Service Test")
    print("=" * 70)
    
    executor = CodeExecutor()
    
    # Test Python code
    python_code = """
numbers = list(map(int, input().split()))
print(max(numbers))
"""
    
    test_cases = [
        {"input": "1 5 3 9 2", "expected_output": "9"},
        {"input": "10 20 30", "expected_output": "30"},
        {"input": "-5 -1 -10", "expected_output": "-1"}
    ]
    
    print("\n📝 Testing Python Code:")
    print(python_code)
    print("\n🧪 Running Test Cases...")
    
    result = executor.execute_code(python_code, "python", test_cases)
    
    print(f"\n{'✅' if result['success'] else '❌'} Result: {result['output']}")
    print(f"⏱️  Execution Time: {result['execution_time']:.3f}s")
    
    if result['test_results']:
        print(f"\n📊 Test Results:")
        for test in result['test_results']:
            status = "✅ PASS" if test['passed'] else "❌ FAIL"
            print(f"  Test {test['test_case']}: {status}")
            if not test['passed']:
                print(f"    Expected: {test['expected_output']}")
                print(f"    Got: {test['actual_output']}")
    
    if result.get('summary'):
        summary = result['summary']
        print(f"\n📈 Summary: {summary['passed']}/{summary['total']} passed")
    
    print("\n" + "=" * 70)
