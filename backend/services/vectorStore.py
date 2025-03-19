from pymongo import MongoClient
import torch
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["rag_db"]
collection = db["embeddings"]

def store_embedding(text, embedding, header="General"):
    """Store text embeddings with contextual headers in MongoDB."""
    augmented_text = f"{header}: {text}"
    collection.insert_one({"header": header, "text": augmented_text, "embedding": embedding})


def search_embedding(query_embedding, top_k=5):
    results = collection.find()
    sorted_results = sorted(results, key=lambda x: torch.cosine_similarity(
        torch.tensor(query_embedding), torch.tensor(x["embedding"]), dim=0), reverse=True)
    return sorted_results[:top_k] 
