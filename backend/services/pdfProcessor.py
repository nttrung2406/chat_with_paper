import fitz  # PyMuPDF
from paddleocr import PaddleOCR

def extract_text_from_pdf(pdf_content):
    """Extract text from a PDF, using direct text extraction first, then OCR as a fallback."""
    try:
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        extracted_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            if not text.strip():
                raise ValueError("No text extracted directly, falling back to OCR.")
            extracted_text += text + "\n"
        return extracted_text
    except Exception as e:
        print(f"Direct text extraction failed: {e}. Using OCR as fallback.")
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        extracted_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = pix.tobytes()
            result = ocr.ocr(img, cls=True)
            for line in result:
                extracted_text += line[1][0] + "\n"
        return extracted_text


# if __name__ == "__main__":
#     pdf_path = "E:\\Project\\Chat_with_pdf\\clipseg.pdf"
#     text = extract_text_from_pdf(pdf_path)
#     print(text)