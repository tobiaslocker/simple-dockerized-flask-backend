from flask import Flask
import logging
from flask_cors import CORS

cors = CORS()

def create_app():

    # initialization
    app = Flask(__name__)
    cors.init_app(app)
    app.logger.setLevel(logging.DEBUG)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
