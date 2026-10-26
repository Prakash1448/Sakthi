import { useLocation, useNavigate } from "react-router-dom";

function Result() {

    const location = useLocation();

    const navigate = useNavigate();

    const result = location.state;

    if (!result) {

        return (

            <div className="min-h-screen bg-slate-950 flex justify-center items-center">

                <h1 className="text-white text-3xl">

                    No Result Found

                </h1>

            </div>

        );

    }

    return (

        <div className="min-h-screen bg-slate-950 p-10">

            <div className="max-w-6xl mx-auto">

                <h1 className="text-4xl font-bold text-center text-blue-400">

                    Interview Result

                </h1>

                <div className="bg-slate-900 mt-8 rounded-xl p-8">

                    <h2 className="text-3xl text-white">

                        Overall Score

                    </h2>

                    <p className="text-6xl font-bold text-green-400 mt-4">

                        {result.overall_score} %

                    </p>

                    <div className="w-full bg-slate-700 rounded-full h-5 mt-6">

                        <div

                            className="bg-green-500 h-5 rounded-full"

                            style={{

                                width: `${result.overall_score}%`

                            }}

                        ></div>

                    </div>

                </div>

                <div className="mt-10">

                    {

                        result.results.map((item,index)=>(

                            <div

                                key={index}

                                className="bg-slate-900 rounded-xl p-6 mb-8"

                            >

                                <h2 className="text-blue-400 text-xl font-bold">

                                    Question {index+1}

                                </h2>

                                <p className="text-white mt-3">

                                    {item.question}

                                </p>

                                <div className="mt-5">

                                    <h3 className="text-yellow-400">

                                        Your Answer

                                    </h3>

                                    <p className="text-gray-300 mt-2">

                                        {item.candidate_answer}

                                    </p>

                                </div>

                                <div className="mt-5">

                                    <h3 className="text-green-400">

                                        Score

                                    </h3>

                                    <p className="text-white">

                                        {item.evaluation.correctness_score} %

                                    </p>

                                </div>

                                <div className="mt-5">

                                    <h3 className="text-green-400">

                                        Feedback

                                    </h3>

                                    <p className="text-gray-300">

                                        {item.evaluation.feedback}

                                    </p>

                                </div>

                                <div className="mt-5">

                                    <h3 className="text-blue-400">

                                        Strengths

                                    </h3>

                                    <p className="text-gray-300">

                                        {item.evaluation.strengths}

                                    </p>

                                </div>

                                <div className="mt-5">

                                    <h3 className="text-red-400">

                                        Missing Points

                                    </h3>

                                    <p className="text-gray-300">

                                        {item.evaluation.missing_points}

                                    </p>

                                </div>

                                <div className="mt-5">

                                    <h3 className="text-purple-400">

                                        Recommendation

                                    </h3>

                                    <p className="text-gray-300">

                                        {item.evaluation.recommendation}

                                    </p>

                                </div>

                            </div>

                        ))

                    }

                </div>

                <button

                    onClick={()=>navigate("/")}

                    className="w-full bg-blue-500 hover:bg-blue-600 py-4 rounded-xl text-white text-xl font-semibold"

                >

                    Start New Interview

                </button>
                
                <button
                    onClick={() => navigate("/dashboard")}
                    className="w-full mt-4 bg-purple-500 hover:bg-purple-600 py-4 rounded-xl text-white text-xl font-semibold"
                >
                    📊 View Dashboard
                </button>

            </div>

        </div>

    );

}

export default Result;