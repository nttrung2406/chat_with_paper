from fastapi import APIRouter
from models.model import rag_model
from services.search import search_relevant_passages

router = APIRouter()

@router.get("/chat")
def chat_with_rag(query: str):
    relevant_passages = search_relevant_passages(query)
    context = " ".join(relevant_passages)
    prompt = f"Using this information, answer the question: {query}\n\n{context}"
    response = rag_model.extract_text(prompt)
    return {"answer": response}
