from fastapi import APIRouter, UploadFile, File
from services.pdfProcessor import extract_text

router = APIRouter()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text(await file.read())
    return {"text": text}