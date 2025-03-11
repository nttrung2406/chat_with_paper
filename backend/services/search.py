from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import torch

client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["rag_db"]
collection = db["embeddings"]

minilm_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def search_relevant_passages(query, top_k=5):
    """Retrieve relevant text passages using MiniLM embeddings."""
    query_embedding = minilm_model.encode(query, convert_to_tensor=True)
    
    results = list(collection.find())
    if not results:
        print("⚠️ No documents found in MongoDB.")
        return []
    
    sorted_results = sorted(
        results,
        key=lambda x: torch.cosine_similarity(query_embedding, torch.tensor(x["embedding"]), dim=0),
        reverse=True
    )
    
    if sorted_results[0]["score"] < 0.3:
        return "Please ask another question."
    
    return [r["text"] for r in sorted_results[:top_k]]
