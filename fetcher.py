#!/usr/bin/python
# coding=utf-8

import time
from dailybbble import dribbble_service
from dailybbble  import database
from dailybbble  import model
from datetime import datetime

"""
Continuously running process for regularly downloading and saving shots
"""


INTERVAL_SECS = 1 * 60 * 60


def main():
    database.create_initial_schema()
    while True:
        try:
            shots = dribbble_service.get_popular_shots()
            for shot_resp in shots:
                shot_model = model.shot_to_record(shot_resp)
                database.upsert_shot(shot_model)
            print '[{0}] Processed {1} posts.'.format(datetime.utcnow(),
                                                      len(shots))
        except Exception as e:
            print '[{0}] Error: {1}'.format(datetime.utcnow(), e)
        time.sleep(INTERVAL_SECS)

if __name__ == '__main__':
    main()
