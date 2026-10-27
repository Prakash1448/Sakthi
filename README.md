# 🎯 AI Interview Platform - Complete Documentation

> **Intelligent AI-Powered Technical Interview System with Real-time Proctoring, Speech-to-Text, and Comprehensive Reporting**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com/)

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Tech Stack](#-tech-stack)
4. [Architecture](#-architecture)
5. [AI/LLM Integration](#-aillm-integration)
6. [Installation](#-installation)
7. [Configuration](#-configuration)
8. [Usage Guide](#-usage-guide)
9. [API Documentation](#-api-documentation)
10. [Database Schema](#-database-schema)
11. [Project Structure](#-project-structure)
12. [Advanced Features](#-advanced-features)
13. [Troubleshooting](#-troubleshooting)
14. [Future Enhancements](#-future-enhancements)
15. [Contributing](#-contributing)
16. [License](#-license)

---

## 🌟 Overview

The **AI Interview Platform** is a cutting-edge, full-stack application that revolutionizes the technical interview process using artificial intelligence. It conducts intelligent interviews across 15 technical domains, evaluates candidate responses using LLM-powered analysis, monitors candidates with real-time webcam proctoring, and generates professional PDF reports with visual analytics.

### Why This Platform?

- **🤖 AI-Powered**: Leverages Groq's high-speed LLM for question generation, answer evaluation, and feedback
- **👁️ Real-time Monitoring**: Advanced webcam proctoring with face detection and violation tracking
- **🎤 Voice Input**: Speech-to-text capability using Groq Whisper for hands-free responses
- **📊 Visual Analytics**: Professional PDF reports with charts (gauge, bar, pie, radar)
- **🎓 Multi-Level**: Three progressive difficulty levels from basics to behavioral + AI knowledge
- **🌐 15 Domains**: Comprehensive coverage across modern tech stacks

---

## ✨ Key Features

### 🎯 Core Interview Features
- ✅ **Domain-Specific Questions**: 15 technical domains with tailored questions
- ✅ **Three-Level System**: 
  - Level 1: Basic Fundamentals (definitions, concepts)
  - Level 2: Coding Logic (problem-solving approach)
  - Level 3: HR & AI Knowledge (behavioral + modern tech)
- ✅ **AI-Powered Evaluation**: Real-time answer scoring with detailed feedback
- ✅ **Dynamic Question Generation**: Context-aware questions based on domain and level
- ✅ **Reference Answer Generation**: AI-generated model answers for comparison

### 🎤 Speech & Input Features
- ✅ **Speech-to-Text**: Groq Whisper integration for voice responses
- ✅ **Real-time Audio Monitoring**: Visual audio level meter
- ✅ **Web Audio API**: Reliable recording with 3x volume boost
- ✅ **Multi-format Support**: WAV, WebM, MP3, OGG audio formats
- ✅ **Transcript Review**: Preview and confirm before submission

### 👁️ Proctoring Features
- ✅ **Face Detection**: Real-time facial recognition with bounding box overlay
- ✅ **Multiple Face Detection**: Alerts when multiple people detected
- ✅ **Tab Switching Detection**: Monitors window focus changes
- ✅ **Camera Disconnect Alerts**: Tracks camera connection status
- ✅ **Violation Scoring System**: Progressive warnings and auto-termination
- ✅ **Visual Feedback**: Red bounding box (solid when face present, dashed when absent)

### 📊 Reporting & Analytics
- ✅ **Enhanced Dashboard**: Real-time performance overview
- ✅ **PDF Reports with Charts**: 
  - Performance Gauge (speedometer)
  - Bar Chart (level comparison)
  - Pie Chart (completion rate)
  - Radar Chart (multi-dimensional analysis)
- ✅ **User Tracking**: Complete interview history per user
- ✅ **Performance Metrics**: Scores, completion rate, warnings, statistics
- ✅ **Downloadable Reports**: One-click PDF generation

### 💾 Data Management
- ✅ **MongoDB Integration**: Persistent user data and session tracking
- ✅ **Session Management**: Complete interview lifecycle tracking
- ✅ **Answer Storage**: Q&A pairs with evaluations
- ✅ **Proctoring Logs**: Detailed violation tracking
- ✅ **Progress Tracking**: Multi-level journey per user

---

## 🛠️ Tech Stack

### Frontend
```
React 18.x          - Modern UI framework
Vite 4.x           - Lightning-fast build tool
React Router 6.x   - Client-side routing
Axios              - HTTP client
TailwindCSS        - Utility-first CSS framework
React Icons        - Icon library
Web Audio API      - Audio recording
MediaDevices API   - Camera/microphone access
Canvas API         - Face detection overlay
```

### Backend
```
Python 3.8+        - Programming language
FastAPI 0.100+     - Modern async web framework
Uvicorn            - ASGI server
Pydantic           - Data validation
Python-Multipart   - File upload support
Python-dotenv      - Environment management
```

### AI/LLM Stack
```
Groq Cloud         - High-speed LLM inference
Llama 3.1 70B      - Question generation & evaluation
Whisper Large V3   - Speech-to-text transcription
```

### Database
```
MongoDB 6.0+       - NoSQL document database
PyMongo            - Python MongoDB driver
```

### Computer Vision
```
OpenCV (cv2)       - Face detection
MediaPipe          - Alternative face detection (optional)
```

### PDF Generation
```
ReportLab          - PDF creation
Matplotlib         - Chart generation
NumPy              - Numerical operations
Pillow (PIL)       - Image processing
```

### Development Tools
```
Git                - Version control
VS Code            - IDE
Postman            - API testing
MongoDB Compass    - Database GUI
```

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  ┌────────────┐  ┌──────────┐  ┌─────────────┐            │
│  │   Home     │  │Dashboard │  │  Interview  │            │
│  └─────┬──────┘  └────┬─────┘  └──────┬──────┘            │
│        │              │                │                    │
│        └──────────────┴────────────────┘                    │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │ REST API (Axios)
┌───────────────────────┼──────────────────────────────────────┐
│                       │         BACKEND (FastAPI)            │
│  ┌────────────────────▼───────────────────────────────────┐ │
│  │              API Routes Layer                          │ │
│  │  /start-interview  /transcribe-audio  /submit         │ │
│  └────────┬─────────────┬─────────────────┬──────────────┘ │
│           │             │                 │                 │
│  ┌────────▼────────┐ ┌─▼────────────┐ ┌─▼──────────────┐  │
│  │  Interview      │ │  Speech      │ │  Proctoring    │  │
│  │  Service        │ │  Service     │ │  Service       │  │
│  └────────┬────────┘ └─┬────────────┘ └─┬──────────────┘  │
│           │             │                 │                 │
│  ┌────────▼─────────────▼─────────────────▼──────────────┐ │
│  │              Core Services Layer                       │ │
│  │  • Question Generation  • Answer Evaluation           │ │
│  │  • Reference Generation • Report Generation           │ │
│  └────────┬────────────────────────────┬─────────────────┘ │
└───────────┼────────────────────────────┼────────────────────┘
            │                            │
    ┌───────▼──────────┐        ┌───────▼────────┐
    │   Groq Cloud     │        │   MongoDB      │
    │  • Llama 3.1 70B │        │  • users       │
    │  • Whisper V3    │        │  • sessions    │
    └──────────────────┘        │  • answers     │
                                │  • proctoring  │
                                └────────────────┘
```

### Data Flow

```
1. User Interaction Flow:
   Home → Camera Setup → Interview → Result → Dashboard

2. Interview Flow:
   Start Interview → Generate Questions → Display Q&A
   → Record Answer (Text/Voice) → Evaluate → Next Question
   → Submit → Generate Report → Show Results

3. Proctoring Flow:
   Camera Access → Face Detection → Violation Detection
   → Warning System → Session Termination (if severe)

4. Data Persistence Flow:
   User Action → API Call → Service Layer → Database
   → Response → Frontend Update
```

---

## 🤖 AI/LLM Integration

### Groq Cloud Platform

**Why Groq?**
- ⚡ **Ultra-Fast Inference**: 500+ tokens/second (10x faster than standard LLMs)
- 💰 **Cost-Effective**: Competitive pricing for high-volume usage
- 🎯 **Low Latency**: Sub-second response times
- 🔒 **Reliable**: Enterprise-grade uptime and stability

### LLM Models Used

#### 1. **Llama 3.1 70B Versatile**
```python
Model: "llama-3.1-70b-versatile"
Use Cases:
  - Question Generation (10 questions per interview)
  - Answer Evaluation (scoring + detailed feedback)
  - Reference Answer Generation
  
Temperature: 0.7 (Questions), 0.0 (Evaluation)
Max Tokens: 1000 (Questions), 500 (Evaluation)

Why Llama 3.1 70B?
✓ Superior reasoning capabilities
✓ Domain-specific knowledge across 15 tech areas
✓ Excellent at structured output generation
✓ Consistent evaluation metrics
```

#### 2. **Whisper Large V3 Turbo**
```python
Model: "whisper-large-v3-turbo"
Use Cases:
  - Speech-to-Text transcription
  - Audio file processing (WAV, MP3, WebM, OGG)
  
Supported Formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm
Max File Size: 25MB
Language: Auto-detect (supports 99+ languages)

Why Whisper V3 Turbo?
✓ State-of-the-art accuracy
✓ Fast transcription (real-time processing)
✓ Robust against background noise
✓ Multi-language support
```

### AI Prompt Engineering

#### Question Generation Prompt Structure
```python
# Level 1 - Basic Fundamentals
f"""
You are an experienced Technical Interviewer.
Generate EXACTLY 10 basic fundamental questions.

Domain: {selected_domain}

FOCUS:
- Definition-based questions
- Basic concepts and terminology
- "What is..." type questions
- Questions MUST be specifically about {selected_domain}

Rules:
1. Return ONLY questions (numbered 1-10)
2. No answers generated
3. Domain-specific terminology
4. Suitable for beginners
"""

# Level 2 - Coding Logic
f"""
Generate EXACTLY 10 coding logic questions.

Domain: {selected_domain}

FOCUS:
- Logic explanation (NOT actual code)
- "How would you..." approach questions
- Problem-solving strategy
- Questions MUST be about {selected_domain}

Rules:
1. Ask for LOGIC/APPROACH, not code syntax
2. Focus on problem-solving methodology
3. Candidate explains thinking process
"""

# Level 3 - HR & AI Knowledge
f"""
Generate EXACTLY 10 questions (5 HR + 5 AI).

Domain Context: {selected_domain}

HR BEHAVIORAL (5 questions):
- Teamwork in {selected_domain} projects
- Handling deadlines
- Career goals in {selected_domain}

AI & MODERN TECH (5 questions):
- AI tools usage (ChatGPT, Copilot)
- How AI helps in {selected_domain}
- Modern development practices
"""
```

#### Answer Evaluation Prompt
```python
f"""
You are an Expert Technical Interviewer.

Question: {question}
Reference Answer: {reference_answer}
Candidate Answer: {candidate_answer}

Evaluate the candidate's answer:

1. Correctness Score (0-100)
2. Detailed Feedback (3-5 sentences)

Return JSON:
{{
  "correctness_score": <0-100>,
  "feedback": "<detailed feedback>",
  "strengths": ["point1", "point2"],
  "improvements": ["suggestion1", "suggestion2"]
}}

Be fair but thorough in evaluation.
"""
```

### LLM Configuration

```python
# config.py
GROQ_API_KEY = "gsk_..."  # From .env file
MODEL_NAME = "llama-3.1-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"

# Temperature Settings
QUESTION_TEMPERATURE = 0.7    # Creativity for questions
EVALUATION_TEMPERATURE = 0.0  # Consistency for scoring

# Token Limits
QUESTION_MAX_TOKENS = 1000   # ~10 questions
EVALUATION_MAX_TOKENS = 500  # Detailed feedback
REFERENCE_MAX_TOKENS = 800   # Reference answers

# Timeout Settings
LLM_TIMEOUT = 30 seconds
WHISPER_TIMEOUT = 30 seconds
```

### API Rate Limits

```
Groq Free Tier:
- 30 requests per minute
- 14,400 requests per day
- Shared across all models

Optimization Strategies:
✓ Batch question generation (10 at once)
✓ Cache reference answers
✓ Async processing where possible
✓ Request queuing for high traffic
```

---

## 📦 Installation

### Prerequisites

```bash
# Required Software
- Python 3.8 or higher
- Node.js 16.x or higher
- MongoDB 6.0+ (optional but recommended)
- Git

# Accounts Needed
- Groq Cloud Account (Free tier available)
  Sign up: https://console.groq.com/

# Operating System
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)
```

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/AI-Interview-Level1.git
cd AI-Interview-Level1
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Additional packages for full features
pip install matplotlib scipy  # For PDF charts
```

**requirements.txt includes:**
```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
groq>=0.4.0
python-dotenv>=1.0.0
python-multipart>=0.0.6
pymongo>=4.5.0
reportlab>=4.0.0
pillow>=10.0.0
matplotlib>=3.7.0
scipy>=1.11.0
numpy>=1.24.0
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend
cd ../frontend

# Install Node dependencies
npm install

# Dependencies installed:
# - react
# - react-dom
# - react-router-dom
# - axios
# - react-icons
# - tailwindcss
# - vite
```

### Step 4: Environment Configuration

Create `.env` file in project root:

```bash
# .env file
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# MongoDB Configuration (Optional)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=ai_interview_platform

# Server Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=5173

# AI Model Configuration
MODEL_NAME=llama-3.1-70b-versatile
WHISPER_MODEL=whisper-large-v3-turbo

# Feature Flags
ENABLE_PROCTORING=true
ENABLE_SPEECH_TO_TEXT=true
ENABLE_PDF_REPORTS=true
```

**Get Your Groq API Key:**
1. Go to https://console.groq.com/
2. Sign up (free tier available)
3. Navigate to API Keys section
4. Create new API key
5. Copy and paste into `.env` file

### Step 5: MongoDB Setup (Optional)

**Option A: Local MongoDB**
```bash
# Download MongoDB Community Edition
# https://www.mongodb.com/try/download/community

# Install and start MongoDB service
# Windows: MongoDB service starts automatically
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# Verify MongoDB is running
# Open MongoDB Compass or:
mongosh
```

**Option B: MongoDB Atlas (Cloud)**
```bash
# 1. Go to https://www.mongodb.com/cloud/atlas
# 2. Create free cluster
# 3. Get connection string
# 4. Update .env:
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

**Option C: Run Without MongoDB**
- Platform works without MongoDB
- Features disabled: Dashboard, PDF reports, progress tracking
- Interview still functions normally

---

## ⚙️ Configuration

### Backend Configuration

**config.py**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM Models
MODEL_NAME = "llama-3.1-70b-versatile"
WHISPER_MODEL = "whisper-large-v3-turbo"

# Default Domain (fallback)
DOMAIN = "Python Programming"

# Temperature Settings
QUESTION_TEMPERATURE = 0.7    # Creative questions
EVALUATION_TEMPERATURE = 0.0  # Consistent scoring

# Token Limits
QUESTION_MAX_TOKENS = 1000
EVALUATION_MAX_TOKENS = 500
REFERENCE_MAX_TOKENS = 800

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "ai_interview_platform")

# Server Settings
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173"
]
```

### Frontend Configuration

**vite.config.js**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

**src/services/api.js**
```javascript
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default api;
```

### Domain Configuration

**15 Available Domains:**
```javascript
const domains = [
    "Python Programming",
    "Data Structures & Algorithms",
    "Machine Learning & AI",
    "Web Development - Frontend",
    "Web Development - Backend",
    "Full Stack Development",
    "React.js & Modern Frontend",
    "Node.js & Express",
    "Database & SQL",
    "Cloud Computing (AWS/Azure/GCP)",
    "DevOps & CI/CD",
    "Data Science & Analytics",
    "Cybersecurity",
    "Mobile App Development",
    "RAG & LLM Applications"
];
```

### Proctoring Configuration

**proctoring_service.py**
```python
# Violation Thresholds
MAX_WARNINGS = 5              # Auto-terminate after 5 warnings
FACE_ABSENCE_THRESHOLD = 3.0  # Seconds before warning
MULTIPLE_FACES_LIMIT = 1      # Alert if > 1 face detected
TAB_SWITCH_PENALTY = 2        # Warning points per switch
CAMERA_DISCONNECT_PENALTY = 3 # Warning points per disconnect

# Face Detection Settings
FACE_DETECTION_CONFIDENCE = 0.85  # Minimum confidence threshold
DETECTION_INTERVAL = 1.0          # Check every 1 second
```

---

## 🚀 Usage Guide

### Starting the Application

#### Method 1: Manual Start

```bash
# Terminal 1 - Start Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Start Frontend
cd frontend
npm run dev

# Access Application
Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

#### Method 2: Quick Start (Windows)

```bash
# Double-click START_BACKEND.bat
# Or run:
.\START_BACKEND.bat

# In another terminal:
cd frontend
npm run dev
```

### User Journey

#### 1. **Home Page** (`/`)
```
┌─────────────────────────────────────┐
│    AI Interview Platform            │
│                                     │
│  Name: [Enter name]                 │
│  Domain: [Select domain ▼]          │
│  Level: [Select level ▼]            │
│                                     │
│  [Start Interview]                  │
│  [📊 View Dashboard]                │
└─────────────────────────────────────┘
```

**Actions:**
- Enter candidate name
- Select from 15 technical domains
- Choose difficulty level (1-3)
- Start interview or view dashboard

#### 2. **Camera Setup** (`/camera-setup`)
```
┌─────────────────────────────────────┐
│   Camera & Microphone Setup         │
│                                     │
│  ┌─────────────────────┐           │
│  │                     │           │
│  │   [Camera Feed]     │           │
│  │                     │           │
│  └─────────────────────┘           │
│                                     │
│  ✓ Camera detected                  │
│  ✓ Microphone detected              │
│                                     │
│  [Continue to Interview]            │
└─────────────────────────────────────┘
```

**Actions:**
- Grant camera/microphone permissions
- Verify devices working
- System checks proctoring capabilities
- Proceed to interview

#### 3. **Interview Page** (`/interview`)
```
┌─────────────────────────────────────┐
│  Question 3/10                      │
│                                     │
│  Q: What is a closure in            │
│     JavaScript?                     │
│                                     │
│  [🎤 Record] Audio: ███░░░ 15%     │
│                                     │
│  Answer:                            │
│  ┌───────────────────────────┐     │
│  │                           │     │
│  │  [Type or record answer]  │     │
│  │                           │     │
│  └───────────────────────────┘     │
│                                     │
│  [Previous]         [Next]          │
└─────────────────────────────────────┘

[Webcam View with Red Box]
```

**Features:**
- 10 questions per interview
- Type or speak answers
- Real-time audio level meter
- Face detection with bounding box
- Previous/Next navigation
- Submit when complete

#### 4. **Result Page** (`/result`)
```
┌─────────────────────────────────────┐
│       Interview Result              │
│                                     │
│  Overall Score: 75%                 │
│  ████████████░░░░░                  │
│                                     │
│  Question 1: ✓ 8/10                 │
│  Feedback: Good understanding...    │
│                                     │
│  Question 2: ✓ 7/10                 │
│  Feedback: Correct approach...      │
│                                     │
│  [Start New Interview]              │
│  [📊 View Dashboard]                │
└─────────────────────────────────────┘
```

**Displays:**
- Overall percentage score
- Individual question scores
- AI-generated feedback
- Strengths and improvements
- Navigation options

#### 5. **Dashboard** (`/dashboard`)
```
┌─────────────────────────────────────┐
│  John's Dashboard                   │
│  [Start Interview] [Download PDF]   │
│                                     │
│  🏆 7.5  📄 3   ✓ 93%  ⚠ 2         │
│  Score   Sessions Complete Warnings │
│                                     │
│  Level Performance:                 │
│  L1: ████████░░ 8.0/10             │
│  L2: ██████░░░░ 6.5/10             │
│  L3: ███████░░░ 7.0/10             │
│                                     │
│  [View Detailed Reports]            │
└─────────────────────────────────────┘
```

**Features:**
- Performance overview
- Statistics cards
- Level-wise breakdown
- Download PDF reports
- Start new interviews

### Speech-to-Text Usage

```
1. Click "🎤 Start Recording"
2. Speak clearly for 2+ seconds
3. Watch audio level meter (target: 10-30%)
4. Click "⏹️ Stop Recording"
5. Review transcript preview
6. Click "✓ Confirm" or "🔄 Retry"
```

**Tips for Best Results:**
- Speak 6-12 inches from microphone
- Reduce background noise
- Speak at normal pace
- Use clear pronunciation
- Check audio level meter stays green/yellow

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Start Interview
```http
POST /start-interview
Content-Type: application/json

{
  "difficulty": "Level 1 - Basic Fundamentals",
  "domain": "React.js & Modern Frontend"
}

Response:
{
  "difficulty": "Level 1 - Basic Fundamentals",
  "questions": ["Q1", "Q2", ...],
  "reference_answers": ["A1", "A2", ...]
}
```

#### 2. Transcribe Audio
```http
POST /transcribe-audio
Content-Type: multipart/form-data

Form Data:
- audio: [audio file]

Response:
{
  "success": true,
  "text": "Transcribed text here",
  "language": "en"
}
```

#### 3. Submit Interview
```http
POST /submit-interview
Content-Type: application/json

{
  "questions": ["Q1", "Q2", ...],
  "reference_answers": ["A1", "A2", ...],
  "candidate_answers": ["Answer1", "Answer2", ...]
}

Response:
{
  "overall_score": 75.5,
  "results": [
    {
      "question": "...",
      "candidate_answer": "...",
      "evaluation": {
        "correctness_score": 80,
        "feedback": "..."
      }
    }
  ]
}
```

#### 4. Create Proctoring Session
```http
POST /proctoring/create-session

Response:
{
  "success": true,
  "session_id": "abc123..."
}
```

#### 5. Monitor Event
```http
POST /proctoring/monitor
Content-Type: application/json

{
  "session_id": "abc123",
  "face_detected": true,
  "face_count": 1,
  "confidence": 0.95,
  "timestamp": 1234567890.123
}

Response:
{
  "success": true,
  "status": "normal",
  "warning_count": 0,
  "should_continue": true
}
```

#### 6. Download Report
```http
GET /reports/user/{username}/pdf

Response:
[PDF File Download]
```

#### 7. Get User Report Data
```http
GET /reports/user/{username}

Response:
{
  "success": true,
  "data": {
    "user": {...},
    "sessions": [...],
    "level_data": {...},
    "statistics": {...}
  }
}
```

### Interactive API Docs

FastAPI provides interactive documentation:

**Swagger UI:**
```
http://localhost:8000/docs
```

**ReDoc:**
```
http://localhost:8000/redoc
```

---

## 💾 Database Schema

### MongoDB Collections

#### 1. **users** Collection
```javascript
{
  _id: ObjectId("..."),
  username: "John Doe",
  domain: "Python Programming",
  email: "john@example.com",  // optional
  created_at: ISODate("2024-01-01T00:00:00Z"),
  updated_at: ISODate("2024-01-01T00:00:00Z"),
  completed_levels: [
    "Level 1 - Basic Fundamentals",
    "Level 2 - Coding Logic"
  ],
  average_score: 7.5,
  total_sessions: 5
}
```

#### 2. **sessions** Collection
```javascript
{
  _id: ObjectId("..."),
  session_id: "uuid-1234-5678",
  username: "John Doe",
  domain: "Python Programming",
  level: "Level 1 - Basic Fundamentals",
  status: "completed",  // in_progress, completed, terminated
  
  questions: [
    "What is a variable in Python?",
    "What is the difference between..."
  ],
  
  reference_answers: ["Answer 1", "Answer 2", ...],
  
  candidate_answers: ["My answer 1", "My answer 2", ...],
  
  evaluations: [
    {
      score: 8.0,
      feedback: "Good understanding...",
      strengths: ["Clear explanation"],
      improvements: ["Could add examples"]
    }
  ],
  
  total_score: 7.5,
  percentage: 75.0,
  
  proctoring_session_id: "proc-uuid-...",
  proctoring_warnings: 2,
  
  started_at: ISODate("2024-01-01T10:00:00Z"),
  completed_at: ISODate("2024-01-01T10:30:00Z"),
  duration_minutes: 30
}
```

#### 3. **answers** Collection
```javascript
{
  _id: ObjectId("..."),
  session_id: "uuid-1234-5678",
  username: "John Doe",
  question_index: 0,
  
  question: "What is a variable in Python?",
  reference_answer: "A variable is...",
  candidate_answer: "In Python, a variable is...",
  
  evaluation: {
    score: 8.0,
    feedback: "Excellent explanation...",
    correctness_score: 80,
    strengths: ["Clear", "Accurate"],
    improvements: ["Add examples"]
  },
  
  answered_at: ISODate("2024-01-01T10:05:00Z"),
  time_taken_seconds: 120,
  input_method: "text"  // or "speech"
}
```

#### 4. **proctoring_events** Collection
```javascript
{
  _id: ObjectId("..."),
  session_id: "proc-uuid-...",
  username: "John Doe",
  
  event_type: "face_detection",  // face_detection, tab_switch, camera_disconnect
  
  timestamp: ISODate("2024-01-01T10:05:30Z"),
  
  // For face_detection events
  face_detected: true,
  face_count: 1,
  confidence: 0.95,
  violation_type: null,  // "no_face", "multiple_faces", null
  
  // For tab_switch events
  switch_count: 1,
  
  // For camera events
  camera_status: "connected",  // connected, disconnected
  
  warning_issued: false,
  warning_message: null,
  
  penalty_points: 0
}
```

### Indexes

```javascript
// Optimize query performance
db.users.createIndex({ username: 1 }, { unique: true })
db.users.createIndex({ created_at: -1 })

db.sessions.createIndex({ session_id: 1 }, { unique: true })
db.sessions.createIndex({ username: 1, started_at: -1 })
db.sessions.createIndex({ status: 1 })

db.answers.createIndex({ session_id: 1 })
db.answers.createIndex({ username: 1 })

db.proctoring_events.createIndex({ session_id: 1 })
db.proctoring_events.createIndex({ timestamp: -1 })
`

## 📁 Project Structure

```
AI-Interview-Level1/
│
├── backend/                          # FastAPI Backend
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                # API endpoints
│   │
│   ├── config.py                    # Configuration settings
│   ├── database.py                  # MongoDB operations
│   ├── groq_client.py              # Groq API client
│   │
│   ├── question_generation.py       # LLM question generation
│   ├── reference_generation.py      # Reference answer generation
│   ├── evaluation_service.py        # Answer evaluation
│   ├── interview_service.py         # Interview orchestration
│   │
│   ├── speech_to_text_service.py   # Whisper integration
│   ├── proctoring_service.py       # Face detection & monitoring
│   │
│   ├── pdf_report_generator.py     # Basic PDF generation
│   ├── pdf_report_generator_enhanced.py  # PDF with charts
│   │
│   ├── submit_service.py           # Interview submission
│   ├── main.py                     # FastAPI app entry
│   ├── requirements.txt            # Python dependencies
│   └── reports/                    # Generated PDF reports
│
├── frontend/                        # React Frontend
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   │
│   ├── src/
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   │
│   │   ├── components/
│   │   │   └── WebcamProctoring.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx           # Landing page
│   │   │   ├── CameraSetup.jsx    # Device verification
│   │   │   ├── Interview.jsx      # Main interview page
│   │   │   ├── Result.jsx         # Results display
│   │   │   └── Dashboard.jsx      # User dashboard
│   │   │
│   │   ├── services/
│   │   │   └── api.js             # Axios HTTP client
│   │   │
│   │   ├── App.jsx                # Main app component
│   │   ├── App.css                # Global styles
│   │   ├── main.jsx               # Entry point
│   │   └── index.css              # Tailwind imports
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .oxlintrc.json
│
├── notebook/
│   └── Level1_AI_Interview_Demo.ipynb.ipynb
│
├── .env                            # Environment variables
├── .gitignore
├── README.md                       # This file
│
├── DASHBOARD_README.md             # Dashboard documentation
├── DOMAIN_FIX_VERIFICATION.md     # Domain fix guide
├── INSTALLATION_GUIDE.txt          # Setup instructions
├── MICROPHONE_DIAGNOSTICS.md      # Audio troubleshooting
├── PDF_REPORT_SAMPLE.md           # PDF preview
├── QUICK_START_PDF.txt            # Quick start guide
│
├── START_BACKEND.bat              # Windows backend launcher
└── SETUP_PDF_REPORTS.bat          # PDF setup script
```

---

## 🎨 Advanced Features

### 1. **Adaptive Question Generation**

Questions adapt based on:
- Selected domain (15 options)
- Difficulty level (3 levels)
- Previous performance (future enhancement)

### 2. **Multi-Modal Answer Input**

Candidates can respond via:
- **Typing**: Traditional text input
- **Voice**: Speech-to-text transcription
- **Hybrid**: Switch between methods per question

### 3. **Real-Time Proctoring**

Advanced monitoring includes:
- Face detection with visual bounding box
- Multiple person detection
- Tab switching monitoring
- Camera disconnect tracking
- Progressive warning system
- Auto-termination on severe violations

### 4. **Intelligent Evaluation**

LLM-powered evaluation provides:
- Numerical score (0-100)
- Detailed feedback paragraph
- Identified strengths
- Improvement suggestions
- Comparison with reference answer

### 5. **Visual PDF Reports**

Professional reports include:
- **Performance Gauge**: Speedometer-style overall score
- **Bar Chart**: Level-wise score comparison
- **Pie Chart**: Question completion rate
- **Radar Chart**: Multi-dimensional analysis (3+ levels)
- **Tables**: Detailed statistics
- **Recommendations**: AI-generated career guidance

### 6. **Progress Tracking Dashboard**

Comprehensive user dashboard with:
- Performance overview cards
- Historical data visualization
- Level completion tracking
- Trend analysis (future)
- Downloadable reports

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Backend Won't Start

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment activated
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 2. Groq API Error

**Problem:** `Authentication failed`

**Solution:**
```bash
# Check .env file has correct API key
GROQ_API_KEY=gsk_your_actual_key_here

# Verify key at https://console.groq.com/
# Ensure no extra spaces or quotes
```

#### 3. MongoDB Connection Failed

**Problem:** `ServerSelectionTimeoutError`

**Solution:**
```bash
# Check MongoDB running:
mongosh  # Should connect

# If not installed, platform works without MongoDB
# Or update .env with MongoDB Atlas URI
```

#### 4. Microphone Not Working

**Problem:** "Audio file too small" or "No audio detected"

**Solution:**
```
1. Check Windows microphone volume (90-100%)
2. Grant browser microphone permission
3. Watch audio level meter (should show 10-30%)
4. Speak louder and closer to mic
5. See MICROPHONE_DIAGNOSTICS.md for details
```

#### 5. Camera Permission Denied

**Problem:** "Camera access denied"

**Solution:**
```
1. Click lock icon in browser address bar
2. Allow camera and microphone
3. Refresh page
4. Check Windows Privacy Settings
   Settings → Privacy → Camera → Allow apps
```

#### 6. PDF Generation Fails

**Problem:** `ModuleNotFoundError: No module named 'matplotlib'`

**Solution:**
```bash
cd backend
pip install matplotlib scipy
# Or run: SETUP_PDF_REPORTS.bat
```

#### 7. Frontend Blank Page

**Problem:** White screen after `npm run dev`

**Solution:**
```bash
# Check console for errors (F12)
# Verify backend running
# Check CORS settings in backend config.py

# Try:
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### 8. Domain-Specific Questions Not Working

**Problem:** Always getting Python questions

**Solution:**
```bash
# Verify backend updated
# Restart backend completely
uvicorn main:app --reload

# Check browser console network tab
# Verify domain sent in request body
```

---

## 🚀 Future Enhancements

### Planned Features

#### Phase 1: Enhanced Intelligence
- [ ] **Adaptive Difficulty**: Adjust question difficulty based on performance
- [ ] **Follow-up Questions**: Generate contextual follow-ups
- [ ] **Code Execution**: Sandbox for coding questions
- [ ] **Multi-Language Support**: Interface in multiple languages

#### Phase 2: Advanced Analytics
- [ ] **Performance Trends**: Track improvement over time
- [ ] **Skill Gap Analysis**: Identify weak areas with recommendations
- [ ] **Benchmarking**: Compare against other candidates
- [ ] **Predictive Scoring**: ML model to predict job fit

#### Phase 3: Collaboration Features
- [ ] **Team Interviews**: Multi-interviewer support
- [ ] **Live Interview Mode**: Real-time with human interviewer
- [ ] **Interview Scheduling**: Calendar integration
- [ ] **Candidate Portal**: Self-service dashboard

#### Phase 4: Enterprise Features
- [ ] **Custom Question Banks**: Upload company-specific questions
- [ ] **White-Label Solution**: Customizable branding
- [ ] **SSO Integration**: Enterprise authentication
- [ ] **Advanced Reporting**: Custom report templates
- [ ] **API Access**: Integrate with ATS systems

#### Phase 5: AI Enhancements
- [ ] **Video Analysis**: Analyze candidate demeanor
- [ ] **Emotion Detection**: Gauge confidence and stress
- [ ] **Voice Analysis**: Assess communication skills
- [ ] **Multi-Modal LLMs**: GPT-4V, Gemini Pro Vision

### Technical Improvements

- [ ] **Caching Layer**: Redis for improved performance
- [ ] **Load Balancing**: Handle high traffic
- [ ] **Microservices**: Split into independent services
- [ ] **Real-time Updates**: WebSocket for live status
- [ ] **Mobile Apps**: Native iOS/Android applications
- [ ] **Offline Mode**: Continue interview without internet
- [ ] **Auto-Save**: Prevent data loss on disconnection
- [ ] **Video Recording**: Record entire interview session

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Getting Started

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/AI-Interview-Level1.git
cd AI-Interview-Level1
```

2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Make your changes**
- Follow existing code style
- Add comments for complex logic
- Update documentation

4. **Test thoroughly**
```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm test
```

5. **Commit your changes**
```bash
git add .
git commit -m "Add amazing feature"
```

6. **Push to your fork**
```bash
git push origin feature/amazing-feature
```

7. **Open a Pull Request**
- Describe your changes
- Reference any related issues
- Wait for review

### Coding Standards

**Python (Backend):**
- PEP 8 style guide
- Type hints where applicable
- Docstrings for functions
- Async/await for I/O operations

**JavaScript (Frontend):**
- ES6+ syntax
- Functional components with hooks
- PropTypes or TypeScript (future)
- Meaningful variable names

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌍 Translations
- ♿ Accessibility improvements

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 AI Interview Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support & Contact

### Get Help

- **Documentation**: Read this README thoroughly
- **Issues**: [GitHub Issues](https://github.com/yourusername/AI-Interview-Level1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AI-Interview-Level1/discussions)

### Report Bugs

When reporting bugs, include:
1. Operating system and version
2. Python and Node.js versions
3. Error messages (full stack trace)
4. Steps to reproduce
5. Expected vs actual behavior

### Feature Requests

Submit feature requests with:
1. Clear description of feature
2. Use case / problem it solves
3. Proposed implementation (optional)
4. Mockups or examples (optional)

---

## 🙏 Acknowledgments

### Technologies
- **Groq Cloud** - Ultra-fast LLM inference
- **Meta** - Llama 3.1 70B model
- **OpenAI** - Whisper speech recognition
- **FastAPI** - Modern Python web framework
- **React** - Frontend UI library
- **MongoDB** - NoSQL database
- **TailwindCSS** - Utility-first CSS
- **Vite** - Next-generation frontend tooling

### Inspiration
Built to address the need for:
- Scalable technical interviews
- Objective candidate evaluation
- Efficient recruitment processes
- AI-powered assessment tools

---

## 📊 Project Stats

```
Languages:
  Python        60%
  JavaScript    35%
  Other          5%

Lines of Code:
  Backend:      ~3,500 lines
  Frontend:     ~2,000 lines
  Total:        ~5,500 lines

Files:          45+
Components:     25+
API Endpoints:  15+
Database Collections: 4
```

---

## 🎯 Quick Links

- **Live Demo**: [Coming Soon]
- **Documentation**: [GitHub Wiki]
- **API Reference**: `http://localhost:8000/docs`
- **Roadmap**: [GitHub Projects]
- **Changelog**: [CHANGELOG.md]

---

## ⭐ Star the Project

If you find this project useful, please consider giving it a star on GitHub!

```
⭐ Star this repo to show your support!
```

---

**Built with ❤️ using AI and Modern Technologies**

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Status**: Active Development

---

## 📚 Additional Resources

### Learning Materials
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **React Documentation**: https://react.dev/
- **Groq Documentation**: https://console.groq.com/docs
- **MongoDB Guide**: https://www.mongodb.com/docs/

### Similar Projects
- [OpenAI Interview Assistant]
- [LangChain Interview Bot]
- [HuggingFace Interview Datasets]

### Related Technologies
- **LangChain**: LLM application framework
- **LlamaIndex**: Data framework for LLMs
- **Streamlit**: ML app framework
- **Gradio**: ML model interfaces

---

**Happy Interviewing! 🚀**

For questions or support, please open an issue on GitHub.
