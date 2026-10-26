import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";



function Home() {
    const navigate = useNavigate();

    const [candidateName, setCandidateName] = useState("");

    const [domain, setDomain] = useState("Python Programming");

    const [difficulty, setDifficulty] = useState("Level 1 - Basic Fundamentals");
    const [loading, setLoading] = useState(false);
    const startInterview = async () => {

    try {

        setLoading(true);

        const response = await api.post("/start-interview", {

            domain,

            difficulty

        });

        console.log(response.data);

      navigate("/camera-setup", {

    state: response.data

});
    }

    catch(error){

        console.error(error);

        alert("Backend Connection Failed");

    }

    finally{

        setLoading(false);

    }

};

    return (

        <div className="min-h-screen bg-slate-950 flex items-center justify-center">

            <div className="w-full max-w-xl bg-slate-900 rounded-2xl shadow-2xl p-10">

                <h1 className="text-4xl font-bold text-center text-blue-400">

                    AI Interview Platform

                </h1>

                <p className="text-gray-400 text-center mt-2">

                    Technical Interview Evaluation using AI

                </p>

                <div className="mt-8">

                    <label className="text-gray-300">

                        Candidate Name

                    </label>

                    <input

                        type="text"

                        placeholder="Enter your name"

                        value={candidateName}

                        onChange={(e)=>setCandidateName(e.target.value)}

                        className="w-full mt-2 p-3 rounded-lg bg-slate-800 text-white outline-none"

                    />

                </div>

                <div className="mt-6">

                    <label className="text-gray-300">

                        Technical Domain

                    </label>

                    <select

                        value={domain}

                        onChange={(e)=>setDomain(e.target.value)}

                        className="w-full mt-2 p-3 rounded-lg bg-slate-800 text-white"

                    >

                        <option>Python Programming</option>

                        <option>Data Structures & Algorithms (DSA)</option>

                        <option>Machine Learning & AI</option>

                        <option>Web Development - Frontend</option>

                        <option>Web Development - Backend</option>

                        <option>Full Stack Development</option>

                        <option>React.js & Modern Frontend</option>

                        <option>Node.js & Express</option>

                        <option>Database & SQL</option>

                        <option>Cloud Computing (AWS/Azure/GCP)</option>

                        <option>DevOps & CI/CD</option>

                        <option>Data Science & Analytics</option>

                        <option>Cybersecurity</option>

                        <option>Mobile App Development</option>

                        <option>RAG (Retrieval Augmented Generation) & LLM Applications</option>

                    </select>

                </div>

                <div className="mt-6">

                    <label className="text-gray-300 block mb-2">

                        Interview Level

                    </label>

                    <select

                        value={difficulty}

                        onChange={(e)=>setDifficulty(e.target.value)}

                        className="w-full mt-2 p-3 rounded-lg bg-slate-800 text-white"

                    >

                        <option value="Level 1 - Basic Fundamentals">
                            Level 1 - Basic Fundamentals (What is...? Definitions)
                        </option>

                        <option value="Level 2 - Coding Logic">
                            Level 2 - Coding Logic (Explain approach, no code)
                        </option>

                        <option value="Level 3 - HR & AI Knowledge">
                            Level 3 - HR & AI Knowledge (Behavioral + AI Tools)
                        </option>

                    </select>
                    
                    <div className="mt-3 p-3 bg-slate-800 rounded-lg text-sm text-gray-400">
                        {difficulty === "Level 1 - Basic Fundamentals" && (
                            <div>
                                <strong className="text-blue-400">Level 1:</strong> Tests basic knowledge, 
                                definitions, and fundamental concepts. No coding required.
                            </div>
                        )}
                        {difficulty === "Level 2 - Coding Logic" && (
                            <div>
                                <strong className="text-yellow-400">Level 2:</strong> Explain your logic 
                                and approach to solve problems. No actual code writing needed.
                            </div>
                        )}
                        {difficulty === "Level 3 - HR & AI Knowledge" && (
                            <div>
                                <strong className="text-green-400">Level 3:</strong> HR behavioral questions 
                                + Modern AI tools usage (ChatGPT, Copilot, etc.)
                            </div>
                        )}
                    </div>

                </div>

              <button

    onClick={startInterview}

    className="w-full mt-8 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold transition"

>

{

loading ?

"Loading..."

:

"Start Interview"

}

</button>

                <button
                    onClick={() => {
                        if (candidateName.trim()) {
                            navigate('/dashboard', { state: { username: candidateName } });
                        } else {
                            alert("Please enter your name first");
                        }
                    }}
                    className="w-full mt-4 bg-purple-500 hover:bg-purple-600 text-white py-3 rounded-lg text-lg font-semibold transition"
                >
                    📊 View Dashboard
                </button>

            </div>

        </div>

    );

}

export default Home;

// Dashboard button - View user performance and history
