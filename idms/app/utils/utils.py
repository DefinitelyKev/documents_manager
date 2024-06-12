import pytesseract
from PIL import Image
from pathlib import Path
from datetime import datetime
import os
from pypdf import PdfReader
from openai import OpenAI
import asyncio
import aiohttp
from aiohttp import ClientSession

CONFIG_FILE_PATH = "app/utils/chosen_file_path.txt"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

client = OpenAI()


def open_ai_model(text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that categorieze documents and generate tags for the specific document",
            },
            {
                "role": "user",
                "content": f"""
                given this text below and given list of document types, allocate a tag for this document that suits the document the most. Answer with only the tag:
                {text}

                Here is the list of most common document types, choose one from here:
                {common_document_types}
                """,
            },
        ],
    )

    return str(completion.choices[0].message.content)


def save_chosen_folder_path(path):
    with open(CONFIG_FILE_PATH, "w") as file:
        file.write(path)


def load_chosen_folder_path():
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
    file_type = os.path.splitext(name)[1]
    if file_type in [".jpg", ".png"]:
        text = extract_text(abs_path)
        return text
    if file_type in [".pdf"]:
        reader = PdfReader(abs_path)
        text = ""
        for i in range(0, len(reader.pages)):
            text += reader.pages[i].extract_text()
        return remove_empty_newlines(text)
    return ""


def remove_empty_newlines(text):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)


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


common_document_types = [
    "Invoice",
    "Resume",
    "Essay",
    "Report",
    "Letter",
    "Meeting Minutes",
    "Manual/Guide",
    "Notes",
    "Contract",
    "Research Paper",
    "E-book",
    "White Paper",
    "User Manual",
    "Brochure",
    "Proposal",
    "Policy Document",
    "Scanned Documents",
    "Photos",
    "Diagrams/Charts",
    "Screenshots",
    "Scanned Receipts",
    "Presentations",
    "Infographics",
    "Product Images",
    "Homework Assignments",
    "Project Reports",
    "Study Guides",
    "Worksheets",
    "Permission Slips",
    "Thesis/Dissertation",
    "Lecture Notes",
    "Coursework",
    "Internship Reports",
    "Lab Reports",
    "Strategic Plans",
    "Performance Reports",
    "Meeting Agendas",
    "Business Proposals",
    "Budget Reports",
    "Training Materials",
    "Compliance Documents",
    "Other",
]
