"""
===========================================
Qwen 2.5 7B Model Loader
===========================================
"""

import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

# ==========================================================
# Model Name
# ==========================================================

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# ==========================================================
# Load Tokenizer
# ==========================================================

print("=" * 60)
print("Loading Qwen Tokenizer...")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# ==========================================================
# Load Model
# ==========================================================

print("Loading Qwen 2.5 7B Model...")
print("This may take a few minutes...")

qwen_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

# ==========================================================
# Ready
# ==========================================================

print("=" * 60)
print("✅ Qwen 2.5 7B Loaded Successfully")
print("=" * 60)