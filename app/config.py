import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')