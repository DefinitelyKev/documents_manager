from app import app, db
from flask import render_template, redirect, flash, url_for
from app.forms import UserForm
from werkzeug.utils import secure_filename
from app.models import User
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UserForm()
    users = User.query.all()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            about_me = form.about_me.data
        )

        uploaded_file = form.avatar.data
        filename = secure_filename(uploaded_file.filename)
        avatar_path = os.path.join(app.config["UPLOAD_PATH"], filename)
        uploaded_file.save(avatar_path)
        user.avatar = avatar_path
        path_list = user.avatar.split('/')[1:]
        new_path = '/'.join(path_list)
        
        # Update the database
        user.avatar = new_path
        db.session.add(user)
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, title='User Form', users=users)