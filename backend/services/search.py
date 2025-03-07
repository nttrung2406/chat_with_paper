from pymongo import MongoClient
from transformers import CLIPProcessor, CLIPModel
import torch

client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["rag_db"]
collection = db["embeddings"]
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def search_relevant_passages(query, top_k=5):
    """Retrieve relevant text passages using CLIP embeddings."""
    inputs = processor(text=query, return_tensors="pt", padding=True, truncation=True)
    query_embedding = clip_model.get_text_features(**inputs).detach().numpy().flatten()  # Ensure 512-dim

    results = list(collection.find())

    if not results:
        print("⚠️ No documents found in MongoDB.")
        return []

    sorted_results = sorted(
        results,
        key=lambda x: torch.cosine_similarity(
            torch.tensor(query_embedding), torch.tensor(x["embedding"]), dim=0
        ),
        reverse=True
    )
    if sorted_results[0]["score"] < 0.3:  
        return "Please ask another question."

    return [r["text"] for r in sorted_results[:top_k]]
