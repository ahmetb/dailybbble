# coding=utf-8

import database


"""
Provides information from database to front-end methods by adding a
caching layer
"""


def popular_shots_of_day(day, count):
    return database.popular_shots_of_day(day, count)


def popular_shots_of_month(date, count):
    return database.popular_shots_of_month(date, count)