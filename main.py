"""
===========================================
AI Interview Platform
Qwen 2.5 7B
Voice Interview Backend
===========================================
"""

from interview_engine import start_interview


def main():

    print("=" * 70)
    print("        AI INTERVIEW PLATFORM")
    print("=" * 70)
    print()

    print("Domain : Data Structures and Algorithms")
    print()

    print("Interview Flow")
    print("----------------------------")
    print("Level 1 -> Fundamentals")
    print("Level 2 -> Application")
    print("Level 3 -> Problem Solving")
    print()

    input("Press ENTER to Start Interview...")

    start_interview()

    print()
    print("=" * 70)
    print("Interview Completed.")
    print("=" * 70)


if __name__ == "__main__":
    main()