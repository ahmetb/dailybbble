#!/usr/bin/python
# coding=utf-8

import time
import service
import database
import model
from datetime import datetime

"""
Continuously running process for regularly downloading and saving shots
"""


def main():
    database.create_initial_schema()
    while True:
        try:
            shots = service.get_popular_shots()
            for shot_resp in shots:
                shot_model = model.shot_to_record(shot_resp)
                print shot_model['created']
                #database.upsert_shot(shot_model)
            print '[{0}] Processed {1} posts.'.format(datetime.utcnow(), len(shots))
        except Exception as e:
            print '[{0}] Error: {1}'.format(datetime.utcnow(), e)
        time.sleep(1* 60 * 60)

if __name__ == '__main__':
    main()
