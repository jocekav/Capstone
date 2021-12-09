from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    preference = db.Column(db.String(1000))
    age = db.Column(db.String(1000))
    image_file = db.Column(db.String(20), default='default.jpg')
    token = db.Column(db.String(1000))
