from flask import Blueprint, make_response, jsonify
from flask_cors import cross_origin

import logging
logging.basicConfig(level=logging.DEBUG)

api = Blueprint('api', __name__)

@api.route('/resource')
@cross_origin()
def resource():
    logging.debug('resource()')
    return make_response(jsonify({
        'Response': 'Hello, World!'
        }), 200)

