# coding=utf-8

import datetime
from . import service
import json
from dateutil import parser
from dailybbble import app
from flask import jsonify


@app.route('/api/1/popular/day/<day>', methods=['GET', 'HEAD'])
def api_popular_day(day):
    if day == 'today':
        date = datetime.datetime.utcnow().date()
    else:
        try:
            date = parser.parse(day).date()
        except ValueError as e:
            return render_api_error('Invalid date format given.'), 400

    try:
        shots = service.popular_shots_of_day(date, 20)
        return render_api_result(shots), 200
    except Exception as e:
        print e
        return render_api_error('Internal error occurred'), 500


@app.route('/api/1/popular/month/<month>', methods=['GET', 'HEAD'])
def api_popular_month(month):
    try:
        y, m = month.split('-')
        if not y or not m:
            raise ValueError()
    except ValueError as e:
        return render_api_error('Invalid date format given.'), 400

    try:
        shots = service.popular_shots_of_month(y, m, 20)
        return render_api_result(shots), 200
    except Exception as e:
        print e
        return render_api_error('Internal error occurred'), 500


def base_api_response():
    return {}


def render_api_result(result_object):
    resp = base_api_response()
    resp['result'] = result_object
    return jsonify(**resp)


def render_api_error(error_message, error_type=None, error_code=None):
    error = {'message': error_message}
    if error_type:
        error['type'] = error_type
    if error_code:
        error['code'] = error_code

    resp = base_api_response()
    resp['error'] = error
    return jsonify(**resp)
