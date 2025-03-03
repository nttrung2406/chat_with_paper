from fastapi import APIRouter, Query
from services.vectorStore import search_documents

router = APIRouter()

@router.get("/")
async def search(query: str = Query(...)):
    results = search_documents(query)
    return {"results": results}