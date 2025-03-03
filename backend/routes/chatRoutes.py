from fastapi import APIRouter, UploadFile, File, HTTPException
from models.model import llava
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/chat/text")
async def chat_with_text(prompt: str):
    """
    Handle text-based queries and return LLaVA-generated response.
    """
    try:
        response = llava.extract_text(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/image")
async def chat_with_image(file: UploadFile = File(...)):
    """
    Handle image-based queries and return LLaVA-generated description.
    """
    try:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process image with LLaVA
        response = llava.extract_image(file_path)

        # Clean up
        os.remove(file_path)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
