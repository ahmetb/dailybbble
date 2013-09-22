# coding=utf-8

import os
import requests
import json

SENDGRID_USERNAME = 'SENDGRID_USERNAME'
SENDGRID_PASSWORD = 'SENDGRID_PASSWORD'
SENDGRID_LIST_NAME = 'SENDGRID_LIST_NAME'

SUBSCRIBE_URI = 'https://sendgrid.com/api/newsletter/lists/email/add.json'


def get_sendgrid_credentials():
    """reads SendGrid credentials from environment

    return; username, password, list_name
    """

    env = os.environ
    if SENDGRID_USERNAME not in env or SENDGRID_PASSWORD not in env or \
            SENDGRID_LIST_NAME not in env:
        raise Exception('SendGrid credentials are not configured properly')
    return env[SENDGRID_USERNAME], env[SENDGRID_PASSWORD],\
        env[SENDGRID_LIST_NAME]


def add_subscriber(email):
    """adds subscriber to list configured in env var SENDGRID_LIST_NAME
    True if successful, False otherwise
    """
    username, password, list_name = get_sendgrid_credentials()
    data = json.dumps({'email': email, 'name': None})
    params = {'api_user': username, 'api_key': password, 'list': list_name,
              'data': data}
    try:
        r = requests.get(SUBSCRIBE_URI, params=params)
        return r.status_code / 100 == 2
    except:
        return False
