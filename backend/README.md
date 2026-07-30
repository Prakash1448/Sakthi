# 🤖 AI Interview Platform - Level-Based Interview Engine

An AI-powered interview engine built using **Qwen 2.5 7B** for generating interview questions, reference answers, evaluating candidate responses, and automatically progressing through multiple interview levels.

---

## 🚀 Features

- 🎯 Domain-specific interview generation
- 📚 Level-based interview system
- 🤖 Qwen 2.5 7B Question Generation
- ✅ AI-generated Reference Answers
- 📊 Semantic Evaluation using MiniLM
- 📈 Automatic Score Calculation
- 📄 Interview Report Generation
- 🔄 Automatic Level Progression

---

## 📂 Project Structure

```
AI_Interview_System/

│── main.py
│── config.py
│── model_loader.py
│── interview_engine.py
│── question_generation.py
│── reference_generation.py
│── evaluation.py
│── report.py

│── requirements.txt
│── README.md
│── .gitignore
```

---

## 📚 Interview Flow

```
Start Interview
        │
        ▼
Level 1 - Fundamentals
        │
Generate Questions
        │
Generate Reference Answers
        │
Candidate Answers
        │
MiniLM Evaluation
        │
Generate Report
        │
PASS?
   ┌────┴────┐
   │         │
 YES         NO
   │         │
   ▼         ▼
Level 2   Repeat Level
   │
   ▼
Level 3
   │
   ▼
Interview Completed
```

---

## 🧠 Technologies Used

- Python 3.10+
- Qwen 2.5 7B Instruct
- Hugging Face Transformers
- Sentence Transformers
- MiniLM (all-MiniLM-L6-v2)
- Scikit-Learn
- PyTorch

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-System.git

cd AI-Interview-System
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Project

```bash
python main.py
```

---

## 📋 Interview Levels

### Level 1

- Fundamentals
- Definitions
- Basic Concepts
- Real-world Examples

---

### Level 2

- Concept Application
- Practical Scenarios
- Comparisons
- Usage-Based Questions

---

### Level 3

- Problem Solving
- Design Thinking
- Optimization
- Analytical Questions

---

## 📊 Evaluation

Candidate answers are evaluated using:

- MiniLM Sentence Embeddings
- Cosine Similarity
- Score out of 10

Average score determines whether the candidate progresses to the next interview level.

---

## 📈 Future Enhancements

- 🎤 Voice-to-Voice Interview
- 🗣️ Speech-to-Text Integration
- 🔊 Text-to-Speech Interviewer
- 😊 Emotion Detection
- 👀 Eye Contact Monitoring
- 📹 Webcam Proctoring
- 🧠 AI Technical Evaluation using Qwen
- 📊 Skill-wise Scoring
- ☁️ Database Integration
- 🌐 Web Interface

---

## 👨‍💻 Developed By

**Tech Jayam**

AI Interview Platform

Built using Qwen 2.5 7B and Hugging Face Transformers.

---