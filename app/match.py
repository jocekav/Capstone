from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

match = Blueprint('match', __name__)
global user_count
user_count = 0

@match.route('/matches', methods=['GET', 'POST'])
def matches():
    global user_count
    users = User.query.all()
    total_users = len(users)
    print(total_users)
    # if request.method == 'GET':
    name = users[user_count].name
    location = users[user_count].location
    preference = users[user_count].preference
    age = users[user_count].age
    picture = users[user_count].image_file
    picture = 'static/' + picture
    user_count = (user_count + 1) % total_users
    print(user_count)
    return render_template('match.html', name=name, location=location, preference=preference, age=age, image_file=picture)

@match.route('/player', methods=['GET', 'POST'])
def player():
    global user_count
    users = User.query.all()
    name = users[user_count].name
    # spotify_uri = 'https://open.spotify.com/embed/playlist/4hAJBSW2653wWwxES5F50F?utm_source=generator'
    return render_template('player.html', token=current_user.token, name=name)