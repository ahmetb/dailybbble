# coding=utf-8

from dailybbble import app
from flask import url_for, Response
import feed


def url_home():
    return url_for('home',  _external=True)


def url_for_day(date):
    return url_for('archive_day', year=date.year, month=date.month,
                   day=date.day, _external=True)


@app.route('/feed/rss.xml')
def rss2():
    rss = feed.get_feed(url_home, url_for_day).format_rss2_string(pretty=True)
    return Response(rss, mimetype='text/xml')
