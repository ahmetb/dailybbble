# coding=utf-8

import datetime
import service
from feedformatter import Feed
from pytz import timezone, UTC
from flask import render_template


DAYS_BACK = 3
SHOTS_PER_DAY = 6
POST_NEW_ITEM_AT = datetime.time(9, 00)  # PST
POST_NEW_ITEM_AT_TZ = 'US/Pacific'


FEED_TITLE = 'Dailybbble Popular Designs'
FEED_DESCRIPTION = 'Popular shots at Dribbble every day'
FEED_AUTHOR = 'Dailybbble'


def get_feed(url_home, url_day):
    feed = Feed()

    feed.feed["title"] = FEED_TITLE
    feed.feed["link"] = url_home()
    feed.feed["description"] = FEED_DESCRIPTION
    feed.feed["author"] = FEED_AUTHOR

    tz = timezone(POST_NEW_ITEM_AT_TZ)
    now = datetime.datetime.now(tz)
    today = now.date()

    if now.time() < POST_NEW_ITEM_AT:  # don't post today's item yet
        today = today - datetime.timedelta(days=1)

    for i in range(1, DAYS_BACK+1):
        date = today - datetime.timedelta(days=i)
        shots = service.popular_shots_of_day(date, SHOTS_PER_DAY)

        if not shots:  # skip the day if no shots are recorded
            continue

        pubDate = datetime.datetime(date.year, date.month, date.day,
                                    POST_NEW_ITEM_AT.hour,
                                    POST_NEW_ITEM_AT.minute,
                                    POST_NEW_ITEM_AT.second,
                                    tzinfo=tz)
        pubDate = pubDate + datetime.timedelta(days=1)

        item = {
            "title": "Popular designs of {0}".format(date.strftime("%b %d")),
            "link": url_day(date),
            "pubDate": pubDate.astimezone(UTC).timetuple(),
            "guid": url_day(date),
            "description": render_template('feed/shots.html', shots=shots,
                                           date=date)
        }
        feed.items.append(item)

    return feed
