import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


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
