import os
import re
from PIL import Image
import pytesseract
import docx
from pdf2image import convert_from_path
from langdetect import detect_langs

# List of supported Indian languages for OCR
INDIAN_LANGUAGES = ["hin", "tam", "tel", "ben", "mar", "guj", "kan", "mal", "pan"]

def detect_languages(text_chunk):
    try:
        langs = detect_langs(text_chunk)
        langs_sorted = sorted(langs, key=lambda x: x.prob, reverse=True)
        tess_langs = []
        mapping = {"hi":"hin","ta":"tam","te":"tel","bn":"ben","mr":"mar",
                   "gu":"guj","kn":"kan","ml":"mal","pa":"pan"}
        for l in langs_sorted:
            if l.lang == "en":
                tess_langs.append("eng")
            elif l.lang in mapping:
                tess_langs.append(mapping[l.lang])
        return "+".join(set(tess_langs)) if tess_langs else "eng"
    except:
        return "eng"


def load_document(path: str) -> str:
    """
    Load document from path and return extracted text.
    Supports .txt, .pdf, .docx, .jpg/.png
    """
    ext = os.path.splitext(path)[1].lower()
    text = ""

    if ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    elif ext == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except:
            pass

        # fallback to OCR if PDF is scanned
        if not text.strip():
            images = convert_from_path(path)
            for img in images:
                tess_lang = detect_languages(pytesseract.image_to_string(img, lang="eng"))
                text += pytesseract.image_to_string(img, lang=tess_lang)

    elif ext in [".doc", ".docx"]:
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext in [".jpg", ".jpeg", ".png"]:
        img = Image.open(path)
        tess_lang = detect_languages(pytesseract.image_to_string(img, lang="eng"))
        text = pytesseract.image_to_string(img, lang=tess_lang)

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    # Clean extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text
