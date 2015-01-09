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


def delete_notification_records(arg_username):
    # try to built here dict so that at delete loop will be faster one
    # op_result_inter = notifications.remove({'to': arg_username, 'created': {'$lte': arg_timestamp}})
    op_result_inter = notifications.find({'to': arg_username, 'created': {'$lte': timestamp_days_back}})
    print "for user: ", arg_username, " total notification deleted: ", op_result_inter
    # op_result_inter = notifications.find({'to': arg_username,
    #  'created': {'$lte': arg_timestamp}}).skip(20).sort('created', 1)

    # for record in op_result_inter:
    #     notifications.remove({'_id': record['_id']})
    # return op_result_inter


# def delete_notification_records_crx(notification_crx):
#     # try to built here dict so that at delete loop will be faster one
#     # op_result_inter = notifications.remove({'to': arg_username, 'created': {'$lte': arg_timestamp}})
#     # op_result_inter = notifications.find({'to': arg_username, 'created': {'$lte': timestamp_days_back}})
#     op_result_inter = notification_crx.remove()
#     # print "for user: ", arg_username, " total notification deleted: ", op_result_inter
#     # op_result_inter = notifications.find({'to': arg_username,
#     #  'created': {'$lte': arg_timestamp}}).skip(20).sort('created', 1)
#
#     # for record in op_result_inter:
#     #     notifications.remove({'_id': record['_id']})
#     # return op_result_inter

#  delete notifications for all users where created timestamp is less( older data ) then 7 days
#  and notification count is more 20 for created timestamp is greater then 7 days
#

if __name__ == "__main__":
    # no_of_processes = int(raw_input("Please enter the number of processes you want to run: "))
    # no_of_processes = 1
    # pool = multiprocessing.Pool(processes=no_of_processes)
    start_time = time.time()
    user_list = []
    counter = 1
    for user in users.find():
        username = user['username']
        print "\n\n\n\n username :", username, "counter: ", counter

        # import ipdb
        # ipdb.set_trace()
        # total notifications count
        notifications_count = notifications.find({'to': username}).count()
        # count the no of counts for last 7 days
        user_notification_count_week = notifications.find({'to': username, 'created': {'$gte': timestamp_days_back}}).count()

        if notifications_count == 0:
            print "\n\n for user: ", username, " there is no notifications"

        elif user_notification_count_week == 0 and notifications_count > no_min_notifications:
            # no notifiacation in last 7 days, so pull past notifications and keep 20 and delete rest
            # import ipdb
            # ipdb.set_trace()
            user_notification_count_whole = notifications.find({'to': username}).sort('created',-1).skip(20).count()
            user_notifications = notifications.find({'to': username }).sort('created',-1).skip(20)
            # import ipdb
            # ipdb.set_trace()
            for record in user_notifications:
                # remove = notifications.find({'_id': record['_id']})
                remove = notifications.remove({'_id': record['_id']})
            print "\n\n for user: ", username, " there is no notifications in last week," \
                                               " notification delete count: ", user_notification_count_whole

        elif user_notification_count_week > no_min_notifications:
            # user_list.append(username)
            # op_result_inter = notifications.find({'to': username, 'created': {'$lte': timestamp_days_back}})
            op_result_inter = notifications.remove({'to': username, 'created': {'$lte': timestamp_days_back}})
            print "\n\n From if,  username: ", username, " delete notification count: ", op_result_inter


        elif user_notification_count_week < no_min_notifications:
            deleted_notification_count = notifications.find({'to': username}).sort('created', -1).skip(20).count()
            deleted_notifications = notifications.find({'to': username}, {'created': 1}).sort('created', -1).skip(20)

            # deleted_notification = notifications.remove({'created': {'$lte': timestamp}})
            # deleted_notification = notifications.find({'created': {'$lte': timestamp}}).count()
            for record in deleted_notifications:
                # import ipdb
                # ipdb.set_trace()
                remove = notifications.remove({'_id': record['_id']})

            print "\n From else, username: ", username, " notification count: ", deleted_notification_count

        counter += 1

    end_time = time.time()

    print "time taken (in seconds ): ", end_time - start_time
    # print "total count: ", deleted_notification
    # map(delete_notification_records, user_list)
    # reuslt = [pool.apply(delete_notification_records, args=(x,)) for x in user_list]

    # import ipdb
    # ipdb.set_trace()

    # pool.map(delete_notification_records, user_list)
    # pool.map(delete_notification_records, username)