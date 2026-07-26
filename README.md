# 🤖 AI Interview Platform - Level 1 (Question Generation & Evaluation)

## 📌 Project Overview

This project is the **Level 1 module** of an AI-powered Interview Platform.

The objective of this module is to conduct a **technical interview** by:

* Generating interview questions using **Qwen 2.5-7B-Instruct**
* Generating ideal reference answers
* Accepting candidate responses
* Evaluating candidate answers using semantic similarity (MiniLM)
* Calculating the final interview score
* Deciding whether the candidate is eligible to proceed to the next interview level

This project is designed as a modular pipeline so it can be easily integrated into a larger AI Interview System.

---

# 🎯 Current Features

* ✅ Level 1 Question Generation
* ✅ Reference Answer Generation
* ✅ Candidate Answer Collection
* ✅ Semantic Evaluation (MiniLM)
* ✅ Question-wise Score
* ✅ Final Level Score
* ✅ PASS / FAIL Decision

---

# 🧠 AI Models Used

### Interview Question Generation

* Qwen 2.5-7B-Instruct

### Reference Answer Generation

* Qwen 2.5-7B-Instruct

### Semantic Evaluation

* all-MiniLM-L6-v2

---

# 📂 Project Structure

```
AI_Interview_Level1/

│
├── src/
│   ├── model_loader.py
│   ├── config.py
│   ├── question_generation.py
│   ├── reference_generation.py
│   ├── evaluation.py
│   ├── report.py
│   └── main.py
│
├── notebook/
│   └── AI_Interview_Level1.ipynb
│
├── outputs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Workflow

```
Start

↓

Load Qwen Model

↓

Generate Level 1 Questions

↓

Generate Reference Answers

↓

Candidate Answers Questions

↓

MiniLM Semantic Evaluation

↓

Calculate Individual Scores

↓

Calculate Average Score

↓

PASS / FAIL

↓

Generate Final Report
```

---

# 📊 Evaluation Method

Each candidate answer is compared with the reference answer using sentence embeddings.

Pipeline:

```
Reference Answer
        │
        ▼
Sentence Embedding
        │
Candidate Answer
        │
        ▼
Sentence Embedding
        │
        ▼
Cosine Similarity
        │
        ▼
Score (0–10)
```

---

# 📈 Interview Report

The generated report contains:

* Question
* Reference Answer
* Candidate Answer
* Question Score
* Final Average Score
* PASS / FAIL Status
* Recommendation

---

# 🚀 Future Enhancements

This module is part of a larger AI Interview Platform.

Upcoming features include:

* 🎤 Voice-to-Voice Interview
* 🗣️ Speech-to-Text
* 🔊 AI Voice Response
* 😊 Emotion Detection
* 👁️ Eye Contact Analysis
* 📹 Webcam Monitoring
* 🧠 Adaptive Question Generation
* 📄 PDF Interview Report
* 📊 Recruiter Dashboard
* 🔗 RAG-based Knowledge Integration

---

# 🛠️ Technologies Used

* Python
* PyTorch
* Transformers
* Hugging Face
* Sentence Transformers
* Scikit-learn
* NumPy

---

# ▶️ How to Run

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

---

# 👨‍💻 Author

**Prakash J**

AI Engineer

AI Interview Platform Development

---

# 📄 License

This project is intended for educational, research, and internship purposes.
"# AI-Interview-Level1" 
