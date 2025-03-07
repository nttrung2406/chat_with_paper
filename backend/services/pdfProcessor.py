import fitz  # PyMuPDF
from paddleocr import PaddleOCR

def extract_text_from_pdf(pdf_content):
    """Extract text from a PDF using OCR."""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    
    extracted_text = ""
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")  # Extract text
        extracted_text += text + "\n"
    
    return extracted_text

# if __name__ == "__main__":
#     pdf_path = "E:\\Project\\Chat_with_pdf\\clipseg.pdf"
#     text = extract_text_from_pdf(pdf_path)
#     print(text)