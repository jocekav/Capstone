from flask import Blueprint, render_template, request, redirect, url_for
from __init__ import db
from __init__ import create_app
from forms import UpdateProfileForm
from flask_login import login_user, logout_user, login_required, current_user
import spotifyLogin

import os
import uuid
from PIL import Image

main = Blueprint('main', __name__)

#homepage
@main.route('/')
def index():
    return render_template('index.html')

#profile page
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if 'code' in request.args:
            global token
            print(request.args['code'])
            userToken = spotifyLogin.getUserToken(request.args['code'])
            token = userToken[0]
            current_user.token = token
            db.session.commit()
            print(token)
    if form.validate_on_submit():
        if form.picture.data:
            f = form.picture.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            picture_path = os.path.join(app.root_path, 'static/', file_name)
            output_size = (125, 125)
            i = Image.open(form.picture.data)
            i.thumbnail(output_size)
            i.save(picture_path)
            # picture_file = form.save_picture(form.picture.data)
            current_user.image_file = file_name
        current_user.location = form.location.data
        current_user.preference = form.preference.data
        current_user.age = form.age.data
        db.session.commit()
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.location.data = current_user.location
        form.preference.data = current_user.preference
        form.age.data = current_user.age
    image_file = url_for('static', filename= current_user.image_file)
    return render_template('profile.html',
                           image_file=image_file, form=form, name=current_user.name)
    # return render_template('profile.html', name=current_user.name)


#init flask app
app = create_app()

if __name__ == '__main__':
    #create database when runnning the app
    db.create_all(app=create_app())
    app.run(debug=True)