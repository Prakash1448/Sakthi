from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("Loading MiniLM Embedding Model...")
print("=" * 60)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("MiniLM Loaded Successfully.")

def evaluate(reference_answers, candidate_answers):

    scores = []

    print("=" * 60)
    print("Evaluating Candidate Answers...")
    print("=" * 60)

    for ref, cand in zip(reference_answers, candidate_answers):

        ref_embedding = embedding_model.encode([ref])

        cand_embedding = embedding_model.encode([cand])

        similarity = cosine_similarity(
            ref_embedding,
            cand_embedding
        )[0][0]

        score = round(similarity * 10, 2)

        scores.append(score)

    print("Evaluation Completed Successfully.")

    return scores