from model_loader import tokenizer, qwen_model
from config import (
    DOMAIN,
    LEVEL,
    QUESTION_TEMPERATURE,
    QUESTION_MAX_TOKENS
)

def generate_questions():

    prompt = f"""
You are an experienced technical interviewer.

Generate exactly 10 interview questions.

Domain:
{DOMAIN}

Difficulty:
{LEVEL}

Rules:

- Ask only beginner-level questions.
- Focus on concepts.
- Focus on definitions.
- Ask simple real-world examples.
- Do NOT ask coding questions.
- Do NOT ask implementation questions.
- Do NOT ask algorithms.

Return ONLY the numbered questions.
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
        temperature=QUESTION_TEMPERATURE
    )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    questions = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    question_list = []

    for line in questions.split("\n"):

        line = line.strip()

        if line == "":
            continue

        if line[0].isdigit():

            question = line.split(".", 1)[1].strip()

            question_list.append(question)

    return question_list