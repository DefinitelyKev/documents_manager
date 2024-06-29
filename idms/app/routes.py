from flask import Flask, render_template, abort, send_file, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
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

    files = get_children_dir(Document, abs_path)
    parent_dir = get_parent_dir(req_path)
    path_list = get_path_list(chosen_folder_path, abs_path)
    return render_template("main.html", files=files, parent_dir=parent_dir, dir_path=path_list)


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        global chosen_folder_path, files_processed
        chosen_folder_path = open_up_tk_dir()
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


@app.route("/delete_all/", methods=["GET", "POST"])
def delete_all():
    if request.method == "POST":
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


@app.route("/choose_directory/", methods=["GET"])
def choose_directory():
    folder_selected = open_up_tk_dir()
    return jsonify({"chosen_directory": folder_selected})


@app.route("/move/", methods=["POST"])
def move_file():
    data = request.get_json()
    absolute_file_path = data["absoluteFilePath"]
    destination_path = data["destinationPath"]

    if os.path.exists(absolute_file_path) and os.path.isdir(destination_path):
        new_file_path = os.path.join(destination_path, os.path.basename(absolute_file_path))
        os.rename(absolute_file_path, new_file_path)
        upload_documents_to_db()
        return jsonify({"destination_path": destination_path}), 200
    return jsonify({"error": "Invalid paths provided"}), 400


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


if __name__ == "__main__":
    app.run(debug=True)
