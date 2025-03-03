from pymongo import MongoClient
import torch
client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["rag_db"]
collection = db["embeddings"]

def store_embedding(text, embedding):
    collection.insert_one({"text": text, "embedding": embedding})

def search_embedding(query_embedding, top_k=5):
    results = collection.find()
    sorted_results = sorted(results, key=lambda x: torch.cosine_similarity(
        torch.tensor(query_embedding), torch.tensor(x["embedding"]), dim=0), reverse=True)
    return sorted_results[:top_k] 
