import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    UPLOAD_PATH = os.environ.get("UPLOAD_PATH")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MSEARCH_INDEX_NAME = "msearch"
    # MSEARCH_BACKEND = "whoosh"
    # MSEARCH_ENABLE = True
    # MSEARCH_PRIMARY_KEY = "id"
    # UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    # ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}
    # OCR_LANG = "eng"
