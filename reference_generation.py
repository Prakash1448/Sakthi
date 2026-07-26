from model_loader import tokenizer, qwen_model
from config import (
    ANSWER_TEMPERATURE,
    ANSWER_MAX_TOKENS
)


def generate_reference_answers(question_list):

    reference_answers = []

    print("=" * 60)
    print("Generating Reference Answers...")
    print("=" * 60)

    for question in question_list:

        prompt = f"""
You are an experienced technical interviewer.

Generate the ideal interview answer.

Question:
{question}

Rules:

- Answer should be technically correct.
- Around 80-120 words.
- Easy English.
- Suitable for freshers.
- Return ONLY the answer.
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
            max_new_tokens=ANSWER_MAX_TOKENS,
            temperature=ANSWER_TEMPERATURE
        )

        generated_tokens = outputs[0][
            inputs["input_ids"].shape[1]:
        ]

        answer = tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        reference_answers.append(answer)

    print("Reference Answers Generated Successfully.")

    return reference_answers