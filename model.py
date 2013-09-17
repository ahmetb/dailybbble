# coding=utf-8

from dateutil import parser


def shot_to_record(shot):
    """
    Returns dictionary for Azure Table record from shot dictionary from API
    result.

    Strips down some unecessary details from original object and sets
    PartitionKey and RowKey for Azure Table Storage.
    """

    d = dict()
    d['id'] = shot['id']
    d['created'] = parser.parse(shot['created_at']).isoformat()
    d['created_day'] = str(parser.parse(shot['created_at']).date())
    d['title'] = shot['title']

    d['url'] = shot['url']
    d['short_url'] = shot['short_url']

    d['user_id'] = shot['player']['id']
    d['user_name'] = shot['player']['username']
    d['user_display_name'] = shot['player']['name']
    d['user_avatar'] = shot['player']['avatar_url']
    d['user_url'] = shot['player']['url']

    d['image_teaser_url'] = shot['image_teaser_url']
    d['image_url'] = shot['image_url']

    d['views'] = shot['views_count']
    d['likes'] = shot['likes_count']
    d['comments'] = shot['comments_count']

    d['width'] = shot['width']
    d['height'] = shot['height']

    d['PartitionKey'] = d['created_day']
    d['RowKey'] = d['id']

    return d
