from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import torch
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["rag_db"]
collection = db["embeddings"]

device = "cuda" if torch.cuda.is_available() else "cpu"
minilm_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").to(device)

def search_relevant_passages(query, top_k=5):
    """Retrieve relevant text passages using MiniLM embeddings."""
    query_embedding = minilm_model.encode(query, convert_to_tensor=True).to(device)
    
    results = list(collection.find())
    if not results:
        print("---------------------No documents found in MongoDB.-------------------")
        return []
    
    # sorted_results = sorted(
    #     results,
    #     key=lambda x: torch.cosine_similarity(query_embedding, torch.tensor(x["embedding"], device=device), dim=0),
    #     reverse=True
    # )
    
    # if sorted_results[0]["score"] < 0.3:
    #     return "Please ask another question."
    
    # return [r["text"] for r in sorted_results[:top_k]]
    scored_results = []
    
    for doc in results:
        if "embedding" not in doc or "text" not in doc:
            continue 

        doc_embedding = torch.tensor(doc["embedding"], device=device)
        similarity = torch.cosine_similarity(query_embedding, doc_embedding, dim=0)

        scored_results.append((similarity.item(), doc["text"]))

    scored_results.sort(reverse=True, key=lambda x: x[0])

    if not scored_results or scored_results[0][0] < 0.3:
        return ["Please ask another question."]

    return [text for _, text in scored_results[:top_k]]
