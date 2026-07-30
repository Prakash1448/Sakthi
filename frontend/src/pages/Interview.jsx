import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../services/api";

function Interview() {

    const location = useLocation();
    const navigate = useNavigate();

    const interview = location.state;

    if (!interview) {

        return (

            <h1 className="text-white text-center mt-20">

                No Interview Data Found

            </h1>

        );

    }

    const [currentQuestion, setCurrentQuestion] = useState(0);

    const [answers, setAnswers] = useState(

        Array(interview.questions.length).fill("")

    );

    const [loading, setLoading] = useState(false);

    const updateAnswer = (value) => {

        const temp = [...answers];

        temp[currentQuestion] = value;

        setAnswers(temp);

    };

    const nextQuestion = () => {

        if (currentQuestion < interview.questions.length - 1) {

            setCurrentQuestion(currentQuestion + 1);

        }

    };

    const previousQuestion = () => {

        if (currentQuestion > 0) {

            setCurrentQuestion(currentQuestion - 1);

        }

    };

    const submitInterview = async () => {

        try {

            setLoading(true);

            const response = await api.post("/submit-interview", {

                questions: interview.questions,

                reference_answers: interview.reference_answers,

                candidate_answers: answers

            });

            navigate("/result", {

                state: response.data

            });

        }

        catch (error) {

            console.error(error);

            alert("Failed to submit interview");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="min-h-screen bg-slate-950 flex justify-center items-center">

            <div className="bg-slate-900 w-[900px] rounded-xl p-10 shadow-xl">

                <h1 className="text-3xl font-bold text-blue-400">

                    AI Interview

                </h1>

                <p className="text-gray-400 mt-2">

                    Difficulty :

                    <span className="text-white ml-2">

                        {interview.difficulty}

                    </span>

                </p>

                <div className="mt-10">

                    <h2 className="text-xl text-white">

                        Question {currentQuestion + 1} / {interview.questions.length}

                    </h2>

                    <div className="mt-5 bg-slate-800 rounded-lg p-6">

                        <p className="text-gray-200 text-lg">

                            {interview.questions[currentQuestion]}

                        </p>

                    </div>

                </div>

                <div className="mt-8">

                    <label className="text-gray-300 text-lg">

                        Your Answer

                    </label>

                    <textarea

                        rows={8}

                        value={answers[currentQuestion]}

                        onChange={(e) => updateAnswer(e.target.value)}

                        placeholder="Type your answer here..."

                        className="w-full mt-3 bg-slate-800 rounded-xl p-5 text-white outline-none"

                    />

                </div>

                <div className="flex justify-between mt-10">

                    <button

                        onClick={previousQuestion}

                        disabled={currentQuestion === 0 || loading}

                        className="bg-gray-700 hover:bg-gray-600 disabled:bg-gray-900 text-white px-6 py-3 rounded-lg"

                    >

                        Previous

                    </button>

                    <button

                        onClick={() => {

                            if (currentQuestion === interview.questions.length - 1) {

                                submitInterview();

                            }

                            else {

                                nextQuestion();

                            }

                        }}

                        disabled={loading}

                        className="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-900 text-white px-6 py-3 rounded-lg"

                    >

                        {

                            loading

                                ? "Submitting..."

                                : currentQuestion === interview.questions.length - 1

                                    ? "Submit Interview"

                                    : "Next"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}

export default Interview;