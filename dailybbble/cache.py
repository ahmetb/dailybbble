# coding=utf-8

import os
import pylibmc

CACHE_SERVERS = 'MEMCACHIER_SERVERS'
CACHE_USERNAME = 'MEMCACHIER_USERNAME'
CACHE_PASSWORD = 'MEMCACHIER_PASSWORD'


CACHE_SERVERS_SEPARATOR = ','


def __get_client():
    """returns memcache client if environment is configured
    `None` if env is not configured for cache
    """
    env = os.environ

    if CACHE_SERVERS in env:
        username = env[CACHE_USERNAME] if CACHE_USERNAME in env else None
        password = env[CACHE_PASSWORD] if CACHE_PASSWORD in env else None
        servers = env[CACHE_SERVERS].split(CACHE_SERVERS_SEPARATOR)
        return pylibmc.Client(servers, username=username, password=password,
                              binary=True)
    else:
        # no environment config found
        return None


def set(key, value, ttl_secs=0):
    """Sets key to value if cache client is configured.
    Does not throw error upon cache service failures.

    Return: success
    """
    c = __get_client()
    if c:
        try:
            return c.set(key, value, time=ttl_secs)
        except:
            return False


def get(key):
    """Gets value of key if cache client is configured and key exists
    as non-expired. Does not throw error upon cache service failures.

    Return: value or None
    """

    c = __get_client()
    if c:
        try:
            return c.get(key)
        except:
            return None
