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


def getIconClassForFilename(f_name):
    file_ext = Path(f_name).suffix
    file_ext = file_ext[1:] if file_ext.startswith(".") else file_ext
    file_types = file_types_list
    file_icon_class = f"bi bi-filetype-{file_ext}" if file_ext in file_types else "bi bi-file-earmark"
    return file_icon_class


def fileObjFromScan(x):
    from app.routes import chosen_folder_path

    file_icon = "bi bi-folder-fill" if os.path.isdir(x.path) else getIconClassForFilename(x.name)
    file_stat = x.stat()
    file_bytes = getReadableByteSize(file_stat.st_size)
    file_time = getTimeStampString(file_stat.st_mtime)
    file_link = os.path.relpath(x.path, chosen_folder_path).replace("\\", "/")
    return {"name": x.name, "size": file_bytes, "mTime": file_time, "icon": file_icon, "link": file_link}


file_types_list = [
    "aac",
    "ai",
    "bmp",
    "cs",
    "css",
    "csv",
    "doc",
    "docx",
    "exe",
    "gif",
    "heic",
    "html",
    "java",
    "jpg",
    "js",
    "json",
    "jsx",
    "key",
    "m4p",
    "md",
    "mdx",
    "mov",
    "mp3",
    "mp4",
    "otf",
    "pdf",
    "php",
    "png",
    "pptx",
    "psd",
    "py",
    "raw",
    "rb",
    "sass",
    "scss",
    "sh",
    "sql",
    "svg",
    "tiff",
    "tsx",
    "ttf",
    "txt",
    "wav",
    "woff",
    "xlsx",
    "xml",
    "yml",
]
