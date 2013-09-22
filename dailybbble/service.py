# coding=utf-8

import database
import cache

"""
Provides information from database to front-end methods by adding a
caching layer
"""


CACHE_TTL_MINS = 30


def popular_shots_of_day(day, count):
    cache_key = 'popular_{0}#{1}'.format(day, count)

    cached = cache.get(cache_key)
    if cached:
        return cached

    shots = database.popular_shots_of_day(day, count)

    if shots:
        cache.set(cache_key, shots, CACHE_TTL_MINS*60)
    return shots


def popular_shots_of_month(year, month, count):
    cache_key = 'popular_{0}-{1}#{2}'.format(year, month, count)
    cached = cache.get(cache_key)
    if cached:
        return cached

    shots = database.popular_shots_of_month(year, month, count)

    if shots:
        cache.set(cache_key, shots, CACHE_TTL_MINS*60)
    return shots
