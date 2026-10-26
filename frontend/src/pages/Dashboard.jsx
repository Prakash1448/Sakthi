import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../services/api";
import { 
    FaUser, 
    FaTrophy, 
    FaChartLine, 
    FaCheckCircle, 
    FaExclamationTriangle,
    FaClock,
    FaDownload,
    FaPlay,
    FaFileAlt,
    FaStar,
    FaAward,
    FaChartBar
} from "react-icons/fa";

function Dashboard() {
    const navigate = useNavigate();
    const location = useLocation();
    
    // Get username from location state or localStorage
    const [username, setUsername] = useState(
        location.state?.username || localStorage.getItem('interview_username') || ''
    );
    
    const [reportData, setReportData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showStartModal, setShowStartModal] = useState(false);
    const [selectedLevel, setSelectedLevel] = useState('');
    const [selectedDomain, setSelectedDomain] = useState('');

    // Domains list
    const domains = [
        "Python Programming",
        "Data Structures & Algorithms",
        "Machine Learning & AI",
        "Web Development - Frontend",
        "Web Development - Backend",
        "Full Stack Development",
        "React.js",
        "Node.js",
        "Database & SQL",
        "Cloud Computing (AWS/Azure/GCP)",
        "DevOps & CI/CD",
        "Data Science & Analytics",
        "Cybersecurity",
        "Mobile App Development",
        "RAG & LLM Applications"
    ];

    const levels = [
        "Level 1 - Basic Fundamentals",
        "Level 2 - Coding Logic",
        "Level 3 - HR & AI Knowledge"
    ];

    useEffect(() => {
        if (username) {
            fetchUserReport();
            // Save to localStorage
            localStorage.setItem('interview_username', username);
        }
    }, [username]);

    const fetchUserReport = async () => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await api.get(`/reports/user/${username}`);
            
            if (response.data.success) {
                setReportData(response.data.data);
            } else {
                setError(response.data.error || "Failed to load report");
            }
        } catch (err) {
            console.error("Error fetching report:", err);
            setError("Could not load user data. Start an interview to create your profile.");
        } finally {
            setLoading(false);
        }
    };

    const downloadPDF = async () => {
        try {
            window.open(`http://localhost:8000/reports/user/${username}/pdf`, '_blank');
        } catch (err) {
            alert("Failed to download PDF report");
        }
    };

    const startNewInterview = () => {
        setShowStartModal(true);
    };

    const launchInterview = async () => {
        if (!selectedDomain || !selectedLevel) {
            alert("Please select both domain and level");
            return;
        }

        try {
            const response = await api.post('/interview/start-with-user', {
                username: username,
                domain: selectedDomain,
                level: selectedLevel
            });

            if (response.data.success) {
                navigate('/camera-setup', {
                    state: {
                        username: username,
                        domain: selectedDomain,
                        level: selectedLevel,
                        sessionId: response.data.session_id,
                        proctoringSessionId: response.data.proctoring_session_id,
                        interview: {
                            questions: response.data.questions,
                            reference_answers: response.data.reference_answers,
                            difficulty: selectedLevel,
                            domain: selectedDomain
                        }
                    }
                });
            }
        } catch (err) {
            alert("Failed to start interview: " + err.message);
        }
    };

    const getPerformanceColor = (score) => {
        if (score >= 7) return 'text-green-400';
        if (score >= 5) return 'text-yellow-400';
        return 'text-red-400';
    };

    const getPerformanceBadge = (score) => {
        if (score >= 7) return { text: 'Excellent', color: 'bg-green-500' };
        if (score >= 5) return { text: 'Good', color: 'bg-yellow-500' };
        if (score >= 3) return { text: 'Average', color: 'bg-orange-500' };
        return { text: 'Needs Work', color: 'bg-red-500' };
    };

    const getCompletionColor = (rate) => {
        if (rate >= 80) return 'bg-green-500';
        if (rate >= 60) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    if (!username) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <div className="bg-slate-900 rounded-xl p-10 max-w-md w-full shadow-2xl border border-slate-800">
                    <h2 className="text-2xl font-bold text-white mb-6 text-center">
                        Welcome to Dashboard
                    </h2>
                    <input
                        type="text"
                        placeholder="Enter your name"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="w-full bg-slate-800 text-white px-4 py-3 rounded-lg mb-4 outline-none border border-slate-700 focus:border-blue-500"
                    />
                    <button
                        onClick={() => {
                            if (username.trim()) {
                                fetchUserReport();
                            } else {
                                alert("Please enter your name");
                            }
                        }}
                        className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg font-semibold"
                    >
                        Enter Dashboard
                    </button>
                    <button
                        onClick={() => navigate('/')}
                        className="w-full mt-3 bg-slate-700 hover:bg-slate-600 text-white py-3 rounded-lg font-semibold"
                    >
                        Back to Home
                    </button>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-white text-xl">Loading Dashboard...</p>
                </div>
            </div>
        );
    }

    const stats = reportData?.statistics || {};
    const user = reportData?.user || {};
    const levelData = reportData?.level_data || {};

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
            {/* Header */}
            <div className="bg-slate-900 border-b border-slate-800 shadow-xl">
                <div className="container mx-auto px-6 py-6">
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                                <FaUser className="text-blue-400" />
                                {username}'s Dashboard
                            </h1>
                            <p className="text-gray-400 mt-1">
                                {user.domain || "No domain selected yet"}
                            </p>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={startNewInterview}
                                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 shadow-lg transition-all"
                            >
                                <FaPlay /> Start New Interview
                            </button>
                            {reportData && (
                                <button
                                    onClick={downloadPDF}
                                    className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 shadow-lg transition-all"
                                >
                                    <FaDownload /> Download Report
                                </button>
                            )}
                            <button
                                onClick={() => navigate('/')}
                                className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-lg font-semibold shadow-lg transition-all"
                            >
                                Home
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-6 py-8">
                {error && (
                    <div className="bg-yellow-900/30 border border-yellow-500 text-yellow-200 px-6 py-4 rounded-lg mb-6">
                        <p className="font-semibold">⚠️ {error}</p>
                        <p className="text-sm mt-2">Start an interview to see your dashboard statistics.</p>
                    </div>
                )}

                {reportData && (
                    <>
                        {/* Stats Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                            {/* Average Score Card */}
                            <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl p-6 shadow-xl border border-blue-500/30">
                                <div className="flex items-center justify-between mb-3">
                                    <FaTrophy className="text-yellow-300 text-3xl" />
                                    <span className={`text-4xl font-bold ${getPerformanceColor(stats.average_score)}`}>
                                        {stats.average_score?.toFixed(1) || '0.0'}
                                    </span>
                                </div>
                                <h3 className="text-white text-lg font-semibold">Average Score</h3>
                                <div className="mt-2">
                                    <span className={`${getPerformanceBadge(stats.average_score).color} text-white text-xs px-3 py-1 rounded-full`}>
                                        {getPerformanceBadge(stats.average_score).text}
                                    </span>
                                </div>
                            </div>

                            {/* Total Sessions Card */}
                            <div className="bg-gradient-to-br from-purple-600 to-purple-800 rounded-xl p-6 shadow-xl border border-purple-500/30">
                                <div className="flex items-center justify-between mb-3">
                                    <FaFileAlt className="text-purple-200 text-3xl" />
                                    <span className="text-4xl font-bold text-white">
                                        {stats.total_sessions || 0}
                                    </span>
                                </div>
                                <h3 className="text-white text-lg font-semibold">Total Sessions</h3>
                                <p className="text-purple-200 text-sm mt-2">
                                    {Object.keys(levelData).length} levels completed
                                </p>
                            </div>

                            {/* Completion Rate Card */}
                            <div className="bg-gradient-to-br from-green-600 to-green-800 rounded-xl p-6 shadow-xl border border-green-500/30">
                                <div className="flex items-center justify-between mb-3">
                                    <FaCheckCircle className="text-green-200 text-3xl" />
                                    <span className="text-4xl font-bold text-white">
                                        {stats.completion_rate?.toFixed(0) || '0'}%
                                    </span>
                                </div>
                                <h3 className="text-white text-lg font-semibold">Completion Rate</h3>
                                <div className="mt-3 bg-green-900/50 rounded-full h-2">
                                    <div 
                                        className={`h-2 rounded-full ${getCompletionColor(stats.completion_rate)}`}
                                        style={{ width: `${stats.completion_rate || 0}%` }}
                                    />
                                </div>
                            </div>

                            {/* Warnings Card */}
                            <div className="bg-gradient-to-br from-orange-600 to-orange-800 rounded-xl p-6 shadow-xl border border-orange-500/30">
                                <div className="flex items-center justify-between mb-3">
                                    <FaExclamationTriangle className="text-orange-200 text-3xl" />
                                    <span className="text-4xl font-bold text-white">
                                        {stats.total_warnings || 0}
                                    </span>
                                </div>
                                <h3 className="text-white text-lg font-semibold">Warnings</h3>
                                <p className="text-orange-200 text-sm mt-2">
                                    Proctoring violations
                                </p>
                            </div>
                        </div>

                        {/* Questions Stats */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                            <div className="bg-slate-800 rounded-xl p-6 shadow-xl border border-slate-700">
                                <div className="flex items-center gap-3 mb-2">
                                    <FaChartBar className="text-blue-400 text-2xl" />
                                    <h3 className="text-white text-lg font-semibold">Total Questions</h3>
                                </div>
                                <p className="text-4xl font-bold text-blue-400">{stats.total_questions || 0}</p>
                            </div>

                            <div className="bg-slate-800 rounded-xl p-6 shadow-xl border border-slate-700">
                                <div className="flex items-center gap-3 mb-2">
                                    <FaCheckCircle className="text-green-400 text-2xl" />
                                    <h3 className="text-white text-lg font-semibold">Answered</h3>
                                </div>
                                <p className="text-4xl font-bold text-green-400">{stats.total_answered || 0}</p>
                            </div>

                            <div className="bg-slate-800 rounded-xl p-6 shadow-xl border border-slate-700">
                                <div className="flex items-center gap-3 mb-2">
                                    <FaClock className="text-yellow-400 text-2xl" />
                                    <h3 className="text-white text-lg font-semibold">Unanswered</h3>
                                </div>
                                <p className="text-4xl font-bold text-yellow-400">
                                    {(stats.total_questions || 0) - (stats.total_answered || 0)}
                                </p>
                            </div>
                        </div>

                        {/* Level Performance */}
                        <div className="bg-slate-800 rounded-xl p-6 shadow-xl border border-slate-700 mb-8">
                            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                                <FaChartLine className="text-blue-400" />
                                Level Performance
                            </h2>

                            {Object.keys(levelData).length > 0 ? (
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    {Object.entries(levelData).map(([levelName, sessions]) => {
                                        const latest = sessions[0];
                                        const score = latest?.total_score || 0;
                                        const percentage = latest?.percentage || 0;

                                        return (
                                            <div
                                                key={levelName}
                                                className="bg-slate-900 rounded-lg p-5 border border-slate-700 hover:border-blue-500 transition-all"
                                            >
                                                <div className="flex items-start justify-between mb-3">
                                                    <h3 className="text-white font-semibold text-lg">
                                                        {levelName.replace("Level ", "L")}
                                                    </h3>
                                                    <FaStar className="text-yellow-400 text-xl" />
                                                </div>

                                                <div className="mb-4">
                                                    <div className="flex justify-between items-center mb-2">
                                                        <span className="text-gray-400">Score</span>
                                                        <span className={`text-2xl font-bold ${getPerformanceColor(score)}`}>
                                                            {score.toFixed(1)}/10
                                                        </span>
                                                    </div>
                                                    <div className="bg-slate-800 rounded-full h-3">
                                                        <div
                                                            className={`h-3 rounded-full ${
                                                                score >= 7 ? 'bg-green-500' :
                                                                score >= 5 ? 'bg-yellow-500' :
                                                                'bg-red-500'
                                                            }`}
                                                            style={{ width: `${(score / 10) * 100}%` }}
                                                        />
                                                    </div>
                                                </div>

                                                <div className="grid grid-cols-2 gap-3 text-sm">
                                                    <div>
                                                        <p className="text-gray-400">Percentage</p>
                                                        <p className="text-white font-semibold">{percentage.toFixed(1)}%</p>
                                                    </div>
                                                    <div>
                                                        <p className="text-gray-400">Attempts</p>
                                                        <p className="text-white font-semibold">{sessions.length}</p>
                                                    </div>
                                                    <div>
                                                        <p className="text-gray-400">Questions</p>
                                                        <p className="text-white font-semibold">
                                                            {latest?.candidate_answers?.filter(a => a).length || 0}/
                                                            {latest?.questions?.length || 0}
                                                        </p>
                                                    </div>
                                                    <div>
                                                        <p className="text-gray-400">Warnings</p>
                                                        <p className="text-white font-semibold">
                                                            {latest?.proctoring_warnings || 0}
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="mt-4">
                                                    <span className={`${getPerformanceBadge(score).color} text-white text-xs px-3 py-1 rounded-full`}>
                                                        {getPerformanceBadge(score).text}
                                                    </span>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            ) : (
                                <div className="text-center py-12">
                                    <FaAward className="text-gray-600 text-6xl mx-auto mb-4" />
                                    <p className="text-gray-400 text-lg">No levels completed yet</p>
                                    <button
                                        onClick={startNewInterview}
                                        className="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold"
                                    >
                                        Start Your First Interview
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Completed Levels Badge */}
                        {user.completed_levels && user.completed_levels.length > 0 && (
                            <div className="bg-gradient-to-r from-green-600 to-green-800 rounded-xl p-6 shadow-xl border border-green-500/30">
                                <h2 className="text-white text-xl font-bold mb-4 flex items-center gap-3">
                                    <FaAward className="text-yellow-300" />
                                    Achievements
                                </h2>
                                <div className="flex flex-wrap gap-3">
                                    {user.completed_levels.map((level, index) => (
                                        <div
                                            key={index}
                                            className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg text-white font-semibold"
                                        >
                                            ✓ {level}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                )}

                {!reportData && !error && (
                    <div className="bg-slate-800 rounded-xl p-12 text-center shadow-xl border border-slate-700">
                        <FaPlay className="text-blue-400 text-6xl mx-auto mb-6" />
                        <h2 className="text-2xl font-bold text-white mb-4">
                            Ready to Start Your Journey?
                        </h2>
                        <p className="text-gray-400 mb-6 text-lg">
                            Take your first interview to unlock your personalized dashboard
                        </p>
                        <button
                            onClick={startNewInterview}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-lg"
                        >
                            Start Your First Interview
                        </button>
                    </div>
                )}
            </div>

            {/* Start Interview Modal */}
            {showStartModal && (
                <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-slate-900 rounded-xl p-8 max-w-md w-full shadow-2xl border border-slate-700">
                        <h3 className="text-2xl font-bold text-white mb-6">Start New Interview</h3>

                        <div className="mb-5">
                            <label className="text-gray-300 mb-2 block font-semibold">Select Domain</label>
                            <select
                                value={selectedDomain}
                                onChange={(e) => setSelectedDomain(e.target.value)}
                                className="w-full bg-slate-800 text-white px-4 py-3 rounded-lg outline-none border border-slate-700 focus:border-blue-500"
                            >
                                <option value="">Choose a domain...</option>
                                {domains.map((domain, index) => (
                                    <option key={index} value={domain}>{domain}</option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-6">
                            <label className="text-gray-300 mb-2 block font-semibold">Select Level</label>
                            <select
                                value={selectedLevel}
                                onChange={(e) => setSelectedLevel(e.target.value)}
                                className="w-full bg-slate-800 text-white px-4 py-3 rounded-lg outline-none border border-slate-700 focus:border-blue-500"
                            >
                                <option value="">Choose a level...</option>
                                {levels.map((level, index) => (
                                    <option key={index} value={level}>{level}</option>
                                ))}
                            </select>
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={launchInterview}
                                disabled={!selectedDomain || !selectedLevel}
                                className="flex-1 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 text-white py-3 rounded-lg font-semibold transition-all"
                            >
                                Launch Interview
                            </button>
                            <button
                                onClick={() => setShowStartModal(false)}
                                className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-3 rounded-lg font-semibold transition-all"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;
