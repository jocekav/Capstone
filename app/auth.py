from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
from spotifyLogin import getAuth

auth = Blueprint('auth', __name__)

@auth.route("/callback/")
def callback():
    print('spotify')
    return redirect(getAuth())

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':    
        return render_template('login.html')
    else:
        # if the request is POST the we check if the user exist 
          # and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it     
        # to the hashed password in the database
        if not user:
            # flash('Please sign up before!')
            print('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            # flash('Please check your login details and try again.')
            print('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user 
               #doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the 
        # right credentials
        login_user(user, remember=remember)
        return redirect(getAuth())
        # return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            # flash('Email already exists')
            print('email already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, name=name,
                        password=generate_password_hash(password,
                        method='sha256'), location='blank', preference='blank', age='blank')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))