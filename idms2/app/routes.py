from flask import Flask, render_template, abort, send_file, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import os

from app.utils import *
from app.form import DocumentForm
from app.models import Document
from app import app, db

basedir = os.path.abspath(os.path.dirname(__file__))
chosen_folder_path = basedir


def getObjFromScan(root, name):
    abs_path = os.path.join(root, name).replace("\\", "/")
    stat = os.stat(abs_path)
    bytes = getReadableByteSize(stat.st_size)
    m_time = getTimeStampString(stat.st_mtime)
    rel_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")
    file_type = os.path.splitext(name)[1]

    content = ""
    try:
        with open(abs_path, "r", errors="ignore") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file {abs_path}: {e}")

    return {
        "name": name,
        "content": content,
        "type": file_type,
        "size": bytes,
        "m_time": m_time,
        "abs_path": abs_path,
        "rel_path": rel_path,
    }


def uploadDocumentsToDb():
    for root, _, files in os.walk(chosen_folder_path):
        for file_name in files:
            file_obj = getObjFromScan(root, file_name)
            document = Document(
                name=file_obj["name"],
                content=file_obj["content"],
                type=file_obj["type"],
                size=file_obj["size"],
                abs_path=file_obj["abs_path"],
                rel_path=file_obj["rel_path"],
                date_modified=file_obj["m_time"],
                tags="None",
            )
            db.session.add(document)
            db.session.commit()

    flash("Your changes have been saved.")


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
    abs_path = os.path.join(chosen_folder_path, req_path)
    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        if "jpg" in abs_path or "png" in abs_path:
            text = extract_text(abs_path)
            print(text)
        return send_file(abs_path)

    file_names = [fileObjFromScan(x) for x in os.scandir(abs_path)]

    if abs_path == os.path.join(chosen_folder_path, ""):
        uploadDocumentsToDb()

    path_list = []
    dir_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")
    directories = dir_path.split("/")
    if dir_path not in ["..", "."]:
        path_list.append((".", "."))

    for i in range(len(directories)):
        sub_path = "/".join(directories[: i + 1])
        path_list.append((directories[i], sub_path))

    return render_template("dir_view.html", files=file_names, dir_path=path_list)


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
        print(results)
        return render_template("search_result.html", results=results)
    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
