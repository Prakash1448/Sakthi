import { useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";



function Home() {
    const navigate = useNavigate();

    const [candidateName, setCandidateName] = useState("");

    const [domain, setDomain] = useState("DSA");

    const [difficulty, setDifficulty] = useState("Fundamentals");
    const [loading, setLoading] = useState(false);
    const startInterview = async () => {

    try {

        setLoading(true);

        const response = await api.post("/start-interview", {

            domain,

            difficulty

        });

        console.log(response.data);

      navigate("/interview", {

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

                        Domain

                    </label>

                    <select

                        value={domain}

                        onChange={(e)=>setDomain(e.target.value)}

                        className="w-full mt-2 p-3 rounded-lg bg-slate-800 text-white"

                    >

                        <option>DSA</option>

                        <option>Java</option>

                        <option>Python</option>

                        <option>React</option>

                        <option>AI/ML</option>

                    </select>

                </div>

                <div className="mt-6">

                    <label className="text-gray-300">

                        Difficulty

                    </label>

                    <select

                        value={difficulty}

                        onChange={(e)=>setDifficulty(e.target.value)}

                        className="w-full mt-2 p-3 rounded-lg bg-slate-800 text-white"

                    >

                        <option>Fundamentals</option>

                        <option>Application</option>

                        <option>Problem Solving</option>

                    </select>

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

            </div>

        </div>

    );

}

export default Home;