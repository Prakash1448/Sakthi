"""
===========================================
Question Generation Module
AI Interview Platform
===========================================
"""

from groq_client import client

from config import (
    DOMAIN,
    MODEL_NAME,
    QUESTION_TEMPERATURE,
    QUESTION_MAX_TOKENS
)


def generate_questions(difficulty, domain=None):

    print("=" * 60)
    print(f"Generating {difficulty} Interview Questions for {domain or DOMAIN}...")
    print("=" * 60)
    
    # Use provided domain or fall back to config
    selected_domain = domain or DOMAIN

    # Three-level interview system with specific question types
    if difficulty == "Level 1 - Basic Fundamentals":
        prompt = f"""
You are an experienced Technical Interviewer conducting a LEVEL 1 Basic Interview.

Generate EXACTLY 10 basic fundamental questions.

Domain:
{selected_domain}

LEVEL 1 FOCUS:
- Definition-based questions
- Basic concepts and terminology
- Simple examples
- "What is..." type questions
- Core fundamentals understanding
- Questions MUST be specifically about {selected_domain}

Examples for Python:
- What is a variable in Python?
- What is the difference between a list and a tuple?
- What are the basic data types in Python?

Examples for React.js:
- What is JSX in React?
- What is the difference between props and state?
- What is the Virtual DOM?

Examples for Machine Learning:
- What is supervised learning?
- What is the difference between classification and regression?
- What is overfitting in machine learning?

Rules:
1. Return ONLY questions.
2. Number each question (1-10).
3. Do NOT generate answers.
4. Questions should test BASIC knowledge only about {selected_domain}.
5. No coding required - theoretical knowledge.
6. Suitable for complete beginners in {selected_domain}.
7. Focus on definitions and concepts specific to {selected_domain}.
"""
    
    elif difficulty == "Level 2 - Coding Logic":
        prompt = f"""
You are an experienced Technical Interviewer conducting a LEVEL 2 Coding Logic Interview.

Generate EXACTLY 10 coding logic questions.

Domain:
{selected_domain}

LEVEL 2 FOCUS:
- Logic explanation (NOT writing actual code)
- Algorithm approach questions
- Problem-solving strategy
- "How would you..." type questions
- Explain the logic/approach
- Pseudocode thinking
- Questions MUST be specifically about {selected_domain}

Examples for Python:
- How would you find the largest number in a list? Explain the logic.
- What approach would you use to remove duplicates from a list?
- Explain the logic to reverse a string without using built-in functions.

Examples for React.js:
- How would you handle form validation in React? Explain the approach.
- What approach would you use to optimize a React component that re-renders frequently?
- Explain the logic for implementing infinite scroll in React.

Examples for Database & SQL:
- How would you optimize a slow database query? Explain the approach.
- What strategy would you use to prevent SQL injection attacks?
- Explain the logic for designing a normalized database schema.

Rules:
1. Return ONLY questions.
2. Number each question (1-10).
3. Do NOT generate answers.
4. Questions ask for LOGIC/APPROACH about {selected_domain}, not actual code.
5. Focus on problem-solving methodology in {selected_domain}.
6. Candidate should explain their thinking process.
7. No need to write syntactically correct code.
"""
    
    else:  # Level 3 - HR & AI Knowledge
        prompt = f"""
You are an experienced HR and AI Technical Interviewer conducting a LEVEL 3 Interview.

Generate EXACTLY 10 questions covering HR behavioral questions and AI/Modern Tech knowledge.

Domain Context:
{selected_domain}

LEVEL 3 FOCUS (Mix both types):

HR BEHAVIORAL (5 questions):
- Teamwork and collaboration
- Problem-solving scenarios
- Career goals and motivation in {selected_domain}
- Handling challenges
- Communication skills

Examples:
- Tell me about a time you worked in a team on a {selected_domain} project. What was your role?
- How do you handle tight deadlines when working with {selected_domain}?
- Where do you see yourself in 3 years in the {selected_domain} field?

AI & MODERN TECH KNOWLEDGE (5 questions):
- AI tools usage (ChatGPT, GitHub Copilot, etc.)
- How AI helps in {selected_domain} development
- Modern development practices in {selected_domain}
- Tech trends awareness
- AI in the {selected_domain} industry

Examples for Python:
- How can AI tools like ChatGPT assist you in Python development?
- Have you used any AI-powered coding assistants? How do they help with Python?
- What is the role of AI in modern Python application testing?

Examples for Web Development:
- How do AI tools help in frontend development?
- Have you used AI for code review or debugging in web projects?
- What role does AI play in modern web design and UX?

Rules:
1. Return ONLY questions.
2. Number each question (1-10).
3. Do NOT generate answers.
4. Mix 5 HR behavioral + 5 AI/Modern Tech questions.
5. Questions should assess soft skills and modern tech awareness in {selected_domain}.
6. Focus on real-world application of AI tools in {selected_domain}.
"""

    prompt += f"""
8. Questions must be unique and specifically related to {selected_domain}.
9. Questions should match the level specification exactly.
10. Return in numbered format (1., 2., 3., etc.)
11. DO NOT generate generic questions - they MUST be domain-specific to {selected_domain}.
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ],

        temperature=QUESTION_TEMPERATURE,

        max_tokens=QUESTION_MAX_TOKENS

    )

    generated_text = response.choices[0].message.content.strip()

    question_list = []

    for line in generated_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():

            question = line.split(".", 1)[1].strip()

            question_list.append(question)

    print()

    print("Questions Generated Successfully")

    print()

    return question_list


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    questions = generate_questions("Fundamentals")

    print("=" * 60)

    print("Generated Questions")

    print("=" * 60)

    for i, question in enumerate(questions, start=1):

        print(f"{i}. {question}")