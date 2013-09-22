# coding=utf-8

import dribbble


def get_popular_shots():
    resp = dribbble.shots('popular')()

    if 'shots' in resp:
        return resp['shots']
