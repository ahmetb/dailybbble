# coding=utf-8

from flask import Flask


app = Flask(__name__)

# circular reference here, however, it is ok
# http://flask.pocoo.org/docs/patterns/packages/
from dailybbble import frontend_web, frontend_api
