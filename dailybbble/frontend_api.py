# coding=utf-8

import datetime
import service
from dateutil import parser
from dailybbble import app


@app.route('/api/1/popular/day/<day>')
def api_popular_day(day):
    if day == 'today':
        date = datetime.datetime.utcnow().date()
    else:
        try:
            date = parser.parse(day).date()
        except:
            return render_api_error('Invalid date format given.'), 400
    shots = service.popular_shots_of_day(day, 20)
    return str(shots)


def render_api_error(message):
    return message # TODO json
