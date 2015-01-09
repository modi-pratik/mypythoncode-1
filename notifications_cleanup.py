from DBSetting import db #, delete_notification_records
import time
import multiprocessing
# from itertools import product
# from pymongo import MongoClient


# Following are settings variables for script
no_min_notifications = 20
days_in_seconds = 604800
timestamp_days_back = int(time.time()) - days_in_seconds

users = db['users']
notifications = db['notifications_copy']


def delete_notification_records(arg_username):
    # import ipdb
    # ipdb.set_trace()
    # client = MongoClient('mongodb://192.168.4.86:27017/')
    # conn = pymongo.Connection('192.168.4.86')

    # connecting to db
    # db = client['mobapi']
    # notifications = db['notifications_copy']

    # try to built here dict so that at delete loop will be faster one
    op_result_inter = notifications.find({'to': arg_username}).skip(20).sort('created', -1)
    # op_result_inter = notifications.find({'to': arg_username,
    #  'created': {'$lte': arg_timestamp}}).skip(20).sort('created', 1)

    for record in op_result_inter:
        # notifications.remove({'_id': record['_id']})
        print record
    # print op_result_inter
    # print op_result_inter
    # return op_result_inter


if __name__ == "__main__":
    no_of_processes = int(raw_input("Please enter the number of processes you want to run: "))
    pool = multiprocessing.Pool(processes=no_of_processes)
    user_list = []
    for user in users.find():
        username = user['username']
        user_notification_count = notifications.find({'to': username}).count()
        # case 1: get users who's notifications are gt then 20
        if user_notification_count > no_min_notifications:
            # case 2: for selected user get the older data more then 7 days
            # result = delete_notification_records(username, timestamp_days_back)
            user_list.append(username)
            # import ipdb
            # ipdb.set_trace()
            # pool.map(delete_notification_records, username)
            # print len([x for x in result])

    # map(delete_notification_records, user_list)
    # reuslt = [pool.apply(delete_notification_records, args=(x,)) for x in user_list]
    pool.map(delete_notification_records, user_list)
