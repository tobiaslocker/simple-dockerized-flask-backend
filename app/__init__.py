from flask import Flask
import logging
from flask_cors import CORS
from .models import db
from . import config

cors = CORS()

def create_app():

    # initialization
    app = Flask(__name__)
    cors.init_app(app)
    app.logger.setLevel(logging.DEBUG)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.app_context().push()

    db.init_app(app)
    db.create_all()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
