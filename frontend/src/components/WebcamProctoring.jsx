import { useEffect, useRef, useState } from "react";
import { FaVideo, FaVideoSlash, FaExclamationTriangle } from "react-icons/fa";

/**
 * WebcamProctoring Component
 * 
 * Monitors candidate behavior during interview using webcam.
 * Detects violations and manages 10-warning system.
 */
function WebcamProctoring({ sessionId, onTerminate }) {
    
    // State
    const [cameraActive, setCameraActive] = useState(false);
    const [cameraError, setCameraError] = useState("");
    const [faceDetected, setFaceDetected] = useState(false);
    const [warningCount, setWarningCount] = useState(0);
    const [currentWarning, setCurrentWarning] = useState(null);
    const [monitoringStatus, setMonitoringStatus] = useState("initializing");
    const [faceCount, setFaceCount] = useState(0);
    
    // Refs
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const overlayCanvasRef = useRef(null); // New canvas for face box overlay
    const streamRef = useRef(null);
    const detectionIntervalRef = useRef(null);
    const lastViolationTypeRef = useRef(null);
    const violationStartTimeRef = useRef(null);
    const lastProcessTimeRef = useRef(0);
    
    // Configuration - STRICT SECURITY
    const DETECTION_INTERVAL = 200; // Check every 200ms (faster detection)
    const PROCESS_THROTTLE = 300; // Send to backend every 300ms (more frequent)
    const MAX_WARNINGS = 10;
    
    // Refs for tab switch detection
    const visibilityChangeCountRef = useRef(0);
    const lastTabSwitchTimeRef = useRef(0);
    const tabSwitchProcessedRef = useRef(false);
    
    /**
     * Initialize webcam
     */
    const initializeCamera = async () => {
        try {
            setCameraError("");
            
            // Request webcam permission
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
            setMonitoringStatus("active");
            
            // Start detection loop
            startDetection();
            
        } catch (error) {
            console.error("Camera initialization error:", error);
            
            if (error.name === 'NotAllowedError') {
                setCameraError("Camera permission denied. Please allow camera access.");
            } else if (error.name === 'NotFoundError') {
                setCameraError("No camera found. Please connect a webcam.");
            } else {
                setCameraError("Failed to access camera: " + error.message);
            }
            
            setCameraActive(false);
            setMonitoringStatus("error");
        }
    };
    
    /**
     * Start face detection loop
     */
    const startDetection = () => {
        detectionIntervalRef.current = setInterval(() => {
            detectFaceAndViolations();
        }, DETECTION_INTERVAL);
    };
    
    /**
     * Detect face and potential violations
     * Uses simple heuristics based on video feed analysis
     * Draws RED BOX around detected face area
     */
    const detectFaceAndViolations = () => {
        if (!videoRef.current || !canvasRef.current || !overlayCanvasRef.current) return;
        
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const overlayCanvas = overlayCanvasRef.current;
        const ctx = canvas.getContext('2d');
        const overlayCtx = overlayCanvas.getContext('2d');
        
        // Set canvas size to match video
        if (canvas.width !== video.videoWidth) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            overlayCanvas.width = video.videoWidth;
            overlayCanvas.height = video.videoHeight;
        }
        
        // Draw current video frame
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get image data for analysis
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        
        // Analyze frame for face detection
        const detection = analyzeFrameWithBoundingBox(imageData, canvas.width, canvas.height);
        
        // Clear overlay canvas
        overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
        
        // Draw face detection box
        if (detection.face_detected && detection.boundingBox) {
            const box = detection.boundingBox;
            
            // Draw RED BOX around face
            overlayCtx.strokeStyle = '#FF0000'; // Red color
            overlayCtx.lineWidth = 3;
            overlayCtx.strokeRect(box.x, box.y, box.width, box.height);
            
            // Add label
            overlayCtx.fillStyle = '#FF0000';
            overlayCtx.font = '14px Arial';
            overlayCtx.fillText('Face Detected', box.x, box.y - 5);
        } else {
            // Draw RED BOX indicating "NO FACE" - covering center area
            const boxWidth = canvas.width * 0.5;
            const boxHeight = canvas.height * 0.6;
            const boxX = (canvas.width - boxWidth) / 2;
            const boxY = (canvas.height - boxHeight) / 2;
            
            overlayCtx.strokeStyle = '#FF0000'; // Red color
            overlayCtx.lineWidth = 3;
            overlayCtx.setLineDash([10, 5]); // Dashed line for empty box
            overlayCtx.strokeRect(boxX, boxY, boxWidth, boxHeight);
            overlayCtx.setLineDash([]); // Reset dash
            
            // Add warning text
            overlayCtx.fillStyle = '#FF0000';
            overlayCtx.font = 'bold 16px Arial';
            overlayCtx.fillText('⚠️ NO FACE DETECTED', boxX + 10, boxY + 30);
        }
        
        // Update UI state
        setFaceDetected(detection.face_detected);
        setFaceCount(detection.face_count);
        
        // Process violation with backend (throttled)
        const now = Date.now();
        if (now - lastProcessTimeRef.current >= PROCESS_THROTTLE) {
            processDetectionResult(detection);
            lastProcessTimeRef.current = now;
        }
    };
    
    /**
     * Analyze video frame for face detection
     * STRICT VERSION: Only reports violations when VERY CONFIDENT
     * Returns bounding box coordinates for face
     */
    const analyzeFrameWithBoundingBox = (imageData, width, height) => {
        const { data } = imageData;
        
        // Calculate average brightness and color distribution
        let totalBrightness = 0;
        let skinTonePixels = 0;
        let totalPixels = data.length / 4;
        
        // Track bounds of skin-tone pixels for bounding box
        let minX = width, maxX = 0, minY = height, maxY = 0;
        let skinPixelCount = 0;
        
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const idx = (y * width + x) * 4;
                const r = data[idx];
                const g = data[idx + 1];
                const b = data[idx + 2];
                
                const brightness = (r + g + b) / 3;
                totalBrightness += brightness;
                
                // Simple skin tone detection (rough heuristic)
                if (r > 95 && g > 40 && b > 20 && 
                    r > g && r > b && 
                    Math.abs(r - g) > 15) {
                    skinTonePixels++;
                    skinPixelCount++;
                    
                    // Update bounding box
                    if (x < minX) minX = x;
                    if (x > maxX) maxX = x;
                    if (y < minY) minY = y;
                    if (y > maxY) maxY = y;
                }
            }
        }
        
        const avgBrightness = totalBrightness / totalPixels;
        const skinToneRatio = skinTonePixels / totalPixels;
        
        // VERY STRICT face detection to avoid false negatives
        // If there's any reasonable skin tone detected, consider face present
        const face_detected = skinToneRatio > 0.02 && avgBrightness > 15 && skinPixelCount > 1000;
        
        // Calculate bounding box (with padding)
        let boundingBox = null;
        if (face_detected && skinPixelCount > 1000) {
            const padding = 20;
            boundingBox = {
                x: Math.max(0, minX - padding),
                y: Math.max(0, minY - padding),
                width: Math.min(width, maxX - minX + 2 * padding),
                height: Math.min(height, maxY - minY + 2 * padding)
            };
        }
        
        // DEFAULT: No violation (be conservative)
        let violation_type = null;
        let confidence = 0.0;
        let face_count = face_detected ? 1 : 0;
        
        // ONLY report violations with VERY HIGH confidence
        if (!face_detected && skinToneRatio < 0.01 && avgBrightness < 30) {
            // Face is CLEARLY absent - very dark or empty frame
            violation_type = "face_absent";
            confidence = 0.95;  // Very high confidence
            face_count = 0;
        } else if (skinToneRatio > 0.25) {
            // VERY HIGH skin tone ratio - likely multiple faces
            violation_type = "multiple_faces";
            confidence = 0.90;  // High confidence
            face_count = 2;
        }
        // ELSE: Face appears to be present - NO violation
        
        return {
            face_detected,
            face_count,
            violation_type,
            confidence,
            boundingBox
        };
    };
    
    /**
     * Send detection result to backend for processing
     */
    const processDetectionResult = async (detection) => {
        if (!sessionId) return;
        
        try {
            const eventId = `detection_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            const response = await fetch('http://127.0.0.1:8000/proctoring/process-event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    face_detected: detection.face_detected,
                    face_count: detection.face_count,
                    violation_type: detection.violation_type,
                    confidence: detection.confidence,
                    timestamp: Date.now() / 1000,
                    event_id: eventId
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                setWarningCount(result.warning_count);
                setMonitoringStatus(result.monitoring_status);
                
                if (result.warning_issued) {
                    setCurrentWarning(result.warning_message);
                    
                    // Auto-hide warning after 5 seconds (unless terminated)
                    if (!result.should_terminate) {
                        setTimeout(() => {
                            setCurrentWarning(null);
                        }, 5000);
                    }
                }
                
                if (result.should_terminate) {
                    handleTermination(result.warning_message);
                }
            }
        } catch (error) {
            console.error("Error processing detection:", error);
        }
    };
    
    /**
     * Handle interview termination
     */
    const handleTermination = (message) => {
        // Stop detection
        if (detectionIntervalRef.current) {
            clearInterval(detectionIntervalRef.current);
        }
        
        setMonitoringStatus("terminated");
        setCurrentWarning(message);
        
        // Notify parent component
        if (onTerminate) {
            onTerminate(message);
        }
    };
    
    /**
     * Stop camera
     */
    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
        }
        
        if (detectionIntervalRef.current) {
            clearInterval(detectionIntervalRef.current);
        }
        
        setCameraActive(false);
        setMonitoringStatus("stopped");
    };
    
    /**
     * Initialize on mount
     */
    useEffect(() => {
        initializeCamera();
        
        // Setup tab switch detection
        setupTabSwitchDetection();
        
        return () => {
            stopCamera();
            cleanupTabSwitchDetection();
        };
    }, []);
    
    /**
     * Setup browser tab switch/visibility detection
     */
    const setupTabSwitchDetection = () => {
        // Primary: visibilitychange event
        document.addEventListener('visibilitychange', handleVisibilityChange);
        
        // Supporting: window focus/blur
        window.addEventListener('blur', handleWindowBlur);
        window.addEventListener('focus', handleWindowFocus);
    };
    
    /**
     * Cleanup tab switch detection
     */
    const cleanupTabSwitchDetection = () => {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
        window.removeEventListener('blur', handleWindowBlur);
        window.removeEventListener('focus', handleWindowFocus);
    };
    
    /**
     * Handle visibility change (primary tab switch detection)
     */
    const handleVisibilityChange = () => {
        if (document.hidden) {
            // Tab switched away or browser minimized
            const now = Date.now();
            
            // Prevent duplicate penalties within 2 seconds
            if (now - lastTabSwitchTimeRef.current > 2000) {
                lastTabSwitchTimeRef.current = now;
                processTabSwitch(now);
            }
        } else {
            // Tab returned to focus
            tabSwitchProcessedRef.current = false;
        }
    };
    
    /**
     * Handle window blur (supporting signal)
     */
    const handleWindowBlur = () => {
        // Blur alone is ambiguous, but combined with visibility change provides confirmation
        // We rely on visibilitychange as primary signal
    };
    
    /**
     * Handle window focus (supporting signal)
     */
    const handleWindowFocus = () => {
        // Reset processed flag when window regains focus
        tabSwitchProcessedRef.current = false;
    };
    
    /**
     * Process tab switch penalty
     */
    const processTabSwitch = async (timestamp) => {
        if (!sessionId || tabSwitchProcessedRef.current) return;
        
        tabSwitchProcessedRef.current = true;
        visibilityChangeCountRef.current += 1;
        
        try {
            const eventId = `tab_switch_${timestamp}_${visibilityChangeCountRef.current}`;
            
            const response = await fetch('http://127.0.0.1:8000/proctoring/tab-switch', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    event_type: 'tab_switch',
                    event_id: eventId,
                    timestamp: timestamp / 1000
                })
            });
            
            const result = await response.json();
            
            if (result.success && result.penalty_applied) {
                setWarningCount(result.warning_count);
                setMonitoringStatus(result.monitoring_status);
                
                if (result.warning_message) {
                    setCurrentWarning(result.warning_message);
                    
                    // Don't auto-hide tab switch warnings
                    if (!result.should_terminate) {
                        setTimeout(() => {
                            setCurrentWarning(null);
                        }, 10000);  // Show for 10 seconds
                    }
                }
                
                if (result.should_terminate) {
                    handleTermination(result.warning_message);
                }
            }
        } catch (error) {
            console.error("Error processing tab switch:", error);
        }
    };
    
    /**
     * Initialize on mount
     */
    useEffect(() => {
        initializeCamera();
        
        return () => {
            stopCamera();
        };
    }, []);
    
    /**
     * Get status indicator color
     */
    const getStatusColor = () => {
        if (monitoringStatus === "normal") return "bg-green-500";
        if (monitoringStatus === "potential_violation") return "bg-yellow-500";
        if (monitoringStatus === "terminated") return "bg-red-500";
        return "bg-gray-500";
    };
    
    /**
     * Get warning color based on count
     */
    const getWarningColor = () => {
        if (warningCount === 0) return "text-green-400";
        if (warningCount < 5) return "text-yellow-400";
        if (warningCount < 9) return "text-orange-400";
        return "text-red-400";
    };
    
    return (
        <div className="fixed top-4 right-4 z-50">
            
            {/* Camera Preview */}
            <div className="bg-slate-900 rounded-lg p-3 shadow-xl border border-slate-700">
                
                {/* Video Feed with Overlay */}
                <div className="relative">
                    <video
                        ref={videoRef}
                        className="w-48 h-36 bg-black rounded object-cover"
                        autoPlay
                        muted
                        playsInline
                    />
                    <canvas
                        ref={canvasRef}
                        className="hidden"
                    />
                    {/* Overlay canvas for face detection box */}
                    <canvas
                        ref={overlayCanvasRef}
                        className="absolute top-0 left-0 w-48 h-36 pointer-events-none"
                    />
                    
                    {/* Status Indicators */}
                    <div className="absolute top-2 left-2 flex gap-2">
                        <div className={`${getStatusColor()} w-3 h-3 rounded-full animate-pulse`} />
                        {cameraActive ? (
                            <FaVideo className="text-white text-sm" />
                        ) : (
                            <FaVideoSlash className="text-red-400 text-sm" />
                        )}
                    </div>
                    
                    {/* Face Detection Indicator */}
                    {cameraActive && (
                        <div className="absolute top-2 right-2">
                            {faceDetected ? (
                                <div className="bg-green-500 text-white text-xs px-2 py-1 rounded">
                                    Face OK
                                </div>
                            ) : (
                                <div className="bg-red-500 text-white text-xs px-2 py-1 rounded">
                                    No Face
                                </div>
                            )}
                        </div>
                    )}
                </div>
                
                {/* Status Info */}
                <div className="mt-2 text-xs space-y-1">
                    <div className="flex justify-between">
                        <span className="text-gray-400">Camera:</span>
                        <span className={cameraActive ? "text-green-400" : "text-red-400"}>
                            {cameraActive ? "Active" : "Inactive"}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Status:</span>
                        <span className="text-white capitalize">
                            {monitoringStatus.replace("_", " ")}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Warnings:</span>
                        <span className={`font-bold ${getWarningColor()}`}>
                            {warningCount}/{MAX_WARNINGS}
                        </span>
                    </div>
                </div>
                
                {/* Camera Error */}
                {cameraError && (
                    <div className="mt-2 bg-red-900/50 border border-red-500 text-red-200 text-xs p-2 rounded">
                        {cameraError}
                        <button
                            onClick={initializeCamera}
                            className="ml-2 underline"
                        >
                            Retry
                        </button>
                    </div>
                )}
            </div>
            
            {/* Warning Modal */}
            {currentWarning && (
                <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
                    <div className="bg-slate-900 border border-red-500 rounded-xl p-8 max-w-md mx-4">
                        <div className="flex items-center gap-3 mb-4">
                            <FaExclamationTriangle className="text-red-500 text-3xl" />
                            <h2 className="text-2xl font-bold text-red-400">
                                Monitoring Alert
                            </h2>
                        </div>
                        <div className="text-white whitespace-pre-line">
                            {currentWarning}
                        </div>
                        {monitoringStatus !== "terminated" && (
                            <button
                                onClick={() => setCurrentWarning(null)}
                                className="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg"
                            >
                                I Understand
                            </button>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default WebcamProctoring;
