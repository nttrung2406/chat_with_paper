from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import torch

client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["rag_db"]
collection = db["embeddings"]
text_embedder = SentenceTransformer("all-MiniLM-L6-v2")  

def search_relevant_passages(query, top_k=3):
    """Retrieve relevant text passages from MongoDB."""
    query_embedding = text_embedder.encode(query).tolist()
    
    results = collection.find()
    sorted_results = sorted(
        results,
        key=lambda x: torch.cosine_similarity(
            torch.tensor(query_embedding), torch.tensor(x["embedding"]), dim=0
        ),
        reverse=True
    )
    
    return [r["text"] for r in sorted_results[:top_k]]
