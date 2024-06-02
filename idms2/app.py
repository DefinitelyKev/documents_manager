from flask import Flask, render_template, abort, send_file
from werkzeug.utils import secure_filename
from config import Config
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config.from_object(Config)

basedir = os.path.abspath(os.path.dirname(__file__))
text_folder_path = os.path.join(basedir, "text")


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


def getIconClassForFilename(fName):
    fileExt = Path(fName).suffix
    fileExt = fileExt[1:] if fileExt.startswith(".") else fileExt
    fileTypes = [
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
    fileIconClass = f"bi bi-filetype-{fileExt}" if fileExt in fileTypes else "bi bi-file-earmark"
    return fileIconClass


@app.route("/", methods=["GET", "POST"], defaults={"req_path": ""})
@app.route("/<path:req_path>", methods=["GET", "POST"])
def index(req_path):
    abs_path = Path(os.path.join(text_folder_path, req_path))
    print(abs_path)
    if not os.path.exists(abs_path):
        print("poo")
        return abort(404)

    if os.path.isfile(abs_path):
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
            "link": os.path.relpath(x.path, text_folder_path).replace("\\", "/"),
        }

    f_names = [fObj_from_scan(x) for x in os.scandir(abs_path)]
    parent_path = os.path.relpath(abs_path.parents[0], text_folder_path).replace("\\", "/")

    directories = parent_path.split("/")
    path_list = []
    if parent_path not in ["..", "."]:
        path_list.append((".", "."))

    for i in range(len(directories)):
        sub_path = "/".join(directories[: i + 1])
        path_list.append((directories[i], sub_path))

    return render_template("index.html", files=f_names, parent_path=path_list)


if __name__ == "__main__":
    app.run(debug=True)
