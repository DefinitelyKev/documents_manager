import os
import ast
from werkzeug.utils import secure_filename

from app.models import Document
import app.routes as routes
from app import db


def sort_files():
    documents = Document.query.all()
    tag_to_paths = {}

    for doc in documents:
        tags = ast.literal_eval(doc.tags)
        for tag in tags:
            if tag not in tag_to_paths:
                tag_to_paths[tag] = []
            tag_to_paths[tag].append(doc.abs_path)

    for tag, paths in tag_to_paths.items():
        if tag == "None":
            continue

        tag_folder_path = os.path.join(routes.chosen_folder_path, secure_filename(tag))
        if not os.path.exists(tag_folder_path):
            os.mkdir(tag_folder_path)

        for path in paths:
            try:
                new_path = os.path.join(tag_folder_path, os.path.basename(path))
                count = 1
                while os.path.exists(new_path):
                    directory, file_name = os.path.split(new_path)
                    file_base_name, file_extension = os.path.splitext(file_name)
                    new_file_name = f"{file_base_name}({count}){file_extension}"
                    new_path = os.path.join(directory, new_file_name)
                    count += 1
                os.rename(path, new_path)

                document = Document.query.filter_by(abs_path=path).first()
                document.abs_path = new_path.replace("\\", "/")
                document.rel_path = os.path.relpath(new_path, routes.chosen_folder_path).replace("\\", "/")

                db.session.add(document)
            except Exception as e:
                print(f"Error moving file {path}: {e}")

    db.session.commit()
