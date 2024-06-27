from flask import Flask, render_template, abort, send_file, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
from tkinter import filedialog
from tkinter import *
import os

from app.utils.utils import *
from app.utils.db_utils import *
from app.utils.sort_utils import *
from app.form import DocumentForm
from app.models import Document
from app import app, db

chosen_folder_path = load_chosen_folder_path()


@app.route("/", methods=["GET", "POST"], defaults={"req_path": ""})
@app.route("/<path:req_path>", methods=["GET", "POST"])
def main(req_path):
    global chosen_folder_path
    if not chosen_folder_path:
        return render_template("main.html")

    abs_path = os.path.join(chosen_folder_path, req_path).replace("\\", "/") if req_path else chosen_folder_path

    if not os.path.exists(abs_path):
        return render_template("main.html")

    if os.path.isfile(abs_path):
        img_to_text(abs_path)
        return send_file(abs_path)

    if abs_path == chosen_folder_path:
        upload_documents_to_db()
        delete_unused_records()

    documents = Document.query.filter(Document.abs_path.like(f"{abs_path}%")).all()
    direct_children = [doc for doc in documents if os.path.dirname(doc.abs_path) == abs_path]

    path_list = []
    dir_path = os.path.relpath(abs_path, chosen_folder_path).replace("\\", "/")
    directories = dir_path.split("/")

    for i in range(len(directories)):
        sub_path = "/".join(directories[: i + 1])
        path_list.append((directories[i], sub_path))

    if dir_path == ".":
        path_list[0] = (f"{os.path.basename(chosen_folder_path)}", ".")
    else:
        path_list = [(f"{os.path.basename(chosen_folder_path)}", ".")] + path_list

    parent_dir = os.path.dirname(req_path)

    for i in direct_children:
        i.tags = ast.literal_eval(i.tags)

    return render_template("main.html", files=direct_children, dir_path=path_list, parent_dir=parent_dir)


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        global chosen_folder_path, files_processed
        root = Tk()
        root.attributes("-topmost", True, "-alpha", 0)
        file_name = filedialog.askdirectory()
        root.destroy()
        del root
        chosen_folder_path = file_name
        save_chosen_folder_path(chosen_folder_path)
        return redirect(url_for("main"))
    return render_template("main.html")


@app.route("/check_database/", methods=["GET", "POST"])
def check_database():
    global files_processed
    documents = Document.query.all()

    if request.method == "POST":
        sort_req = request.form.get("sortInput")
        if sort_req is not None:
            sort_files()
            files_processed = False
            return redirect(url_for("main"))

    return render_template("check_database.html", documents=documents)


@app.route("/delete/", methods=["POST"])
def delete_file():
    absolute_file_path = request.form.get("absoluteFilePath")

    if os.path.exists(absolute_file_path):
        try:
            os.remove(absolute_file_path)

            document = Document.query.filter_by(abs_path=absolute_file_path).first()
            if document:
                db.session.delete(document)
                db.session.commit()

            return "File deleted successfully", 200
        except Exception as e:
            db.session.rollback()
            return f"Error deleting file: {str(e)}", 500

    return "File not found", 404


@app.route("/delete_file/", methods=["GET", "POST"])
def delete_file1():
    if request.method == "POST":
        del_by_id = request.form.get("deleteInput")
        if del_by_id is not None:
            document = Document.query.get(del_by_id)

            if document:
                db.session.delete(document)
                db.session.commit()
                return redirect(url_for("check_database"))
            else:
                return 404

        del_all = request.form.get("deleteAllInput")
        if del_all is not None:
            try:
                global chosen_folder_path
                Document.query.delete()
                db.session.commit()
                chosen_folder_path = None
                return redirect(url_for("check_database"))
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


@app.route("/rename/", methods=["POST"])
def rename_file():
    current_file_path = request.form["currentFilePath"]
    new_file_name = request.form["newFileName"]
    directory = os.path.dirname(current_file_path)
    new_file_path = os.path.join(directory, new_file_name)

    if os.path.exists(current_file_path):
        os.rename(current_file_path, new_file_path)
    return redirect(url_for("main", req_path=directory))


@app.route("/move/", methods=["POST"])
def move_file():
    absolute_file_path = request.form["absoluteFilePath"]
    destination_path = request.form["destinationPath"]

    if os.path.exists(absolute_file_path) and os.path.isdir(destination_path):
        new_file_path = os.path.join(destination_path, os.path.basename(absolute_file_path))
        os.rename(absolute_file_path, new_file_path)
    return redirect(url_for("main", req_path=os.path.dirname(absolute_file_path)))


if __name__ == "__main__":
    app.run(debug=True)
