import { useState, useRef, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { FaVideo, FaVideoSlash, FaCheckCircle } from "react-icons/fa";

/**
 * Camera Setup and Consent Page
 * 
 * Allows candidate to test camera and understand monitoring rules
 * before starting the proctored interview.
 */
function CameraSetup() {
    const navigate = useNavigate();
    const location = useLocation();
    const interviewData = location.state;
    
    const [cameraActive, setCameraActive] = useState(false);
    const [cameraError, setCameraError] = useState("");
    const [consentGiven, setConsentGiven] = useState(false);
    const [faceVisible, setFaceVisible] = useState(false);
    
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const checkIntervalRef = useRef(null);
    
    /**
     * Initialize camera
     */
    const initializeCamera = async () => {
        try {
            setCameraError("");
            
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: "user"
                }
            });
            
            streamRef.current = stream;
            
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            }
            
            setCameraActive(true);
            
            // Start basic face visibility check
            startFaceCheck();
            
        } catch (error) {
            console.error("Camera error:", error);
            
            if (error.name === 'NotAllowedError') {
                setCameraError("Camera permission denied. Please allow camera access to continue.");
            } else if (error.name === 'NotFoundError') {
                setCameraError("No camera found. Please connect a webcam to continue.");
            } else {
                setCameraError("Failed to access camera: " + error.message);
            }
            
            setCameraActive(false);
        }
    };
    
    /**
     * Simple face visibility check
     */
    const startFaceCheck = () => {
        checkIntervalRef.current = setInterval(() => {
            if (videoRef.current && videoRef.current.readyState === 4) {
                // Simple check: if video is playing and has content, assume face might be visible
                const canvas = document.createElement('canvas');
                canvas.width = 160;
                canvas.height = 120;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(videoRef.current, 0, 0, 160, 120);
                
                const imageData = ctx.getImageData(0, 0, 160, 120);
                let brightness = 0;
                
                for (let i = 0; i < imageData.data.length; i += 4) {
                    brightness += (imageData.data[i] + imageData.data[i + 1] + imageData.data[i + 2]) / 3;
                }
                
                brightness /= (imageData.data.length / 4);
                
                // Simple heuristic: if average brightness is reasonable, face might be visible
                setFaceVisible(brightness > 30 && brightness < 220);
            }
        }, 1000);
    };
    
    /**
     * Stop camera
     */
    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
        }
        
        if (checkIntervalRef.current) {
            clearInterval(checkIntervalRef.current);
        }
        
        setCameraActive(false);
    };
    
    /**
     * Start interview with proctoring
     */
    const startInterview = () => {
        if (!cameraActive) {
            alert("Please enable your camera before starting the interview.");
            return;
        }
        
        if (!consentGiven) {
            alert("Please read and accept the monitoring consent to continue.");
            return;
        }
        
        // Camera will be reinitialized by WebcamProctoring component
        stopCamera();
        
        navigate("/interview", { state: interviewData });
    };
    
    /**
     * Initialize on mount
     */
    useEffect(() => {
        if (!interviewData) {
            navigate("/");
            return;
        }
        
        initializeCamera();
        
        return () => {
            stopCamera();
        };
    }, []);
    
    if (!interviewData) {
        return null;
    }
    
    return (
        <div className="min-h-screen bg-slate-950 p-6 flex items-center justify-center">
            <div className="max-w-4xl w-full bg-slate-900 rounded-2xl shadow-2xl p-8">
                
                <h1 className="text-3xl font-bold text-blue-400 mb-2">
                    Camera Setup & Monitoring Consent
                </h1>
                
                <p className="text-gray-400 mb-8">
                    Before starting your interview, please test your camera and review the monitoring rules.
                </p>
                
                <div className="grid md:grid-cols-2 gap-8">
                    
                    {/* Camera Preview */}
                    <div>
                        <h2 className="text-xl text-white font-semibold mb-4">
                            Camera Preview
                        </h2>
                        
                        <div className="relative bg-black rounded-lg overflow-hidden">
                            <video
                                ref={videoRef}
                                className="w-full h-64 object-cover"
                                autoPlay
                                muted
                                playsInline
                            />
                            
                            {/* Status Indicator */}
                            <div className="absolute top-4 left-4 flex items-center gap-2">
                                {cameraActive ? (
                                    <>
                                        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                                        <FaVideo className="text-white" />
                                        <span className="text-white text-sm">Camera Active</span>
                                    </>
                                ) : (
                                    <>
                                        <FaVideoSlash className="text-red-400" />
                                        <span className="text-red-400 text-sm">Camera Inactive</span>
                                    </>
                                )}
                            </div>
                            
                            {/* Face Detection Indicator */}
                            {cameraActive && (
                                <div className="absolute top-4 right-4">
                                    {faceVisible ? (
                                        <div className="bg-green-500 text-white px-3 py-1 rounded-full text-sm flex items-center gap-2">
                                            <FaCheckCircle />
                                            Face Visible
                                        </div>
                                    ) : (
                                        <div className="bg-red-500 text-white px-3 py-1 rounded-full text-sm">
                                            Face Not Detected
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                        
                        {/* Camera Error */}
                        {cameraError && (
                            <div className="mt-4 bg-red-900/50 border border-red-500 text-red-200 p-3 rounded-lg">
                                {cameraError}
                                <button
                                    onClick={initializeCamera}
                                    className="ml-2 underline hover:text-white"
                                >
                                    Retry
                                </button>
                            </div>
                        )}
                        
                        {/* Camera Tips */}
                        <div className="mt-4 bg-blue-900/30 border border-blue-500 p-4 rounded-lg">
                            <h3 className="text-blue-300 font-semibold mb-2">Camera Tips:</h3>
                            <ul className="text-gray-300 text-sm space-y-1">
                                <li>• Ensure your face is well-lit and clearly visible</li>
                                <li>• Position camera at eye level</li>
                                <li>• Remove any obstructions</li>
                                <li>• Ensure you're the only person in frame</li>
                            </ul>
                        </div>
                    </div>
                    
                    {/* Monitoring Rules & Consent */}
                    <div>
                        <h2 className="text-xl text-white font-semibold mb-4">
                            Monitoring Rules
                        </h2>
                        
                        <div className="bg-slate-800 rounded-lg p-4 mb-4 max-h-96 overflow-y-auto">
                            <div className="text-gray-300 space-y-3 text-sm">
                                <div>
                                    <h3 className="text-yellow-400 font-semibold mb-1">What We Monitor:</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• Camera must remain active throughout the interview</li>
                                        <li>• Your face must be clearly visible at all times</li>
                                        <li>• Looking away for extended periods</li>
                                        <li>• Face absence or obstruction</li>
                                        <li>• Multiple faces in the camera frame</li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <h3 className="text-orange-400 font-semibold mb-1">Warning System (STRICT):</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• <strong>1 SECOND</strong> violation threshold (very strict)</li>
                                        <li>• Any violation lasting 1+ seconds will issue a warning</li>
                                        <li>• You can receive up to <strong>10 warnings total</strong></li>
                                        <li>• <strong>Browser tab switch: immediate +3 warnings</strong></li>
                                        <li>• After 10 warnings, your interview will end pending review</li>
                                        <li>• Warning counter persists throughout all interview levels</li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <h3 className="text-green-400 font-semibold mb-1">Allowed Behavior:</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• Normal blinking</li>
                                        <li>• Very brief glances (under 1 second)</li>
                                        <li>• Minor head movements</li>
                                        <li>• Reading questions on screen</li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <h3 className="text-red-400 font-semibold mb-1">⚠️ Critical Violations:</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• <strong>Tab switching: +3 warnings immediately</strong></li>
                                        <li>• Browser minimization: +3 warnings</li>
                                        <li>• Face absent for 1+ second: +1 warning</li>
                                        <li>• Looking away for 1+ second: +1 warning</li>
                                        <li>• Multiple faces: +1 warning</li>
                                        <li>• <strong>Stay focused on the interview tab</strong></li>
                                    </ul>
                                </div>
                                
                                <div>
                                    <h3 className="text-red-400 font-semibold mb-1">Camera Issues:</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• If your camera disconnects, the interview will pause</li>
                                        <li>• Reconnect your camera to continue</li>
                                        <li>• Hardware failures are recorded separately</li>
                                        <li>• Not automatically treated as violations</li>
                                    </ul>
                                </div>
                                
                                <div className="pt-2 border-t border-slate-600">
                                    <h3 className="text-purple-400 font-semibold mb-1">Privacy:</h3>
                                    <ul className="ml-4 space-y-1">
                                        <li>• We do not record or store video footage</li>
                                        <li>• Only monitoring events and timestamps are logged</li>
                                        <li>• No biometric data is collected</li>
                                        <li>• Data used only for interview integrity</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        
                        {/* Consent Checkbox */}
                        <label className="flex items-start gap-3 cursor-pointer">
                            <input
                                type="checkbox"
                                checked={consentGiven}
                                onChange={(e) => setConsentGiven(e.target.checked)}
                                className="mt-1 w-5 h-5"
                            />
                            <span className="text-gray-300 text-sm">
                                I have read and understood the monitoring rules. I consent to webcam monitoring 
                                during this interview and understand that sustained violations will result in warnings 
                                and potential session termination pending review.
                            </span>
                        </label>
                        
                        {/* Start Button */}
                        <button
                            onClick={startInterview}
                            disabled={!cameraActive || !consentGiven}
                            className="w-full mt-6 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-700 disabled:cursor-not-allowed text-white py-4 rounded-lg text-lg font-semibold transition"
                        >
                            {!cameraActive
                                ? "Waiting for Camera..."
                                : !consentGiven
                                ? "Please Accept Consent"
                                : "Start Proctored Interview"}
                        </button>
                        
                        <button
                            onClick={() => navigate("/")}
                            className="w-full mt-3 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg transition"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CameraSetup;
