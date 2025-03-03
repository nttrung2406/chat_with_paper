from models.model import clip_model
from services.pdfProcessor import extract_text_from_pdf
from services.vectorStore import store_embedding

def process_pdf(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    embedding = clip_model.get_text_embedding(extracted_text)
    store_embedding(extracted_text, embedding)
    return "PDF processed and stored in MongoDB."
