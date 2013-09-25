#!/usr/bin/python
# coding=utf-8

import os
import sys
import uuid
from datetime import datetime, timedelta
from jinja2 import Environment, PackageLoader
from . import service
from . import email


"""An executable to send out daily/weekly email newsletters
with popular shots. This can be scheduled to run once every day and/or
once every week.
"""

SHOTS_DAILY_MODE = 6
SHOTS_WEEKLY_MODE = 10


def main():
    args = sys.argv
    if len(args) < 2:
        print_usage()
        sys.exit(1)
    opt = sys.argv[1]

    if opt != email.DAILY_OPTION and opt != email.WEEKLY_OPTION:
        print 'Unrecognized email option: {0}'.format(opt)
        print_usage()
        sys.exit(1)

    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    sender = email.get_sender_identity()
    list_name = list_name_for_mode(opt)
    unique_id = str(uuid.uuid1())[:8]
    email_name = 'Dailybbble-{0}-{1}-{2}'.format(opt, today, unique_id)
    subject = email_subject_for_mode(opt, yesterday)
    shots = shots_for_mode(opt)
    email_html, email_txt = email_body(opt, shots)

    success = True
    if not email.create_email(email_name, sender, subject, email_txt,
                              email_html):
        print 'Creating email failed.'
        success = False
    if success and not email.assign_list(list_name, email_name):
        print 'Assigning email list failed.'
        success = False
    if success and not email.schedule_email(email_name):
        print 'Scheduling created email for sending failed.'
        success = False
    else:
        print '[{0}] {1} email sent!'.format(datetime.utcnow(), opt)

    if not success:
        sys.exit(1)


def list_name_for_mode(mode):
    lists = email.get_email_list_names()
    if not lists or len(lists) < 2:
        raise Exception('Email lists are not configured')
    if mode == email.DAILY_OPTION:
        return lists[0]
    elif mode == email.WEEKLY_OPTION:
        return lists[1]
    else:
        raise Exception('Unsupported email mode: "{0}"'.format(mode))


def shots_for_mode(mode):
    if mode == email.DAILY_OPTION:
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        return service.popular_shots_of_day(yesterday, SHOTS_DAILY_MODE)
    elif mode == email.WEEKLY_OPTION:
        raise Exception('Not implemented yet')  # TODO implement service
    else:
        raise Exception('Unsupported email mode: "{0}"'.format(mode))


def email_body(mode, shots):
    """provides email contents rendered in HTML and Plain Text with given
    shots

    return: (html, text)
    """
    templates = list(email_templates_for_mode(mode))
    return tuple(map(lambda tpl: tpl.render(shots=shots), templates))


def email_templates_for_mode(mode):
    """provides unrendered templates for emails
    return: (htmlTemplate, plainTextTemplate)
    """
    env = Environment(loader=PackageLoader('dailybbble', 'templates/email'))
    return env.get_template('shots.html'), env.get_template('shots.txt')


def email_subject_for_mode(mode, date):
    if mode == email.DAILY_OPTION:
        return 'Popular designs of {0}'.format(date.strftime('%b %d, %A'))
    else:
        raise Exception('Not implemented yet')  # TODO implement service


def print_usage():
    print 'USAGE: {0} OPTION'.format(os.path.basename(sys.argv[0]))
    print '\tSends emails to subscribed users in lists'
    print '\tOPTION: either "{0}" or "{1}"'.format(email.DAILY_OPTION,
                                                   email.WEEKLY_OPTION)


if __name__ == '__main__':
    main()
