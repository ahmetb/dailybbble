# coding=utf-8

from azure.storage import TableService
import calendar
import datetime
import os


"""Persistence store implementation with Azure Table Storage
"""


def __table_name():
    """Returns Azure storage table name from environment variable
    """

    if not 'AZURE_TABLE_NAME' in os.environ:
        raise Exception('Azure table name not configured in environment var.')
    return os.environ['AZURE_TABLE_NAME']


def __get_conn():
    """Returns connection handle for Table Storage API
    """

    env_account_name = 'AZURE_ACCOUNT_NAME'
    env_account_key = 'AZURE_ACCOUNT_KEY'
    env = os.environ
    if env_account_name not in env or env_account_key not in env:
        raise Exception('Environment vars not configured for Azure storage')

    return TableService(env[env_account_name], env[env_account_key])


def create_initial_schema():
    """Creates table on Azure Table Storage
    """
    conn = __get_conn()
    conn.create_table(__table_name(), fail_on_exist=False)


def insert_shot(shot):
    """Inserts record to table storage. Fails if shot exists upon insert

        shot: has PartitionKey and RowKey set.
    """
    return __get_conn().insert_entity(__table_name(), shot)


def upsert_shot(shot):
    """Upserts record to table storage. Returns response from API.

        shot: has PartitionKey and RowKey set.
    """
    return __get_conn().insert_or_replace_entity(__table_name(),
                                                 shot['PartitionKey'],
                                                 shot['RowKey'], shot)


def get_shot(shot):
    """Retrieves shot object from database and returns as dictionary.
    Raises exception if shot is not found.
    """
    return __get_conn().get_entity(__table_name(),
                                   shot['PartitionKey'], shot['RowKey'])


def update_shot(id, shot):
    """Updates record with specified id with given shot dictionary
    """

    return __get_conn().get_entity(__table_name(),
                                   shot['PartitionKey'], shot['RowKey'])


def popular_shots_of_day(day, count=20):
    """Returns shot records list of a specified day (optionally of given max
    size) as dict

    day: datetime.date of day requested
    count: max shots to return after sorting by popularity
    """

    query = "PartitionKey eq '{0}'".format(str(day))
    return __get_popular_shots(query, count)


def popular_shots_of_month(year, month, count=20, min_likes=50):
    """Returns shot records list of a specified day (optionally of given max
    size) as dict

    count: max shots to return after sorting by popularity
    min_likes: minimum likes (best-effort to workaround azure table response
        1000 rows limit in a single request)
    """
    month_range = calendar.monthrange(year, month)
    dt_start = datetime.date(year, month, 1)
    dt_end = datetime.date(year, month, month_range[1])
    query = "PartitionKey ge '{0}' and PartitionKey le '{1}' and likes gt {2}"\
            .format(dt_start, dt_end, min_likes)
    return __get_popular_shots(query, count)


def __get_popular_shots(query_filter, count):
    """Queries shots from database from filter
    and sorted by popularity (in descending order) of given max size (`count`)
    """

    records = __get_conn().query_entities(__table_name(), filter=query_filter)
    records = [r.__dict__ for r in records]
    for r in records:  # remove azure-table entity clutters
        del r['PartitionKey']
        del r['RowKey']
        del r['etag']
    # TODO cache <query_filter:records> here
    records = sorted(records, key=lambda s: s['likes'], reverse=True)
    return records[:count]
