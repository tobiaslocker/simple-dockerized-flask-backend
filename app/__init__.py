from flask import Flask
import logging
from flask_cors import CORS

cors = CORS()

def create_app():

    # initialization
    app = Flask(__name__)
    cors.init_app(app)
    app.logger.setLevel(logging.DEBUG)

    return app
