"""
===========================================
Evaluation Module
===========================================
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("Loading MiniLM Embedding Model...")
print("=" * 60)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("MiniLM Loaded Successfully.")
print()


def evaluate_candidate(question_list, reference_answers):

    candidate_answers = []
    scores = []

    print("=" * 60)
    print("Candidate Interview Started")
    print("=" * 60)

    # ---------------------------------------
    # Candidate Answers
    # ---------------------------------------

    for i, question in enumerate(question_list):

        print()
        print("=" * 60)
        print(f"Question {i+1}")
        print("=" * 60)
        print(question)
        print()

        answer = input("Candidate Answer : ")

        candidate_answers.append(answer)

    print()
    print("=" * 60)
    print("Evaluating Answers...")
    print("=" * 60)

    # ---------------------------------------
    # Semantic Evaluation
    # ---------------------------------------

    for ref, cand in zip(reference_answers, candidate_answers):

        ref_embedding = embedding_model.encode(
            [ref]
        )

        cand_embedding = embedding_model.encode(
            [cand]
        )

        similarity = cosine_similarity(
            ref_embedding,
            cand_embedding
        )[0][0]

        score = round(similarity * 10, 2)

        scores.append(score)

    # ---------------------------------------
    # Average Score
    # ---------------------------------------

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    print("Evaluation Completed Successfully.")
    print()

    return (
        average_score,
        candidate_answers,
        scores
    )