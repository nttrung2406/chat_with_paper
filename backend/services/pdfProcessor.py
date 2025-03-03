import fitz  # PyMuPDF
from paddleocr import PaddleOCR

def extract_text_from_pdf(pdf_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    pdf_document = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = pix.tobytes()

        result = ocr.ocr(img)

        for line in result:
            for word in line:
                extracted_text += word[1][0] + " "

    return extracted_text

# if __name__ == "__main__":
#     pdf_path = "E:\\Project\\Chat_with_pdf\\clipseg.pdf"
#     text = extract_text_from_pdf(pdf_path)
#     print(text)