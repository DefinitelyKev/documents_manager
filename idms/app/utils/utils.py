import pytesseract
from PIL import Image
from pathlib import Path
from datetime import datetime
import os
from pypdf import PdfReader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def getTimeStampString(t_sec) -> str:
    t_obj = datetime.fromtimestamp(t_sec)
    t_str = datetime.strftime(t_obj, "%Y-%m-%d %H:%M:%S")
    return t_str


def getReadableByteSize(num, suffix="B") -> str:
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Y", suffix)
