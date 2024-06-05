from app import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(128), unique=True, nullable=False)
    file_content = db.Column(db.Text, nullable=False)
    file_classification = db.Column(db.String(128), nullable=False)
    file_size = db.Column(db.String(120), index=True)
    tags = db.Column(db.String(256))
    date_modified = db.Column(db.String(140))

    # __searchable__ = [
    #     "file_name",
    #     "file_content",
    #     "file_classification",
    #     "file_size",
    #     "tags",
    #     "date_modified",
    # ]  # Columns to be indexed


# search.create_index(Document)
