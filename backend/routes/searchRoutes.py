from fastapi import APIRouter
from services.vectorStore import search_embedding
from models.model import clip_model

router = APIRouter()

@router.get("/search")
def search(query: str):
    query_embedding = clip_model.get_text_embedding(query)
    results = search_embedding(query_embedding)
    return {"results": results}
