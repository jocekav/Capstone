from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from __init__ import create_app
from forms import UpdateProfileForm
from flask_login import login_user, logout_user, login_required, current_user
import spotifyLogin
import playlist
import numpy as np

import os
import uuid
from PIL import Image

main_bp = Blueprint('main', __name__)

#homepage
@main_bp.route('/')
def index():
    return render_template('index.html')

#profile page
@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if 'code' in request.args:
            userToken = spotifyLogin.getUserToken(request.args['code'])
            token = userToken[0]
            current_user.token = token
            spotify_id = spotifyLogin.getUserID(token)
            current_user.spotify_id = spotify_id
            db.session.commit()
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

@main_bp.route('/load_spotify_data')
def load_spotify_data():
    print('button push')
    token = current_user.token
    user_id = current_user.spotify_id
    playlists = playlist.getPlaylists(user_id, token)
    songs = playlist.getSongInLists(playlists, token)
    artists = playlist.getArtistInLists(playlists, token)
    genres = playlist.getArtistGenre(artists, token)

    path = os.path.join(app.root_path, 'txt/')
    playlist_fn = str(uuid.uuid4()) + '_playlists.txt'
    songs_fn = str(uuid.uuid4()) + '_songs.txt'
    artists_fn = str(uuid.uuid4()) + '_artists.txt'
    genre_fn = str(uuid.uuid4()) + '_genre.txt'
    np.savetxt((path + playlist_fn), playlists, delimiter=" ", fmt="%s")
    np.savetxt((path + songs_fn), songs, delimiter=" ", fmt="%s")
    np.savetxt((path + artists_fn), artists, delimiter=" ", fmt="%s")
    np.savetxt((path + genre_fn), genres, delimiter=" ", fmt="%s")
    
    current_user.playlists = playlist_fn
    current_user.songs = songs_fn
    current_user.artists = artists_fn
    current_user.genres = genre_fn

    db.session.commit()
    print('data recieved')
    return jsonify(status='Spotify Data Recieved')


#init flask app
app = create_app()
db = SQLAlchemy(app)
db.init_app(app)

if __name__ == '__main__':
    #create database when runnning the app
    # db.create_all(app=create_app())
    db.init_app(app=create_app())
    app.run(debug=True)