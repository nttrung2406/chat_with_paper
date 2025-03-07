from models.model import clip_model
from services.pdfProcessor import extract_text_from_pdf
from services.vectorStore import store_embedding

def process_pdf(pdf_content):
    try:
        print("✅ Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(pdf_content)
        print("Extracted text:", extracted_text[:500])  #
        
        print("✅ Generating text embedding...")
        embedding = clip_model.get_text_embedding(extracted_text)
        print("Embedding size:", len(embedding))  
        print("✅ Storing in MongoDB...")
        store_embedding(extracted_text, embedding)

        return "PDF processed and stored in MongoDB."
    except Exception as e:
        print("❌ Error in process_pdf:", str(e))
        raise
