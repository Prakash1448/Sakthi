# 🚀 AI Interview Platform - Level 1

> An AI-powered Interview Platform that automatically generates technical interview questions, reference answers, evaluates candidate responses using Large Language Models (LLMs), and provides intelligent feedback with an overall performance score.

---

## 📌 Overview

The AI Interview Platform simulates a real technical interview experience by:

- 🎯 Generating interview questions
- 📖 Creating reference answers
- 🤖 Evaluating candidate responses using AI
- 📊 Calculating overall interview score
- 💡 Providing strengths, weaknesses, and recommendations

---

# ✨ Features

✅ AI Question Generation

✅ AI Reference Answer Generation

✅ AI Answer Evaluation

✅ Overall Interview Score

✅ Detailed Feedback

✅ Multi-Level Interview

✅ FastAPI REST APIs

✅ Swagger API Documentation

✅ React + Vite Frontend

✅ Render Deployment

---

# 🛠 Tech Stack

## 🎨 Frontend

- React.js
- Vite
- Axios
- CSS

---

## ⚙ Backend

- FastAPI
- Python
- Groq API
- Large Language Model (LLM)

---

## 🤖 AI Model

Current Model

```
Llama 3.1 8B Instant
```

Future Upgrade

```
Qwen2.5-7B-Instruct
```

---

# 🏗 System Architecture

```text
             React Frontend
                    │
                    ▼
            Axios HTTP Requests
                    │
                    ▼
             FastAPI Backend
                    │
                    ▼
              Groq Cloud API
                    │
                    ▼
          Large Language Model
                    │
                    ▼
     Question • Answer • Evaluation
```

---

# 🔄 Project Workflow

```text
Select Interview Level
          │
          ▼
Generate Interview Questions
          │
          ▼
Generate Reference Answers
          │
          ▼
Candidate Answers Questions
          │
          ▼
AI Evaluates Answers
          │
          ▼
Detailed Feedback
          │
          ▼
Overall Interview Score
```

---

# 📂 Project Structure

```text
AI_Interview_Level1
│
├── backend
│   ├── api
│   ├── main.py
│   ├── question_generation.py
│   ├── reference_generation.py
│   ├── evaluation_service.py
│   ├── submit_service.py
│   └── ...
│
├── frontend
│   ├── src
│   ├── public
│   └── ...
│
└── README.md
```

---

# 🌐 Live Demo

## 🎨 Frontend

https://ai-interview-frontend-k3fe.onrender.com

---

## ⚙ Backend

https://ai-interview-level1.onrender.com

---

# 📚 Swagger API Documentation

Open Swagger UI

```
https://ai-interview-level1.onrender.com/docs
```

Use Swagger to test all backend APIs directly.

---

# 🔗 Available APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Home API |
| GET | `/health` | Health Check |
| POST | `/generate-questions` | Generate Interview Questions |
| POST | `/generate-reference-answers` | Generate Reference Answers |
| POST | `/start-interview` | Start Interview |
| POST | `/evaluate-answer` | Evaluate Candidate Answer |
| POST | `/submit-interview` | Submit Complete Interview |

---

# 🧪 API Testing

The backend APIs can be tested using:

✅ Swagger UI

or

✅ Postman

Swagger URL

```
https://ai-interview-level1.onrender.com/docs
```

---

# 💻 Local Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/AI-Interview-Level1.git
```

---

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

Backend runs on

```
http://127.0.0.1:8000
```

---

# 📸 Screens

- 🏠 Home Page
- 🎯 Interview Page
- 🤖 AI Evaluation
- 📊 Result Dashboard
- 📚 Swagger Documentation

---

# 🚀 Deployment

| Service | Platform |
|----------|----------|
| Frontend | Render Static Site |
| Backend | Render Web Service |

---

# 🔮 Future Enhancements

- 🚀 Qwen2.5-7B Integration
- 🎙 Voice Interview
- 🔊 Text-to-Speech
- 🎤 Speech-to-Text
- 📄 Resume-based Questions
- 🌐 Multi-Domain Interviews
- 📈 Analytics Dashboard
- 📊 Performance Charts
- 🧠 Adaptive AI Interviews
- 📥 PDF Report Generation

---

# 👨‍💻 Developer

**Prakash J**

🎓 B.E. Computer Science and Engineering

🏫 Sri Krishna College of Engineering and Technology

🤖 AI Developer Intern

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub!

---

## ❤️ Thank You
