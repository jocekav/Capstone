from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db

match = Blueprint('match', __name__)

@match.route('/matches', methods=['GET', 'POST'])
def matches():
    user_count = 0
    users = User.query.all()
    # if request.method == 'GET':
    name = users[user_count].name
    location = users[user_count].location
    preference = users[user_count].preference
    age = users[user_count].age
    picture = users[user_count].image_file
    return render_template('match.html', name=name, location=location, preference=preference, age=age, image_file=picture)
    # else:
    #     # if the request is POST the we check if the user exist 
    #       # and with te right password
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     remember = True if request.form.get('remember') else False
    #     user = User.query.filter_by(email=email).first()
    #     # check if the user actually exists
    #     # take the user-supplied password, hash it, and compare it     
    #     # to the hashed password in the database
    #     if not user:
    #         # flash('Please sign up before!')
    #         print('Please sign up before!')
    #         return redirect(url_for('auth.signup'))
    #     elif not check_password_hash(user.password, password):
    #         # flash('Please check your login details and try again.')
    #         print('Please check your login details and try again.')
    #         return redirect(url_for('auth.login')) # if the user 
    #            #doesn't exist or password is wrong, reload the page
    #     # if the above check passes, then we know the user has the 
    #     # right credentials
    #     login_user(user, remember=remember)
    #     return redirect(getAuth())
    #     # return redirect(url_for('main.profile'))
