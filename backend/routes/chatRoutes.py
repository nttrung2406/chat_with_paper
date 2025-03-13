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
            print("---------------------------------No relevant passages found. The bot might hallucinate.------------------------------------")

        full_prompt = f"Using this information, provide a **concise and unique** answer to the following question: {prompt}\n\n{context}\n\nLimit your response to a single paragraph."

        print(f"Full prompt: {full_prompt}")

        response = rag_model.extract_text(full_prompt)
        cleaned_response = "\n".join(
            line for line in response.split("\n") if not line.startswith("###:")
        )

        return {"answer": cleaned_response.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

