__author__ = 'stonex'

# from DBSetting import db #, delete_notification_records
import time
import multiprocessing
from datetime import timedelta
from pymongo import MongoClient
import json
# import sys
# from itertools import product

# connection details
# connection_string = raw_input("Plesse enter the connection string: i.e mongodb://192.168.4.86:27017/ : ")

client = MongoClient('mongodb://192.168.4.86:27017/')
db = client['mobapi']

# users = db['users_live']
notifications = db['notification_live_copy']

total_notifications = notifications.count()
notification_counter = 1
start_time = time.time()
for notification in notifications.find():
    msg_type = json.loads(notification['msg'])['type']

    # updating msg type to action field
    notification.update({'action': msg_type})
    notification_obj_id = notifications.save(notification)
    print " Updating notification: ", notification_counter,\
        "notification object id: ", notification_obj_id,\
        " total notifications: ", total_notifications
    notification_counter += 1

end_time = time.time()

time_taken = end_time - start_time
print "Time taken (in secs): ", time_taken

a = timedelta(seconds=time_taken)
time_string = "\nTime taken: %d days %02d:%02d:%02d" % (a.days, a.seconds / 3600, (a.seconds / 60) % 60, a.seconds % 60)
print time_string