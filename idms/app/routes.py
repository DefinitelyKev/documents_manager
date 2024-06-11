from flask import Flask, render_template, abort, send_file, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import random
import ast
import os

from app.utils import *
from app.form import DocumentForm
from app.models import Document
from app import app, db

basedir = os.path.abspath(os.path.dirname(__file__))
chosen_folder_path = ""

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
    rel_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")

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

    for root, dirs, files in os.walk(chosen_folder_path):
        for dir_name in dirs:
            addOrUpdateDocment(documents_to_add, documents_to_update, root, dir_name, is_file=False)
        for file_name in files:
            addOrUpdateDocment(documents_to_add, documents_to_update, root, file_name, is_file=True)

    if documents_to_add:
        db.session.bulk_save_objects(documents_to_add)
    if documents_to_update:
        db.session.bulk_update_mappings(Document, [doc.__dict__ for doc in documents_to_update])
    db.session.commit()


def sortFiles():
    documents = Document.query.all()
    tag_to_paths = {}

    for doc in documents:
        tags = ast.literal_eval(doc.tags)
        for tag in tags:
            if tag not in tag_to_paths:
                tag_to_paths[tag] = []
            tag_to_paths[tag].append(doc.abs_path)

    for tag, paths in tag_to_paths.items():
        if tag == "none":
            continue

        tag_folder_path = os.path.join(chosen_folder_path, secure_filename(tag))
        if not os.path.exists(tag_folder_path):
            os.mkdir(tag_folder_path)

        for path in paths:
            try:
                new_path = os.path.join(tag_folder_path, os.path.basename(path))
                os.rename(path, new_path)

                document = Document.query.filter_by(abs_path=path).first()
                document.abs_path = new_path
                document.rel_path = os.path.relpath(new_path, chosen_folder_path)

                db.session.add(document)
            except Exception as e:
                print(f"Error moving file {path}: {e}")

    db.session.commit()


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        global chosen_folder_path
        root = Tk()
        root.attributes("-topmost", True, "-alpha", 0)
        file_name = filedialog.askdirectory()
        root.destroy()
        del root
        chosen_folder_path = file_name
        return redirect(url_for("dir_view"))

    return render_template("upload.html")


@app.route("/dir_view/", methods=["GET", "POST"], defaults={"req_path": ""})
@app.route("/dir_view/<path:req_path>", methods=["GET", "POST"])
def dir_view(req_path):
    abs_path = os.path.join(chosen_folder_path, req_path).replace("\\", "/") if req_path else chosen_folder_path

    if not os.path.exists(abs_path):
        return redirect(url_for("upload"))

    if os.path.isfile(abs_path):
        if abs_path.endswith(".png") or abs_path.endswith(".jpg"):
            text = extract_text(abs_path)
            print(text)
        if abs_path.endswith(".pdf"):
            reader = PdfReader(abs_path)
            print(len(reader.pages))
            page = reader.pages[0]
            text = page.extract_text()
            print(text)
        return send_file(abs_path)

    if abs_path == chosen_folder_path:
        uploadDocumentsToDb()

    documents = Document.query.filter(Document.abs_path.like(f"{abs_path}%")).all()
    direct_children = [doc for doc in documents if os.path.dirname(doc.abs_path) == abs_path]

    path_list = []
    dir_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")
    directories = dir_path.split("/")
    if dir_path not in ["..", "."]:
        path_list.append((".", "."))

    for i in range(len(directories)):
        sub_path = "/".join(directories[: i + 1])
        path_list.append((directories[i], sub_path))

    return render_template("dir_view.html", files=direct_children, dir_path=path_list)


@app.route("/add_file/", methods=["GET", "POST"])
def add_file():
    form = DocumentForm()
    documents = Document.query.all()
    if form.validate_on_submit():
        document = Document(
            name=form.file_name.data,
            content=form.file_content.data,
            type="txt",
            size="100",
            abs_path="None",
            rel_path="None",
            date_modified="4/06",
            tags="None",
        )

        db.session.add(document)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("add_file"))

    if request.method == "POST":
        sort_req = request.form.get("sortInput")
        if sort_req is not None:
            sortFiles()
            return redirect(url_for("add_file"))

    return render_template("add_file.html", form=form, documents=documents)


@app.route("/delete_file/", methods=["GET", "POST"])
def delete_file():
    if request.method == "POST":
        id = request.form.get("deleteInput")
        if id is not None:
            document = Document.query.get(id)

            if document:
                db.session.delete(document)
                db.session.commit()
                return redirect(url_for("add_file"))
            else:
                return 404

        del_all = request.form.get("deleteAllInput")
        if del_all is not None:
            try:
                Document.query.delete()
                db.session.commit()
                return redirect(url_for("add_file"))
            except Exception as e:
                db.session.rollback()
                return f"An error occurred: {str(e)}", 500

    return render_template("delete_file.html")


@app.route("/search/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("searchInput")
        results = Document.query.msearch(query).all()
        return render_template("search_result.html", results=results)
    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
