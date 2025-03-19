import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import re
import string

EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F"  # Emoticons
    u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # Transport & map symbols
    u"\U0001F700-\U0001F77F"  # Alchemical symbols
    u"\U0001F780-\U0001F7FF"  # Geometric symbols
    u"\U0001F800-\U0001F8FF"  # Supplemental arrows
    u"\U0001F900-\U0001F9FF"  # Supplemental symbols
    u"\U0001FA00-\U0001FA6F"  # Chess symbols
    u"\U0001FA70-\U0001FAFF"  # Symbols and pictographs
    u"\U00002702-\U000027B0"  # Dingbats
    u"\U000024C2-\U0001F251" 
    "]+", flags=re.UNICODE)

def clean_text(text):
    """Removes emojis and non-ASCII characters."""
    text = EMOJI_PATTERN.sub('', text)  
    text = text.encode("ascii", "ignore").decode("utf-8")  
    return text.strip()

def extract_text_from_pdf(pdf_content):
    """Extract text from a PDF, using direct text extraction first, then OCR as a fallback."""
    try:
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        extracted_text = ""
        section_headers = []
        current_header = None

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            blocks = page.get_text("blocks")  # Extract text blocks

            for block in blocks:
                text = block[4].strip()
                if not text:
                    continue
                text = clean_text(text)
                # Check if text looks like a header (heuristic: short length, bold, or regex pattern)
                if len(text) < 50 and re.match(r'^\d+[\.\)]?\s+[A-Za-z]+', text):
                    current_header = text.strip()
                    # print("HEADER: ", current_header)
                    section_headers.append(current_header)
                
                chunk_text = f"{current_header if current_header else 'General'}: {text}"
                extracted_text += chunk_text + "\n"
        
        return extracted_text
    except Exception as e:
        print(f"Direct text extraction failed: {e}. Using OCR as fallback.")
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        extracted_text = ""
        section_headers = []
        current_header = None

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = pix.tobytes()
            result = ocr.ocr(img, cls=True)

            for line in result:
                text = line[1][0]
                text = clean_text(text)
                if len(text) < 50 and re.match(r'^\d+[\.\)]?\s+[A-Za-z]+', text):
                    current_header = text.strip()
                    section_headers.append(current_header)
                
                chunk_text = f"{current_header if current_header else 'General'}: {text}"
                extracted_text += chunk_text + "\n"

        return extracted_text


# if __name__ == "__main__":
#     pdf_path = "E:\\Project\\Chat_with_pdf\\clipseg.pdf"
#     text = extract_text_from_pdf(pdf_path)
#     print(text)