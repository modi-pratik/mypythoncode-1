__author__ = 'stonex'

from DBSetting import db #, delete_notification_records
import time
import multiprocessing
# from itertools import product
# from pymongo import MongoClient


# Following are settings variables for script
no_min_notifications = 20
days_in_seconds = 604800
timestamp_days_back = int(time.time()) - days_in_seconds

users = db['users_live']
notifications = db['notification_live_copy']


if __name__ == '__main__':
    # use aggregate function to create temp collection for given user and then remove all the entry in old collection
    # then insert the temp collection back in old collection for current user and then move next user
    counter = 0
    start_time = time.time()

    for user in users.find():
        username = user['username']

        # import ipdb
        # ipdb.set_trace()
        print "\n\n\nusername: ", username, " user count:", counter
        user_notifications_total_count = notifications.find({'to': username}).count()
        user_notifications_week_count = notifications.find({'to': username,
                                                            'created': {'$lte': timestamp_days_back}}).count()

        if user_notifications_total_count == 0:
            print "\nusername: ", username, " has no notifications"

        elif user_notifications_week_count > no_min_notifications:
            remove_result = notifications.remove({'created': {'$lte': timestamp_days_back}})
            print "\nusername: ", username, "remove result: ", remove_result

        elif user_notifications_week_count < no_min_notifications:

            # creating temp collection for selection
            result = notifications.aggregate(({'$match': {'to': username}}, {'$sort': {'created': -1}}, {'$limit': 20},
                                              {'$out': 'latest_20_notification_tmp'}))
            print "\nresult of aggregate latest_20_notification_tmp: ", result

            # removing all the records form main collection for current username
            remove_result = notifications.remove({'to': username})

            # insert each record from new temp collection to main collection
            latest_20_notification_tmp = db['latest_20_notification_tmp']
            for record in latest_20_notification_tmp.find():
                notifications.insert(record)
                print "\nnotification inserted back for user: ", username, " record objId: ", record['_id']

        counter += 1

    end_time = time.time()
    print "total time take in secs: ", (end_time - start_time)