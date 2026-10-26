"""
===========================================
Groq Client
AI Interview Platform
===========================================
"""

import os

from groq import Groq

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Read API Key
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================================
# Validate API Key
# ==========================================================

if GROQ_API_KEY is None or GROQ_API_KEY == "":

    raise ValueError(
        "❌ GROQ_API_KEY not found.\n"
        "Please create a .env file and add:\n\n"
        "GROQ_API_KEY=your_api_key"
    )

# ==========================================================
# Initialize Groq Client
# ==========================================================

client = Groq(
    api_key=GROQ_API_KEY
)

print("=" * 60)
print("Groq Client Initialized Successfully")
print("=" * 60)

# ==========================================================
# Test Connection
# ==========================================================

if __name__ == "__main__":

    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "user",
                    "content": "Say Hello"
                }
            ]

        )

        print("\nGroq Connection Successful\n")

        print(response.choices[0].message.content)

    except Exception as e:

        print("\nGroq Connection Failed\n")

        print(e)