from flask import Flask
import logging
from flask_cors import CORS
from .models import db
from . import config
import time

cors = CORS()

def create_app():

    # initialization
    app = Flask(__name__)
    cors.init_app(app)
    app.logger.setLevel(logging.DEBUG)

    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.app_context().push()

    db_not_ready = True
    attempt = 1
    while db_not_ready:
        try:
            app.logger.info(f'Connect to Database... (attempt {attempt})')
            attempt += 1
            db.init_app(app)
            db.create_all()
            db_not_ready = False
            app.logger.info('Done!')
        except Exception as e:
            app.logger.warning(f'Could not connect to database, retrying in 5s {e}')
            time.sleep(5)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
