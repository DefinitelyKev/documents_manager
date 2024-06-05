from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired

# class DirForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     about_me = TextAreaField("About Me", validators=[DataRequired()])
#     avatar = FileField("Avatar", validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images Only!")])
#     submit = SubmitField("Update")


class DocumentForm(FlaskForm):
    file_name = StringField("File Name", validators=[DataRequired(), Length(min=2, max=120)])
    file_content = TextAreaField("File Content", validators=[DataRequired()])
    # file_classification = db.Column(db.String(128), nullable=False)
    submit = SubmitField("Update")
