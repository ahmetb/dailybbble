# coding=utf-8

import datetime
import service
import json
from dateutil import parser
from dailybbble import app
from flask import jsonify


@app.route('/api/1/popular/day/<day>')
def api_popular_day(day):
    if day == 'today':
        date = datetime.datetime.utcnow().date()
    else:
        try:
            date = parser.parse(day).date()
        except:
            return render_api_error('Invalid date format given.'), 400

    try:
        shots = service.popular_shots_of_day(date, 20)
        return render_api_result(shots)
    except Exception as e:
        return render_api_error('Internal error occurred')
    

def base_api_response():
    return {}


def render_api_result(result_object):
    resp = base_api_response()
    resp['result'] = result_object
    return jsonify(**resp)


def render_api_error(error_message, error_type=None, error_code=None):
    error = {'message': error_message, 'type': error_type, 'code': error_code}
    resp = base_api_response()
    resp['error'] = error
    return jsonify(**resp)
