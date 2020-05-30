#!/usr/bin/env python
from flask import jsonify, make_response
from app import create_app
import logging

app = create_app()
logger = app.logger
API_VERSION = 'v1.0'


@app.route('/api/{}/resource'.format(API_VERSION))
def resource():
    logger.debug('resource()')
    return make_response(jsonify({
        'Response from Flask': 'Hello, World!'
        }), 200)
