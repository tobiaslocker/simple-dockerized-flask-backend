from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import logging

cors = CORS()
db = SQLAlchemy()
auth = HTTPBasicAuth()

def create_app():

    # initialization
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data-dev.sqlite'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)
    cors.init_app(app)
    app.logger.setLevel(logging.DEBUG)

    return app
