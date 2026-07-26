from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
import torch

# ==========================================================
# Model Configuration
# ==========================================================

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

print("=" * 60)
print("Checking Qwen Model...")
print("=" * 60)

print("Loading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading Qwen 2.5 7B Model...")

qwen_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("=" * 60)
print("Qwen Model Loaded Successfully")
print("=" * 60)