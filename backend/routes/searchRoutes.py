from fastapi import APIRouter
from services.vectorStore import search_embedding
from models.model import minilm_model

router = APIRouter()

@router.get("/search")
def search(query: str):
    query_embedding = minilm_model.get_text_embedding(query)
    results = search_embedding(query_embedding)
    return {"results": results}
