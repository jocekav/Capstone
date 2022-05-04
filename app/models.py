from flask_login import UserMixin
from .app import db

USER_ID = db.Sequence('table_id_seq', start=0)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, USER_ID, primary_key=True, server_default=USER_ID.next_value()) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    preference = db.Column(db.String(1000))
    age = db.Column(db.String(1000))
    image_file = db.Column(db.String(20), default='default.jpg')
    token = db.Column(db.String(1000))
    spotify_id = db.Column(db.String(1000))
    playlists = db.Column(db.String(20))
    songs = db.Column(db.String(20))
    artists = db.Column(db.String(20))
    genres = db.Column(db.String(20))
    
