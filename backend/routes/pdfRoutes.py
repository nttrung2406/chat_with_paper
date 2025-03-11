from fastapi import APIRouter, UploadFile, File, HTTPException
from services.inference import process_pdf

router = APIRouter()

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        result = process_pdf(file_content)
        return {"message": result, "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
