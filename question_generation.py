"""
===========================================
Question Generation Module
===========================================
"""

from model_loader import tokenizer, qwen_model
from config import (
    DOMAIN,
    QUESTION_TEMPERATURE,
    QUESTION_MAX_TOKENS
)


def generate_questions(level):

    print("=" * 60)
    print(f"Generating {level} Questions...")
    print("=" * 60)

    prompt = f"""
You are an experienced technical interviewer.

Generate exactly 10 interview questions.

Domain:
{DOMAIN}

Difficulty:
{level}

Rules:

If Difficulty is Fundamentals:
- Ask only beginner-level questions.
- Focus on definitions.
- Focus on concepts.
- Ask simple real-world examples.
- Do NOT ask coding questions.
- Do NOT ask implementation questions.

If Difficulty is Application:
- Ask scenario-based questions.
- Ask practical questions.
- Ask comparison questions.
- Do NOT ask coding problems.

If Difficulty is Problem Solving:
- Ask analytical questions.
- Ask design-thinking questions.
- Ask optimization ideas.
- Still NO coding questions.

Return ONLY the numbered questions.

Example:

1. What is a Stack?
2. Explain Queue with an example.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(next(qwen_model.parameters()).device)
        for k, v in inputs.items()
    }

    outputs = qwen_model.generate(
        **inputs,
        max_new_tokens=QUESTION_MAX_TOKENS,
        temperature=QUESTION_TEMPERATURE,
        do_sample=True
    )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    generated_text = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    question_list = []

    for line in generated_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if "." in line and line[0].isdigit():

            question = line.split(".", 1)[1].strip()

            question_list.append(question)

    print("Questions Generated Successfully.")
    print()

    return question_list