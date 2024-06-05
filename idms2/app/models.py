from app import db


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(128), index=True, nullable=False)
    size = db.Column(db.String(30), index=True, nullable=False)
    abs_path = db.Column(db.String(256), nullable=False)
    rel_path = db.Column(db.String(256), nullable=False)
    date_modified = db.Column(db.String(140), nullable=False)
    tags = db.Column(db.String(256))

    __tablename__ = "document"
    __table_args__ = (db.UniqueConstraint("name", "type", "abs_path", name="uix_name_type_abs_path"),)
    __searchable__ = ["name", "content", "type", "size", "abs_path", "rel_path", "date_modified", "tags"]

    def __repr__(self):
        return f"<Document {self.name}>"
