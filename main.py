#!/usr/bin/env python
from flask_cors import cross_origin
import time
from flask import Flask, abort, request, jsonify, g, make_response
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app, db, auth, cors, util
import logging

app = create_app()
logger = app.logger

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=604800):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])


@auth.verify_password
def verify_password(username_or_token, password):
    logger.debug('verify_password({}, {})'.format(
        username_or_token, password))
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    logger.warning('Unauthorized access from {}'.format(request.remote_addr))
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/api/v1.0/verify_token')
def verify_token():
    logger.debug('verify_token()')
    token = request.args.get('token')
    user = User.verify_auth_token(token)
    if not user:
        abort(401)
    return jsonify({'token': token, 'user': user.username})


@app.route('/api/v1.0/login')
@auth.login_required
@cross_origin()
def get_auth_token():
    logger.debug('get_auth_token()')
    util.download_csv_data()
    token = g.user.generate_auth_token(604800)
    logger.debug('token = {}'.format(token))
    return jsonify({'token': token.decode('ascii'), 'duration': 604800})


@app.route('/api/v1.0/rsl/<string:freq>/<int:ma_period>/<int:year>/<int:week>')
@auth.login_required
@cross_origin()
def rsl_ranking_table(freq, ma_period, year, week):
    week = week - 1
    logger.debug(
            'rsl_ranking_table({}, {}, {}, {})'.format(
                freq, ma_period, year, week))
    list_name = request.args.get('securities_list')
    securities = util.load_securities_list(list_name)
    logger.debug(
            'securities = {}'.format(securities))
    try:
        monday, friday = util.monday_and_friday_of_week(year, week)
        start = monday.strftime("%Y-%m-%d")
        end = friday.strftime("%Y-%m-%d")
        response = util.rsl_ranking(
                freq, ma_period, securities, start, end).to_json()
        return response
    except Exception as e:
        logger.warning(e)
    return make_response(jsonify({'error': 'Invalid'}), 400)


@app.route('/api/v1.0/rsl_comparison/<string:date>')
@auth.login_required
@cross_origin()
def rsl_comparison(date):
    logger.debug('rsl_comparison(%s)' % date)
    list_name = request.args.get('securities_list')
    securities = util.load_securities_list(list_name)
    logger.debug('securities = {}'.format(securities))
    timedelta = request.args.get('timedelta')
    logger.debug('timedelta = {} ({})'.format(timedelta, type(timedelta)))
    try:
        table = util.make_rsl_comparison_table(
                date, securities, delta=int(timedelta))
        logger.debug('\n{}'.format(table))
        return table.to_json()
    except Exception as e:
        logger.warning(e)
    return make_response(jsonify({'error': 'Invalid'}), 400)


@app.route('/api/v1.0/last_date')
@auth.login_required
@cross_origin()
def last_date():
    logger.debug('last_date()')
    df = util.read_rsl_csv('daily', 20)
    last = df.index[-2].strftime("%Y-%m-%d")
    logger.debug('last date = %s' % last)
    return make_response(jsonify({'lastDate': last}), 200)
