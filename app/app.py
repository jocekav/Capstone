from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager

import os
import re

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# def create_app():

app = Flask(__name__)

app.config.from_object(Config)

DB_URI = app.config['SQLALCHEMY_DATABASE_URI']

# rest of connection code using the connection string `uri`
# db = SQLAlchemy(app)
# engine = create_engine(DB_URI)
# app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# db.init_app(app)

login_manager = LoginManager() # Create a Login Manager instance
login_manager.login_view = 'auth.login' # define the redirection 
                        # path when login required and we attempt 
                        # to access without being logged in
login_manager.init_app(app) # configure it for login

from app.models import User
@login_manager.user_loader
def load_user(user_id): #reload user object from the user ID 
                        #stored in the session
    # since the user_id is just the primary key of our user 
    # table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from app.main import main_bp as main_blueprint
app.register_blueprint(main_blueprint)

from app.match import match as match_blueprint
app.register_blueprint(match_blueprint)

db = SQLAlchemy(app)
db.init_app(app)


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    DB_URI = app.config['SQLALCHEMY_DATABASE_URI']

    # rest of connection code using the connection string `uri`
    # db = SQLAlchemy(app)
    # engine = create_engine(DB_URI)
    # app.config['SECRET_KEY'] = 'secret-key-goes-here'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # db.init_app(app)

    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection 
                            # path when login required and we attempt 
                            # to access without being logged in
    login_manager.init_app(app) # configure it for login

    from models import User
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID 
                            #stored in the session
        # since the user_id is just the primary key of our user 
        # table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from match import match as match_blueprint
    app.register_blueprint(match_blueprint)

    return app