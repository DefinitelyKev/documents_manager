import os
import random

from app.utils.utils import *
from app.models import Document
from app import db
import app.routes as routes

random.seed(420)


def getObjFromScan(root, name, is_file=True):
    if is_file:
        file_type = os.path.splitext(name)[1]
        allowed_file_types = [".txt", ".jpg", ".png", ".pdf", ".docx", ".doc"]
        if file_type not in allowed_file_types:
            return None
    else:
        file_type = "folder"

    abs_path = os.path.join(root, name).replace("\\", "/")
    stat = os.stat(abs_path)
    bytes = getReadableByteSize(stat.st_size)
    m_time = getTimeStampString(stat.st_mtime)
    rel_path = os.path.relpath(abs_path, routes.chosen_folder_path).replace("\\", "/")

    tag_list = ["resume", "invoice", "checklist", "essay", "research paper", "homework", "other"]
    chosen_tag = str([random.choice(tag_list) if file_type != "folder" else "none"])

    return Document(
        name=name,
        type=file_type,
        size=bytes,
        abs_path=abs_path,
        rel_path=rel_path,
        date_modified=m_time,
        tags=chosen_tag,
    )


def addOrUpdateDocment(documents_to_add, documents_to_update, root, name, is_file=True):
    document_obj = getObjFromScan(root, name, is_file)
    if document_obj is None:
        return

    document = Document.query.filter_by(abs_path=document_obj.abs_path).first()
    if document:
        if document.date_modified != document_obj.date_modified:
            document.size = document_obj.size
            document.rel_path = document_obj.rel_path
            document.date_modified = document_obj.date_modified
            document.tags = document_obj.tags
            documents_to_update.append(document)
    else:
        documents_to_add.append(document_obj)


def uploadDocumentsToDb():
    documents_to_add = []
    documents_to_update = []

    for root, dirs, files in os.walk(routes.chosen_folder_path):
        for dir_name in dirs:
            addOrUpdateDocment(documents_to_add, documents_to_update, root, dir_name, is_file=False)
        for file_name in files:
            addOrUpdateDocment(documents_to_add, documents_to_update, root, file_name, is_file=True)

    if documents_to_add:
        db.session.bulk_save_objects(documents_to_add)
    if documents_to_update:
        db.session.bulk_update_mappings(Document, [doc.__dict__ for doc in documents_to_update])
    db.session.commit()
