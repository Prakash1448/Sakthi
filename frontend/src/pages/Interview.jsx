import { useLocation, useNavigate } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import api from "../services/api";
import { FaMicrophone, FaStop, FaRedo, FaCheck } from "react-icons/fa";
import WebcamProctoring from "../components/WebcamProctoring";

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
    
    // Speech-to-Text states
    const [isRecording, setIsRecording] = useState(false);
    const [isTranscribing, setIsTranscribing] = useState(false);
    const [transcript, setTranscript] = useState("");
    const [showTranscript, setShowTranscript] = useState(false);
    const [recordingError, setRecordingError] = useState("");
    const [recordingDuration, setRecordingDuration] = useState(0);
    
    // Proctoring states
    const [proctoringSessionId, setProctoringSessionId] = useState(null);
    const [interviewTerminated, setInterviewTerminated] = useState(false);
    const [terminationMessage, setTerminationMessage] = useState("");
    
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const recordingTimerRef = useRef(null);
    const audioContextRef = useRef(null);
    const mediaStreamRef = useRef(null);
    const scriptProcessorRef = useRef(null);
    const audioBuffersRef = useRef([]);
    const [audioLevel, setAudioLevel] = useState(0);
    const [isAudioDetected, setIsAudioDetected] = useState(false);
    
    /**
     * Initialize proctoring session on mount
     */
    useEffect(() => {
        const initProctoring = async () => {
            try {
                const response = await api.post('/proctoring/create-session');
                if (response.data.success) {
                    setProctoringSessionId(response.data.session_id);
                }
            } catch (error) {
                console.error("Failed to create proctoring session:", error);
            }
        };
        
        initProctoring();
    }, []);
    
    /**
     * Handle interview termination from proctoring
     */
    const handleProctoringTermination = (message) => {
        setInterviewTerminated(true);
        setTerminationMessage(message);
    };

    const updateAnswer = (value) => {

        const temp = [...answers];

        temp[currentQuestion] = value;

        setAnswers(temp);

    };

    const nextQuestion = () => {

        if (currentQuestion < interview.questions.length - 1) {

            setCurrentQuestion(currentQuestion + 1);
            
            // Reset speech states when moving to next question
            setTranscript("");
            setShowTranscript(false);
            setRecordingError("");

        }

    };

    const previousQuestion = () => {

        if (currentQuestion > 0) {

            setCurrentQuestion(currentQuestion - 1);
            
            // Reset speech states when moving to previous question
            setTranscript("");
            setShowTranscript(false);
            setRecordingError("");

        }

    };
    
    // NEW APPROACH: Use Web Audio API with ScriptProcessor to collect raw audio
    const startRecording = async () => {
        
        try {
            setRecordingError("");
            audioBuffersRef.current = [];
            
            console.log('=== Starting Web Audio API Recording ===');
            
            // Get microphone stream with specific constraints
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: false,  // Disable to preserve speech clarity
                    noiseSuppression: false,  // Disable to capture full voice
                    autoGainControl: true,    // Keep for volume boost
                    sampleRate: 16000,
                    channelCount: 1
                }
            });
            
            console.log('✓ Microphone stream obtained');
            mediaStreamRef.current = stream;
            
            // Create AudioContext
            const audioContext = new (window.AudioContext || window.webkitAudioContext)({
                sampleRate: 16000
            });
            audioContextRef.current = audioContext;
            console.log('✓ AudioContext created, sample rate:', audioContext.sampleRate);
            
            // Create source from stream
            const source = audioContext.createMediaStreamSource(stream);
            console.log('✓ Audio source created');
            
            // Create gain node to boost volume
            const gainNode = audioContext.createGain();
            gainNode.gain.value = 3.0; // Boost volume by 3x
            console.log('✓ Gain node created (boost: 3x)');
            
            // Create ScriptProcessor to capture raw audio
            const bufferSize = 4096;
            const processor = audioContext.createScriptProcessor(bufferSize, 1, 1);
            scriptProcessorRef.current = processor;
            
            processor.onaudioprocess = (e) => {
                const inputData = e.inputBuffer.getChannelData(0);
                // Clone the data to preserve it
                const buffer = new Float32Array(inputData);
                audioBuffersRef.current.push(buffer);
                
                // Calculate audio level (RMS)
                let sum = 0;
                for (let i = 0; i < inputData.length; i++) {
                    sum += inputData[i] * inputData[i];
                }
                const rms = Math.sqrt(sum / inputData.length);
                const level = Math.round(rms * 100);
                
                // Update audio level every 10 buffers (~0.6 seconds)
                if (audioBuffersRef.current.length % 10 === 0) {
                    setAudioLevel(level);
                    if (level > 1) {
                        setIsAudioDetected(true);
                    }
                }
                
                // Log every 50 buffers (~3 seconds at 4096 buffer size and 16000 sample rate)
                if (audioBuffersRef.current.length % 50 === 0) {
                    console.log(`Captured ${audioBuffersRef.current.length} buffers, total samples: ${audioBuffersRef.current.length * bufferSize}, audio level: ${level}%`);
                }
            };
            
            // Connect: source -> gain -> processor -> destination
            source.connect(gainNode);
            gainNode.connect(processor);
            processor.connect(audioContext.destination);
            
            console.log('✓ Audio pipeline connected (with gain boost)');
            
            setIsRecording(true);
            setRecordingDuration(0);
            setAudioLevel(0);
            setIsAudioDetected(false);
            
            // Start timer
            recordingTimerRef.current = setInterval(() => {
                setRecordingDuration(prev => prev + 1);
            }, 1000);
            
            console.log('✓✓✓ Recording started successfully ✓✓✓');
            
        } catch (error) {
            console.error("❌ Microphone error:", error);
            setRecordingError("Cannot access microphone: " + error.message);
        }
    };
    
    // Convert Float32Array buffers to WAV blob
    const buffersToWav = (buffers, sampleRate) => {
        
        console.log('=== Converting buffers to WAV ===');
        console.log('Buffers count:', buffers.length);
        
        if (buffers.length === 0) {
            console.error('❌ No buffers to convert');
            return null;
        }
        
        // Merge all buffers into one
        const totalLength = buffers.reduce((acc, buf) => acc + buf.length, 0);
        console.log('Total samples:', totalLength);
        
        const mergedBuffer = new Float32Array(totalLength);
        let offset = 0;
        for (const buffer of buffers) {
            mergedBuffer.set(buffer, offset);
            offset += buffer.length;
        }
        
        console.log('✓ Buffers merged');
        
        // Convert Float32 to Int16 PCM
        const int16Buffer = new Int16Array(mergedBuffer.length);
        for (let i = 0; i < mergedBuffer.length; i++) {
            const sample = Math.max(-1, Math.min(1, mergedBuffer[i]));
            int16Buffer[i] = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
        }
        
        console.log('✓ Converted to Int16 PCM');
        
        // Create WAV file
        const wavBuffer = new ArrayBuffer(44 + int16Buffer.length * 2);
        const view = new DataView(wavBuffer);
        
        // WAV header
        const writeString = (offset, string) => {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        };
        
        writeString(0, 'RIFF');
        view.setUint32(4, 36 + int16Buffer.length * 2, true);
        writeString(8, 'WAVE');
        writeString(12, 'fmt ');
        view.setUint32(16, 16, true); // fmt chunk size
        view.setUint16(20, 1, true); // PCM format
        view.setUint16(22, 1, true); // mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true); // byte rate
        view.setUint16(32, 2, true); // block align
        view.setUint16(34, 16, true); // bits per sample
        writeString(36, 'data');
        view.setUint32(40, int16Buffer.length * 2, true);
        
        // Copy PCM data
        const dataView = new Int16Array(wavBuffer, 44);
        dataView.set(int16Buffer);
        
        console.log('✓ WAV file created');
        console.log('WAV size:', wavBuffer.byteLength, 'bytes');
        
        return new Blob([wavBuffer], { type: 'audio/wav' });
    };
    
    // Stop recording and transcribe
    const stopRecording = async () => {
        
        if (!audioContextRef.current || !mediaStreamRef.current) {
            setRecordingError("No active recording");
            return;
        }
        
        console.log('=== Stopping Recording ===');
        
        // Stop timer
        if (recordingTimerRef.current) {
            clearInterval(recordingTimerRef.current);
            recordingTimerRef.current = null;
        }
        
        // Disconnect audio pipeline
        if (scriptProcessorRef.current) {
            scriptProcessorRef.current.disconnect();
            scriptProcessorRef.current.onaudioprocess = null;
        }
        
        // Stop media stream
        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(track => {
                console.log('Stopping track:', track.label);
                track.stop();
            });
        }
        
        // Close audio context
        if (audioContextRef.current) {
            await audioContextRef.current.close();
        }
        
        console.log('✓ Recording stopped');
        console.log('Total buffers captured:', audioBuffersRef.current.length);
        
        if (audioBuffersRef.current.length === 0) {
            setRecordingError("No audio captured. Please check microphone permissions.");
            setIsRecording(false);
            return;
        }
        
        // Convert buffers to WAV
        const audioBlob = buffersToWav(audioBuffersRef.current, 16000);
        
        if (!audioBlob || audioBlob.size < 1000) {
            console.error('❌ Audio too small:', audioBlob?.size || 0);
            setRecordingError(`Recording too short (${audioBlob?.size || 0} bytes). Please speak for at least 2 seconds.`);
            setIsRecording(false);
            return;
        }
        
        console.log('✓✓✓ Audio ready for transcription ✓✓✓');
        console.log('Final blob:', { size: audioBlob.size, type: audioBlob.type });
        
        // Transcribe
        setIsRecording(false);
        await transcribeAudio(audioBlob);
    };
    
    // Transcribe audio using backend API
    const transcribeAudio = async (audioBlob) => {
        
        try {
            setIsTranscribing(true);
            setRecordingError("");
            
            console.log('=== Transcribing Audio ===');
            console.log('Blob:', audioBlob.size, 'bytes', audioBlob.type);
            
            // Always use WAV since we're creating WAV files now
            const filename = 'recording.wav';
            
            console.log('Using filename:', filename);
            
            // Create FormData for file upload
            const formData = new FormData();
            formData.append('audio', audioBlob, filename);
            
            console.log('Sending to backend...');
            
            // Send to backend
            const response = await api.post('/transcribe-audio', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 30000 // 30 second timeout
            });
            
            console.log('Backend response:', response.data);
            
            if (response.data.success) {
                console.log('✓✓✓ Transcription successful! ✓✓✓');
                console.log('Text:', response.data.text);
                setTranscript(response.data.text);
                setShowTranscript(true);
            } else {
                console.error('❌ Transcription failed:', response.data.error);
                setRecordingError(response.data.error || "Transcription failed. Please try again.");
            }
            
        } catch (error) {
            console.error("❌ Transcription error:", error);
            if (error.response) {
                console.error('Error response:', error.response.data);
                setRecordingError(error.response.data.error || "Transcription failed.");
            } else if (error.request) {
                setRecordingError("Cannot reach server. Is backend running?");
            } else {
                setRecordingError("Failed to transcribe: " + error.message);
            }
        } finally {
            setIsTranscribing(false);
        }
    };
    
    // Retry recording
    const retryRecording = () => {
        setTranscript("");
        setShowTranscript(false);
        setRecordingError("");
    };
    
    // Confirm and use transcript
    const confirmTranscript = () => {
        updateAnswer(transcript);
        setShowTranscript(false);
        setTranscript("");
    };

    const submitInterview = async () => {
        
        // Check if interview was terminated
        if (interviewTerminated) {
            alert("Interview was terminated due to monitoring violations.");
            navigate("/");
            return;
        }

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
    
    // Show termination screen if interview was terminated
    if (interviewTerminated) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center">
                <div className="bg-slate-900 max-w-2xl rounded-xl p-10 shadow-xl border-2 border-red-500">
                    <h1 className="text-3xl font-bold text-red-400 mb-4">
                        Interview Session Ended
                    </h1>
                    <div className="text-white whitespace-pre-line text-lg">
                        {terminationMessage}
                    </div>
                    <button
                        onClick={() => navigate("/")}
                        className="mt-8 w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold"
                    >
                        Return to Home
                    </button>
                </div>
            </div>
        );
    }

    return (

        <div className="min-h-screen bg-slate-950 flex justify-center items-center">
            
            {/* Webcam Proctoring Component */}
            {proctoringSessionId && (
                <WebcamProctoring
                    sessionId={proctoringSessionId}
                    onTerminate={handleProctoringTermination}
                />
            )}

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
                    
                    {/* Speech-to-Text Controls */}
                    <div className="flex gap-3 mt-3 mb-3">
                        
                        {!isRecording && !showTranscript && (
                            <button
                                onClick={startRecording}
                                disabled={loading || isTranscribing}
                                className="bg-red-600 hover:bg-red-700 disabled:bg-gray-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                            >
                                <FaMicrophone /> Start Recording
                            </button>
                        )}
                        
                        {isRecording && (
                            <button
                                onClick={stopRecording}
                                className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 animate-pulse"
                            >
                                <FaStop /> Stop Recording ({recordingDuration}s)
                            </button>
                        )}
                        
                        {isRecording && (
                            <div className="flex items-center gap-3 px-4 py-2 bg-slate-800 rounded-lg">
                                <div className="text-white text-sm">Audio Level:</div>
                                <div className="w-48 h-3 bg-slate-700 rounded-full overflow-hidden">
                                    <div 
                                        className={`h-full transition-all duration-200 ${
                                            audioLevel > 5 ? 'bg-green-500' : 
                                            audioLevel > 2 ? 'bg-yellow-500' : 
                                            'bg-red-500'
                                        }`}
                                        style={{ width: `${Math.min(audioLevel * 2, 100)}%` }}
                                    />
                                </div>
                                <div className="text-white text-sm font-mono">{audioLevel}%</div>
                            </div>
                        )}
                        
                        {isRecording && !isAudioDetected && recordingDuration > 2 && (
                            <div className="text-yellow-400 text-sm px-4 py-2">
                                ⚠️ Low audio detected. Speak louder or check microphone!
                            </div>
                        )}
                        
                        {isTranscribing && (
                            <div className="text-blue-400 px-4 py-2">
                                Transcribing...
                            </div>
                        )}
                        
                        {showTranscript && (
                            <>
                                <button
                                    onClick={confirmTranscript}
                                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                                >
                                    <FaCheck /> Confirm Transcript
                                </button>
                                <button
                                    onClick={retryRecording}
                                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
                                >
                                    <FaRedo /> Retry Recording
                                </button>
                            </>
                        )}
                    </div>
                    
                    {/* Recording Error */}
                    {recordingError && (
                        <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-2 rounded-lg mb-3">
                            {recordingError}
                        </div>
                    )}
                    
                    {/* Transcript Preview */}
                    {showTranscript && (
                        <div className="bg-blue-900/30 border border-blue-500 rounded-lg p-4 mb-3">
                            <p className="text-sm text-blue-300 mb-2">Transcript (Review before confirming):</p>
                            <p className="text-white">{transcript}</p>
                        </div>
                    )}

                    <textarea

                        rows={8}

                        value={answers[currentQuestion]}

                        onChange={(e) => updateAnswer(e.target.value)}

                        placeholder="Type your answer here or use voice recording..."

                        className="w-full mt-3 bg-slate-800 rounded-xl p-5 text-white outline-none"

                    />

                </div>

                <div className="flex justify-between mt-10">

                    <button

                        onClick={previousQuestion}

                        disabled={currentQuestion === 0 || loading || isRecording || interviewTerminated}

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

                        disabled={loading || isRecording || isTranscribing || interviewTerminated}

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