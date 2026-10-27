import { useState } from "react";
import { FaPlay, FaCheck, FaTimes, FaClock } from "react-icons/fa";

function CodeEditor({ problem, onSubmit, problemIndex, totalProblems }) {
    const [code, setCode] = useState(getStarterCode(problem));
    const [language, setLanguage] = useState("python");
    const [isExecuting, setIsExecuting] = useState(false);
    const [executionResult, setExecutionResult] = useState(null);
    const [showHints, setShowHints] = useState(false);

    const languages = [
        { id: "python", name: "Python", icon: "🐍" },
        { id: "javascript", name: "JavaScript", icon: "📜" },
        { id: "java", name: "Java", icon: "☕" },
        { id: "cpp", name: "C++", icon: "⚡" },
        { id: "c", name: "C", icon: "🔧" }
    ];

    function getStarterCode(problem) {
        // Provide starter code templates
        const templates = {
            python: `# ${problem.title}\n# ${problem.description}\n\n# Your code here\n`,
            javascript: `// ${problem.title}\n// ${problem.description}\n\n// Your code here\n`,
            java: `// ${problem.title}\n// ${problem.description}\n\npublic class Solution {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}\n`,
            cpp: `// ${problem.title}\n// ${problem.description}\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}\n`,
            c: `// ${problem.title}\n// ${problem.description}\n\n#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}\n`
        };
        return templates.python;
    }

    const handleLanguageChange = (newLang) => {
        setLanguage(newLang);
        // Reset code with new template
        const templates = {
            python: `# ${problem.title}\n\n# Your code here\n`,
            javascript: `// ${problem.title}\n\n// Your code here\n`,
            java: `public class Solution {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}\n`,
            cpp: `#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}\n`,
            c: `#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}\n`
        };
        setCode(templates[newLang]);
    };

    const runCode = async () => {
        if (!code.trim()) {
            alert("Please write some code first!");
            return;
        }

        setIsExecuting(true);
        setExecutionResult(null);

        try {
            const response = await fetch('http://localhost:8000/execute-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    language: language,
                    test_cases: problem.test_cases || [],
                    timeout: 5
                })
            });

            const result = await response.json();
            setExecutionResult(result);
            
        } catch (error) {
            console.error("Execution error:", error);
            setExecutionResult({
                success: false,
                error: "Failed to execute code. Is the backend running?",
                output: "",
                test_results: []
            });
        } finally {
            setIsExecuting(false);
        }
    };

    const submitCode = () => {
        if (!executionResult) {
            alert("Please run your code first to verify it works!");
            return;
        }

        if (!executionResult.success) {
            const confirm = window.confirm(
                "Your code didn't pass all test cases. Submit anyway?"
            );
            if (!confirm) return;
        }

        onSubmit({
            code: code,
            language: language,
            result: executionResult
        });
    };

    return (
        <div className="min-h-screen bg-slate-950 p-6">
            <div className="max-w-7xl mx-auto">
                
                {/* Header */}
                <div className="bg-slate-900 rounded-xl p-6 mb-6 shadow-xl border border-slate-800">
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-2xl font-bold text-blue-400">
                                Level 2: Coding Challenge
                            </h1>
                            <p className="text-gray-400 mt-1">
                                Problem {problemIndex + 1} of {totalProblems}
                            </p>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setShowHints(!showHints)}
                                className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg font-semibold"
                            >
                                {showHints ? "Hide Hints" : "💡 Show Hints"}
                            </button>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    
                    {/* Problem Statement */}
                    <div className="bg-slate-900 rounded-xl p-6 shadow-xl border border-slate-800 h-fit">
                        <h2 className="text-xl font-bold text-white mb-4">
                            📋 {problem.title}
                        </h2>
                        
                        <div className="mb-4">
                            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                                problem.difficulty === 'Easy' ? 'bg-green-600 text-white' :
                                problem.difficulty === 'Medium' ? 'bg-yellow-600 text-white' :
                                'bg-red-600 text-white'
                            }`}>
                                {problem.difficulty}
                            </span>
                        </div>

                        <div className="text-gray-300 mb-4">
                            <p className="leading-relaxed">{problem.description}</p>
                        </div>

                        {/* Input/Output Format */}
                        {problem.input_format && (
                            <div className="mb-4">
                                <h3 className="text-blue-400 font-semibold mb-2">Input Format:</h3>
                                <p className="text-gray-300 text-sm bg-slate-800 p-3 rounded">
                                    {problem.input_format}
                                </p>
                            </div>
                        )}

                        {problem.output_format && (
                            <div className="mb-4">
                                <h3 className="text-green-400 font-semibold mb-2">Output Format:</h3>
                                <p className="text-gray-300 text-sm bg-slate-800 p-3 rounded">
                                    {problem.output_format}
                                </p>
                            </div>
                        )}

                        {/* Examples */}
                        {problem.examples && problem.examples.length > 0 && (
                            <div className="mb-4">
                                <h3 className="text-purple-400 font-semibold mb-2">Examples:</h3>
                                {problem.examples.map((example, idx) => (
                                    <div key={idx} className="bg-slate-800 p-3 rounded mb-2">
                                        <p className="text-sm text-gray-400 mb-1">Input:</p>
                                        <pre className="text-white text-sm mb-2">{example.input}</pre>
                                        <p className="text-sm text-gray-400 mb-1">Output:</p>
                                        <pre className="text-green-400 text-sm mb-2">{example.output}</pre>
                                        {example.explanation && (
                                            <>
                                                <p className="text-sm text-gray-400 mb-1">Explanation:</p>
                                                <p className="text-gray-300 text-sm">{example.explanation}</p>
                                            </>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Hints */}
                        {showHints && problem.hints && (
                            <div className="bg-yellow-900/30 border border-yellow-500 rounded p-4">
                                <h3 className="text-yellow-400 font-semibold mb-2">💡 Hints:</h3>
                                <ul className="list-disc list-inside text-gray-300 text-sm space-y-1">
                                    {problem.hints.map((hint, idx) => (
                                        <li key={idx}>{hint}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>

                    {/* Code Editor & Results */}
                    <div className="space-y-4">
                        
                        {/* Language Selector */}
                        <div className="bg-slate-900 rounded-xl p-4 shadow-xl border border-slate-800">
                            <label className="text-gray-300 font-semibold mb-2 block">
                                Programming Language:
                            </label>
                            <div className="flex gap-2 flex-wrap">
                                {languages.map((lang) => (
                                    <button
                                        key={lang.id}
                                        onClick={() => handleLanguageChange(lang.id)}
                                        className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                                            language === lang.id
                                                ? 'bg-blue-600 text-white'
                                                : 'bg-slate-800 text-gray-300 hover:bg-slate-700'
                                        }`}
                                    >
                                        {lang.icon} {lang.name}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Code Editor */}
                        <div className="bg-slate-900 rounded-xl p-4 shadow-xl border border-slate-800">
                            <div className="flex justify-between items-center mb-3">
                                <h3 className="text-white font-semibold">Code Editor</h3>
                                <div className="flex gap-2">
                                    <button
                                        onClick={runCode}
                                        disabled={isExecuting}
                                        className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold flex items-center gap-2"
                                    >
                                        <FaPlay /> {isExecuting ? "Running..." : "Run Code"}
                                    </button>
                                    <button
                                        onClick={submitCode}
                                        disabled={isExecuting}
                                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold flex items-center gap-2"
                                    >
                                        <FaCheck /> Submit
                                    </button>
                                </div>
                            </div>
                            
                            <textarea
                                value={code}
                                onChange={(e) => setCode(e.target.value)}
                                className="w-full h-96 bg-slate-950 text-white font-mono text-sm p-4 rounded-lg border border-slate-700 focus:border-blue-500 outline-none resize-none"
                                placeholder="Write your code here..."
                                spellCheck={false}
                            />
                        </div>

                        {/* Execution Results */}
                        {executionResult && (
                            <div className={`rounded-xl p-4 shadow-xl border ${
                                executionResult.success 
                                    ? 'bg-green-900/30 border-green-500'
                                    : 'bg-red-900/30 border-red-500'
                            }`}>
                                <div className="flex items-center gap-2 mb-3">
                                    {executionResult.success ? (
                                        <FaCheck className="text-green-400 text-xl" />
                                    ) : (
                                        <FaTimes className="text-red-400 text-xl" />
                                    )}
                                    <h3 className="text-white font-semibold">
                                        {executionResult.success ? "All Tests Passed! ✅" : "Test Failed ❌"}
                                    </h3>
                                    <div className="ml-auto flex items-center gap-2 text-gray-300">
                                        <FaClock />
                                        <span className="text-sm">
                                            {executionResult.execution_time?.toFixed(3)}s
                                        </span>
                                    </div>
                                </div>

                                {/* Test Results */}
                                {executionResult.test_results && executionResult.test_results.length > 0 && (
                                    <div className="space-y-2">
                                        <h4 className="text-gray-300 font-semibold mb-2">Test Cases:</h4>
                                        {executionResult.test_results.map((test, idx) => (
                                            <div
                                                key={idx}
                                                className={`p-3 rounded ${
                                                    test.passed
                                                        ? 'bg-green-900/30 border border-green-700'
                                                        : 'bg-red-900/30 border border-red-700'
                                                }`}
                                            >
                                                <div className="flex items-center gap-2 mb-2">
                                                    {test.passed ? (
                                                        <FaCheck className="text-green-400" />
                                                    ) : (
                                                        <FaTimes className="text-red-400" />
                                                    )}
                                                    <span className="text-white font-semibold">
                                                        Test Case {test.test_case}
                                                    </span>
                                                </div>
                                                
                                                {!test.passed && (
                                                    <>
                                                        <div className="text-sm space-y-1">
                                                            <p className="text-gray-400">Input:</p>
                                                            <pre className="text-white bg-slate-950 p-2 rounded text-xs overflow-x-auto">
                                                                {test.input}
                                                            </pre>
                                                            
                                                            <p className="text-gray-400 mt-2">Expected:</p>
                                                            <pre className="text-green-400 bg-slate-950 p-2 rounded text-xs overflow-x-auto">
                                                                {test.expected_output}
                                                            </pre>
                                                            
                                                            <p className="text-gray-400 mt-2">Got:</p>
                                                            <pre className="text-red-400 bg-slate-950 p-2 rounded text-xs overflow-x-auto">
                                                                {test.actual_output}
                                                            </pre>
                                                        </div>
                                                    </>
                                                )}
                                            </div>
                                        ))}
                                        
                                        {/* Summary */}
                                        {executionResult.summary && (
                                            <div className="mt-3 p-3 bg-slate-800 rounded">
                                                <p className="text-white font-semibold">
                                                    Summary: {executionResult.summary.passed}/{executionResult.summary.total} passed
                                                </p>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Output */}
                                {executionResult.output && (
                                    <div className="mt-3">
                                        <p className="text-gray-400 text-sm mb-1">Output:</p>
                                        <pre className="text-white bg-slate-950 p-3 rounded text-sm overflow-x-auto">
                                            {executionResult.output}
                                        </pre>
                                    </div>
                                )}

                                {/* Error */}
                                {executionResult.error && (
                                    <div className="mt-3">
                                        <p className="text-red-400 text-sm mb-1">Error:</p>
                                        <pre className="text-red-300 bg-slate-950 p-3 rounded text-sm overflow-x-auto">
                                            {executionResult.error}
                                        </pre>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CodeEditor;
