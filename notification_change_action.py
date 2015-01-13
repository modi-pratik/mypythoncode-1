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
for notification in notifications.find():
    # obj_id = notification['_id']
    msg_type = json.loads(notification['msg'])['type']
    # updating msg type to action field
    notification.update({'action': msg_type})
    print " Updating notification: ", notification_counter,\
        " total notifications pending: ", (total_notifications - notification_counter)
    notification_counter += 1
