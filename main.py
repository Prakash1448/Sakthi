"""
===========================================
AI Interview Platform
Main Entry Point
===========================================
"""

from interview_engine import start_interview


def main():

    print("=" * 80)
    print("          AI INTERVIEW PLATFORM")
    print("=" * 80)

    print()

    print("Welcome to the AI Interview Platform")

    print()

    print("Interview Flow")

    print("------------------------------")

    print("Level 1 : Fundamentals")

    print("Level 2 : Application")

    print("Level 3 : Problem Solving")

    print()

    input("Press ENTER to Start the Interview...")

    print()

    start_interview()

    print()

    print("=" * 80)
    print("Interview Session Finished")
    print("=" * 80)


if __name__ == "__main__":

    main()