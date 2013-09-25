# coding=utf-8

import os
import requests
import json

ENV_SENDGRID_USERNAME = 'SENDGRID_USERNAME'
ENV_SENDGRID_PASSWORD = 'SENDGRID_PASSWORD'
ENV_SENDGRID_LIST_NAMES = 'SENDGRID_LIST_NAMES'
ENV_SENDGRID_SENDER_NAME = 'SENDGRID_SENDER_NAME'

SUBSCRIBE_URI = 'https://sendgrid.com/api/newsletter/lists/email/add.json'
EMAIL_ADD_URI = 'https://sendgrid.com/api/newsletter/add.json'
SET_RECIPIENTS_URI = 'https://sendgrid.com/api/newsletter/recipients/add.json'
SCHEDULE_EMAIL_URI = 'https://sendgrid.com/api/newsletter/schedule/add.json'

DAILY_OPTION = 'daily'
WEEKLY_OPTION = 'weekly'


def get_api_credentials():
    """reads SendGrid credentials from environment

    return: username, password
    """

    env = os.environ
    if ENV_SENDGRID_USERNAME not in env or ENV_SENDGRID_PASSWORD not in env:
        raise Exception('SendGrid credentials are not configured properly')
    return env[ENV_SENDGRID_USERNAME], env[ENV_SENDGRID_PASSWORD]


def get_email_list_names():
    """reads recipient list names from environment

    return: list([daily_list, weekly_list])
    """

    env = os.environ
    if ENV_SENDGRID_LIST_NAMES not in env:
        raise Exception('SendGrid list names are not configured properly')
    return env[ENV_SENDGRID_LIST_NAMES].split(',')


def get_sender_identity():
    """reads sender identity name from environment
    """
    env = os.environ
    if ENV_SENDGRID_SENDER_NAME not in env:
        raise Exception('SendGrid sender identity name is not configured')
    return env[ENV_SENDGRID_SENDER_NAME]


def add_subscriber(email, list_name):
    """adds subscriber to specified list name (as appears in SendGrid website)
    True if successful (or user already subscribed), False otherwise
    """
    username, password = get_api_credentials()
    data = json.dumps({'email': email, 'name': None})
    params = {'api_user': username, 'api_key': password, 'list': list_name,
              'data': data}
    try:
        r = requests.get(SUBSCRIBE_URI, params=params)
        return r.status_code / 100 == 2
    except:
        return False


def create_email(email_name, sender, subject, text, html):
    """creates a new marketing email with given name

    sender: registered sender address
    """

    username, password = get_api_credentials()
    params = {'identity': sender, 'name': email_name, 'subject': subject,
              'text': text, 'html': html, 'api_user': username,
              'api_key': password}
    try:
        r = requests.get(EMAIL_ADD_URI, params=params)
        return r.json() and r.json()['message'] == 'success'
    except Exception as e:
        return False


def assign_list(list_name, email_name):
    """assign a recipient list to a marketing email
    """

    username, password = get_api_credentials()
    params = {'api_user': username, 'api_key': password, 'list': list_name,
              'name': email_name}
    try:
        r = requests.get(SET_RECIPIENTS_URI, params=params)
        return r.json() and r.json()['message'] == 'success'
    except Exception as e:
        return False


def schedule_email(email_name):
    """sends email immediately. marketing email with given name
    should be assigned to a recipient list before sending
    """

    username, password = get_api_credentials()
    params = {'api_user': username, 'api_key': password, 'name': email_name}
    try:
        r = requests.get(SCHEDULE_EMAIL_URI, params=params)
        return r.json() and r.json()['message'] == 'success'
    except Exception as e:
        return False
