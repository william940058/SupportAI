
from sentence_transformers import SentenceTransformer, util
from knowledge import load_knowledge

model = SentenceTransformer("all-MiniLM-L6-v2")

query = "How long does it take to receive my refund?"

knowledge_text = load_knowledge("return_policy.txt")

documents = [
    line.strip()
    for line in knowledge_text.splitlines()
    if line.strip() and line.strip()[0].isdigit()
]

def semantic_search(query):
    query_embedding = model.encode(query)
    document_embeddings = model.encode(documents)

    similarities = util.cos_sim(
        query_embedding,
        document_embeddings
    )[0]

    best_index = similarities.argmax().item()

    return {
        "question": query,
        "best_match": documents[best_index],
        "similarity": similarities[best_index].item()
    }


if __name__ == "__main__":
    result = semantic_search(
        "How long does it take to receive my refund?"
    )
    print(result)
