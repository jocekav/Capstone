from posixpath import join
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

import playlist

match = Blueprint('match', __name__)
global user_count
user_count = 0

@match.route('/matches', methods=['GET', 'POST'])
def matches():
    global user_count
    users = User.query.all()
    total_users = len(users) - 1
    print(total_users)
    # if request.method == 'GET':
    user_count = (user_count) % total_users + 1
    if current_user.id == user_count:
        user_count = (user_count) % total_users + 1
    name = users[user_count].name
    location = users[user_count].location
    preference = users[user_count].preference
    age = users[user_count].age
    picture = users[user_count].image_file
    picture = 'static/' + picture
    
    user1_songfile = 'txt/' + current_user.songs
    user1_artistfile = 'txt/' + current_user.artists
    user1_genrefile = 'txt/' + current_user.genres
    
    user2_songfile = 'txt/' + users[user_count].songs
    user2_artistfile = 'txt/' + users[user_count].artists
    user2_genrefile = 'txt/' + users[user_count].genres

    match_score = playlist.matchsummary(user1_songfile, user2_songfile, user1_artistfile, user2_artistfile, user1_genrefile, user2_genrefile)
    print(match_score)
    match_score = round(match_score * 100)
    print(user_count)
    return render_template('match.html', name=name, location=location, preference=preference, age=age, image_file=picture, score=match_score)

@match.route('/player', methods=['GET', 'POST'])
def player():
    global user_count
    users = User.query.all()
    name = users[user_count].name

    user1_songfile = 'txt/' + current_user.songs
    user1_artistfile = 'txt/' + current_user.artists
    
    user2_songfile = 'txt/' + users[user_count].songs
    user2_artistfile = 'txt/' + users[user_count].artists

    joint_playlist = playlist.jointPlaylistV2(user1_songfile, user2_songfile, user1_artistfile, user2_artistfile)

    # if len(joint_playlist) >= 100:
    #     joint_playlist = joint_playlist[:100]

    front = 'spotify:track:'
    song_titles = []
    for i in range(len(joint_playlist)):
        joint_playlist[i] = front + joint_playlist[i]
        song_titles.append(playlist.getSongInfo(current_user.token, joint_playlist[i]))

    playlist_id = playlist.create_playlist(current_user.token, current_user.spotify_id, name, joint_playlist)
    print(playlist_id)
    print(song_titles)

    spotify_uri = 'https://open.spotify.com/embed/playlist/' + playlist_id + '?utm_source=generator&theme=0'
    # return render_template('player.html', token=current_user.token, name=name, user_id=current_user.spotify_id, uris=joint_playlist, song_titles=song_titles)
    # return render_template('player.html', spotify_uri=spotify_uri, name=name)
    return render_template('player.html', spotify_uri=spotify_uri, name=name, song_titles=song_titles)