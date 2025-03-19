from models.model import minilm_model
from services.pdfProcessor import extract_text_from_pdf
from services.vectorStore import store_embedding

def process_pdf(pdf_content):
    try:
        print("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(pdf_content)
        # print("Extracted text:", extracted_text[:500])  
        
        embedding = minilm_model.get_text_embedding(extracted_text)
        print("Embedding size:", len(embedding))  
        store_embedding(extracted_text, embedding)

        return "PDF processed and stored in MongoDB."
    except Exception as e:
        print("Error in process_pdf:", str(e))
        raise
