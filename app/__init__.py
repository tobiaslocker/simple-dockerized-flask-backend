from flask import Flask
import logging

def create_app():

    # initialization
    app = Flask(__name__)
    app.logger.setLevel(logging.DEBUG)

    return app
