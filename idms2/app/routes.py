from flask import Flask, render_template, abort, send_file, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import os

from app.utils import file_types_list, extract_text
from app.form import DocumentForm
from app.models import Document
from app import app, db

basedir = os.path.abspath(os.path.dirname(__file__))
chosen_folder_path = basedir


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

    def fObj_from_scan(x):
        f_icon = "bi bi-folder-fill" if os.path.isdir(x.path) else getIconClassForFilename(x.name)
        file_stat = x.stat()
        f_bytes = getReadableByteSize(file_stat.st_size)
        f_time = getTimeStampString(file_stat.st_mtime)
        return {
            "name": x.name,
            "size": f_bytes,
            "mTime": f_time,
            "icon": f_icon,
            "link": os.path.relpath(x.path, chosen_folder_path).replace("\\", "/"),
        }

    f_names = [fObj_from_scan(x) for x in os.scandir(abs_path)]
    dir_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")

    directories = dir_path.split("/")
    path_list = []
    if dir_path not in ["..", "."]:
        path_list.append((".", "."))

    for i in range(len(directories)):
        sub_path = "/".join(directories[: i + 1])
        path_list.append((directories[i], sub_path))

    return render_template("dir_view.html", files=f_names, dir_path=path_list)


@app.route("/add_file/", methods=["GET", "POST"])
def add_file():
    form = DocumentForm()
    documents = Document.query.all()
    if form.validate_on_submit():
        document = Document(
            file_name=form.file_name.data,
            file_content=form.file_content.data,
            file_classification="txt",
            file_size="100",
            tags="None",
            date_modified="4/06",
        )

        db.session.add(document)
        db.session.commit()

        flash("Your changes have been saved.")
        return redirect(url_for("add_file"))
    return render_template("add_file.html", form=form, documents=documents)


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
