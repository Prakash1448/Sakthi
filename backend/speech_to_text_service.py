"""
=========================================
Speech-to-Text Service
AI Interview Platform
=========================================
"""

from groq_client import client
import os
import tempfile


def transcribe_audio(audio_file, audio_filename="audio.webm"):
    """
    Transcribe audio file using Groq Whisper API.
    
    Args:
        audio_file: File-like object containing audio data
        audio_filename: Original filename with extension
        
    Returns:
        dict: Transcription result with text and metadata
    """
    
    try:
        # Determine file extension
        file_ext = os.path.splitext(audio_filename)[1].lower()
        
        # Supported formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
        supported_formats = ['.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.wav', '.webm']
        
        if file_ext not in supported_formats:
            return {
                "success": False,
                "error": f"Unsupported audio format: {file_ext}. Supported: {', '.join(supported_formats)}"
            }
        
        # Create temporary file with proper extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            # Write audio data to temp file
            audio_file.seek(0)
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name
        
        try:
            # Open temp file and send to Groq
            with open(temp_file_path, "rb") as audio:
                transcription = client.audio.transcriptions.create(
                    file=(audio_filename, audio),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    temperature=0.0
                )
            
            # Extract transcribed text
            transcribed_text = transcription.text.strip()
            
            if not transcribed_text:
                return {
                    "success": False,
                    "error": "Transcription returned empty text. Please record a valid answer."
                }
            
            return {
                "success": True,
                "text": transcribed_text,
                "language": getattr(transcription, 'language', None)
            }
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass
                
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific error cases
        if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
            return {
                "success": False,
                "error": "Authentication failed. Please check Groq API key."
            }
        elif "rate limit" in error_msg.lower():
            return {
                "success": False,
                "error": "Rate limit exceeded. Please try again in a moment."
            }
        elif "timeout" in error_msg.lower():
            return {
                "success": False,
                "error": "Transcription request timed out. Please try again."
            }
        else:
            return {
                "success": False,
                "error": f"Transcription failed: {error_msg}"
            }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":
    
    print("=" * 60)
    print("Speech-to-Text Service - Test")
    print("=" * 60)
    
    # This is for manual testing with an actual audio file
    test_audio_path = "test_audio.wav"
    
    if os.path.exists(test_audio_path):
        with open(test_audio_path, "rb") as audio_file:
            result = transcribe_audio(audio_file, test_audio_path)
            print("\nTranscription Result:")
            print(result)
    else:
        print(f"\nTest audio file not found: {test_audio_path}")
        print("To test, provide a valid audio file.")
