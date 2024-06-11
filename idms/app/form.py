from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class DocumentForm(FlaskForm):
    file_name = StringField("File Name", validators=[DataRequired(), Length(min=2, max=120)])
    file_content = TextAreaField("File Content", validators=[DataRequired()])
    submit = SubmitField("Update")
