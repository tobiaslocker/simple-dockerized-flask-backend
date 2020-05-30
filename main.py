#!/usr/bin/env python
from flask import jsonify, make_response
from app import create_app
import logging

app = create_app()
logger = app.logger

@app.route('/')
def hello():
    logger.debug('hello()')
    return make_response(jsonify({
        'Response from Flask': 'Hello, World!'
        }), 200)
