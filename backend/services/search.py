from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import torch

client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["rag_db"]
collection = db["embeddings"]
text_embedder = SentenceTransformer("all-mpnet-base-v2") 

def search_relevant_passages(query, top_k=5):
    """Retrieve relevant text passages from MongoDB."""
    query_embedding = text_embedder.encode(query)  
    query_tensor = torch.tensor(query_embedding).unsqueeze(0)  

    results = collection.find()
    passages = []
    
    for doc in results:
        stored_embedding = torch.tensor(doc["embedding"])

        if query_tensor.shape[1] != stored_embedding.shape[0]:
            print(f"Shape Mismatch: Query={query_tensor.shape}, Stored={stored_embedding.shape}")
            continue 

        similarity = torch.cosine_similarity(query_tensor, stored_embedding.unsqueeze(0))
        passages.append((doc["text"], similarity.item()))

    sorted_results = sorted(passages, key=lambda x: x[1], reverse=True)
    
    return [r[0] for r in sorted_results[:top_k]]
