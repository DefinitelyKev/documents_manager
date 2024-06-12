import pytesseract
from PIL import Image
from pathlib import Path
from datetime import datetime
import os
from pypdf import PdfReader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CONFIG_FILE_PATH = "app/utils/chosen_file_path.txt"


def save_chosen_folder_path(path):
    print("saving path")
    with open(CONFIG_FILE_PATH, "w") as file:
        file.write(path)


def load_chosen_folder_path():
    print("loading path")
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as file:
            return file.read().strip()
    return ""


def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def img_to_text(abs_path):
    name = os.path.basename(abs_path)
    print(name)
    file_type = os.path.splitext(name)[1]
    if file_type in [".jpg", ".png"]:
        text = extract_text(abs_path)
        print(text)
    if file_type in [".pdf"]:
        reader = PdfReader(abs_path)
        print(len(reader.pages))
        page = reader.pages[0]
        text = page.extract_text()
        print(text)


def get_time_stamp_string(t_sec) -> str:
    t_obj = datetime.fromtimestamp(t_sec)
    t_str = datetime.strftime(t_obj, "%Y-%m-%d %H:%M:%S")
    return t_str


def get_readable_byte_size(num, suffix="B") -> str:
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Y", suffix)
