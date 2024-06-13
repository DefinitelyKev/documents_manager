from app import db
import os


class Document(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), index=True, nullable=False)
    size = db.Column(db.String(30), index=True, nullable=False)
    abs_path = db.Column(db.String(256), unique=True, nullable=False)
    rel_path = db.Column(db.String(256), nullable=False)
    date_modified = db.Column(db.String(140), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(256))

    __tablename__ = "document"
    __table_args__ = (db.UniqueConstraint("name", "type", "abs_path", name="uix_name_type_abs_path"),)
    __searchable__ = ["name", "type", "size", "abs_path", "rel_path", "date_modified", "tags"]

    def get_inode(self, file_path):
        return os.stat(file_path).st_ino

    def __repr__(self):
        return f"<Document {self.name}>"
