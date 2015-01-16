# from DBSetting import db #, delete_notification_records
import time
from datetime import timedelta
from pymongo import MongoClient
import datetime
from email_send_ses_gmail import send_email_amazon_ses

# Following are settings variables for script
no_min_notifications = 20
days_in_seconds = 604800

# connection details
# connection_string = raw_input("Please enter the connection string: i.e mongodb://192.168.4.86:27017/ : ")
# connection_string = 'mongodb://localhost:27017'
connection_string = 'mongodb://192.168.4.86:27017/'

client = MongoClient(connection_string)

db = client['mobapi']

users = db['users_live']
# put other collection here too
# notifications = db['notification_live_copy']
notifications = db['notificationmappings_copy']


def delete_notification_records(arg_username):
    user_notification_count_whole = notifications.find({'to': arg_username}).sort('created', -1).skip(20).count()
    user_notifications = notifications.find({'to': arg_username}).sort('created', -1).skip(20)

    for record in user_notifications:
        remove = notifications.remove({'_id': record['_id']})
    print "\n\n for user: ", arg_username, " there is no notifications in last week," \
                                           " notification delete count: ", (user_notification_count_whole - 20)


if __name__ == "__main__":
    # no_of_processes = int(raw_input("Please enter the number of processes you want to run: "))
    # pool = multiprocessing.Pool(processes=no_of_processes)
    start_time = time.time()

    user_list = []
    counter = 1

    for user in users.find(timeout=False):
        username = user['username']
        print "\n\n\n\n username :", username, "counter: ", counter

        # total notifications count
        notifications_count = notifications.find({'to': username}).count()

        last_updated_notification_lst = list(notifications.find({'to': username},
                                                                {'created': 1}).sort('created', -1).limit(1))
        if last_updated_notification_lst:
            last_updated_notification = last_updated_notification_lst[0]['created']
            timestamp_days_back = last_updated_notification - days_in_seconds

            # count the no of counts for last 7 days
            user_notification_count_week = notifications.find({'to': username,
                                                               'created': {'$gte': timestamp_days_back}}).count()

            if user_notification_count_week >= no_min_notifications:
                # notifications are more then 20 for 7 days, delete all notifications older then 7 days
                op_result_inter = notifications.remove({'to': username, 'created': {'$lte': timestamp_days_back}})
                print "\n\n Removed using mongod remove function,  username: ", username, \
                    " delete notification count: ", op_result_inter

            elif user_notification_count_week < no_min_notifications < notifications_count:
                print " 1 user: ", username, " added to user_list for delete ltr using multiprocess"
                user_list.append(username)
            counter += 1

        else:
            print "\n\n for user: ", username, " there is no notifications"

            # remove all the notifications which have unread 1

    # map(delete_notification_records, user_list)

    delete_notification_records(user_list)
    end_time = time.time()
    time_taken = end_time - start_time

    print "time taken (in seconds ): ", end_time - start_time
    print "\nstart time: ", start_time, "end time: ", end_time

    delta = timedelta(seconds=time_taken)
    time_string = "%d days %02d:%02d:%02d" % (delta.days, delta.seconds / 3600, (delta.seconds / 60) % 60,
                                              delta.seconds % 60)
    print "\n Time taken: %s", time_string

    # ======================================================================================================
    # following are mail sending part

    TEXT = "\nTime taken for the notificationmappings script: %s and \nCurrently total number notifications: %s " \
           " \nStart time: %s, and \nEnd time: %s" % (time_string, notifications.count(),
                                                      datetime.datetime.fromtimestamp(int(start_time)).strftime(
                                                          '%Y-%m-%d %H:%M:%S'),
                                                      datetime.datetime.fromtimestamp(int(end_time)).strftime(
                                                          '%Y-%m-%d %H:%M:%S')
           )

    send_email_amazon_ses(mail_from='hello@workmobmail.com',
                          mail_to=['snehal@arcgate.com', 'snehaldot@gmail.com'],
                          message=TEXT)

    # send_mail_gmail(mail_from='arcgatemailtest@gmail.com', mail_to=['snehal@arcgate.com', 'snehaldot@gmail.com'],
    # host='smtp.gmail.com', message=TEXT, mail_user='arcgatemailtest@gmail.com', mail_pwd='Arcgate1!')
