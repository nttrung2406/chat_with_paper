from fastapi import APIRouter, UploadFile, File
import shutil
from services.inference import process_pdf

router = APIRouter()

@router.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    file_path = f"{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    message = process_pdf(file_path)
    return {"message": message}
