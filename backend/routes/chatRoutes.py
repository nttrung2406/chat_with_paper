from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.model import rag_model
from services.search import search_relevant_passages

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str

@router.post("/text")
async def chat_with_rag(request: ChatRequest):
    try:
        prompt = request.prompt.strip().lower()

        if prompt in ["hi", "hello", "hey"]:
            return {"answer": "Hello! How can I help you today?"}

        relevant_passages = search_relevant_passages(prompt)
        context = " ".join(relevant_passages)

        if not relevant_passages:
            print("⚠️ No relevant passages found. The bot might hallucinate.")

        full_prompt = f"Using this information with relevant specific knowledge, answer the question: {prompt}\n\n{context}"
        

        response = rag_model.extract_text(full_prompt)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

