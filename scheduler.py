#!/usr/bin/python
import schedule
import time
from sktimeline import *

def start_populate_new_items():
    print 'running start_populate_new_items'
    TwitterFeedSetting.start_populate_new_items()
    GithubFeedSetting.start_populate_new_items()
    SlackFeedSetting.start_populate_new_items()
    return

def update_items():
    print 'running update_items'
    TwitterFeedSetting.update_items()
    GithubFeedSetting.update_items()
    SlackFeedSetting.update_items()
    return

# update things marked as "new" every minute
schedule.every(1).minutes.do(start_populate_new_items)

# do an update for things already in the db every 15 minutes
schedule.every(15).minutes.do(update_items)

#todo: do we need to look into threading these?

def run_schedule():
    print 'starting scheduler process'
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_schedule()
