# from DBSetting import db #, delete_notification_records
import time
from datetime import timedelta
from pymongo import MongoClient
import datetime
import sys
from email_send_ses_gmail import send_email_amazon_ses
import logging

# logging config
# crontab entry : * 0 * * * /usr/bin/python /home/ec2-user/python_scripts/notification_cleanup_daily.py
# /var/www/html/site/liveworkmob/api/app/tmp/logs
LOG_FILENAME = '/var/www/html/site/liveworkmob/api/app/tmp/logs/log_notification_cleanup_daily.log'
FORMAT = "%(asctime)-15s %(name)s %(levelname)-8s %(message)s"
logging.basicConfig(format=FORMAT, filename=LOG_FILENAME, level=logging.DEBUG)

# Following are settings variables for script
no_min_notifications = 20
days_in_seconds = 604800


def delete_notification_records(arg_username_list, arg_notifications):
    for arg_username in arg_username_list:
        user_notification_count_whole = arg_notifications.find({'to': arg_username}).sort('created', -1).skip(20).count()
        user_notifications = arg_notifications.find({'to': arg_username}).sort('created', -1).skip(20)

        for record in user_notifications:
            remove = arg_notifications.remove({'_id': record['_id']})
        logging.debug("for user: %s there is no notifications in last week,"
                      " notification delete count: %d" % (arg_username, user_notification_count_whole))
        # print "\n\n for user: ", arg_username, " there is no notifications in last week," \
        #                                        " notification delete count: ", (user_notification_count_whole - 20)


if __name__ == "__main__":
    try:
        # connection details
        # connection_string = raw_input("Please enter the connection string: i.e mongodb://192.168.4.86:27017/ : ")
        # for testing on 86 local server
        # connection_string = 'mongodb://192.168.4.86:27017/'
        # 10.225.171.204
        # for production 10.184.172.70

        connection_string = 'mongodb://10.184.172.70:27017'

        client = MongoClient(connection_string)
        db = client['mobapi']
        users = db['users']
        # put other collection here too
        notifications = db['notifications']

        # no_of_processes = int(raw_input("Please enter the number of processes you want to run: "))
        # pool = multiprocessing.Pool(processes=no_of_processes)
        start_time = time.time()

        logging.debug("Script starting time : %s", start_time)
        user_list = []
        counter = 1

        for user in users.find(timeout=False).limit(10):
            username = user['username']
            logging.debug(" username : %s counter: %s", username, counter)
            # print "\n\n\n\n username :", username, "counter: ", counter

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
                    logging.debug("Removed using mongod remove function,  username: %s "
                                  "delete notification count: %s", username, op_result_inter)
                    # print "\n\n Removed using mongod remove function,  username: ", username, \
                    #     " delete notification count: ", op_result_inter

                elif user_notification_count_week < no_min_notifications < notifications_count:
                    logging.debug(" user: %s added to user_list for delete ltr using multiprocess", username)
                    # print " 1 user: ", username, " added to user_list for delete ltr using multiprocess"
                    user_list.append(username)

            else:
                logging.debug("for user: %s there is no notifications", username)
                # print "\n\n for user: ", username, " there is no notifications"

                # remove all the notifications which have unread 1
            counter += 1

        # map(delete_notification_records, user_list)

        delete_notification_records(user_list, notifications)

        # compacting database
        compact_result = db.command("repairDatabase")

        end_time = time.time()
        time_taken = end_time - start_time

        logging.debug("time taken (in seconds ): ", time_taken)
        # print "time taken (in seconds ): ", time_taken
        logging.debug("start time: ", start_time, "end time: ", end_time)
        # print "\nstart time: ", start_time, "end time: ", end_time

        delta = timedelta(seconds=time_taken)
        time_string = "%d days %02d:%02d:%02d" % (delta.days, delta.seconds / 3600, (delta.seconds / 60) % 60,
                                                  delta.seconds % 60)
        logging.debug("Time taken: %s", time_string)
        # print "\n Time taken: %s", time_string

        # ======================================================================================================
        # following are mail sending part

        TEXT = "\nTime taken for the Notification_cleanup_daily script: %s and \nCurrently total number notifications: %s " \
               " \nStart time: %s, and \nEnd time: %s \n compact result: %s" % (time_string, notifications.count(),
                                                          datetime.datetime.fromtimestamp(int(start_time)).strftime(
                                                              '%Y-%m-%d %H:%M:%S'),
                                                          datetime.datetime.fromtimestamp(int(end_time)).strftime(
                                                              '%Y-%m-%d %H:%M:%S'), compact_result
               )

        #email_list = ['snehal@arcgate.com', 'snehaldot@gmail.com', 'baran@arcgate.com', 'manish@arcgate.com']
        email_list = ['snehal@arcgate.com', 'snehaldot@gmail.com']
        send_email_amazon_ses(mail_from='hello@workmobmail.com', mail_to=email_list, message=TEXT)

        # send_mail_gmail(mail_from='arcgatemailtest@gmail.com', mail_to=['snehal@arcgate.com', 'snehaldot@gmail.com'],
        # host='smtp.gmail.com', message=TEXT, mail_user='arcgatemailtest@gmail.com', mail_pwd='Arcgate1!')
    except:
        TEXT = "Exception in running the script, please check log file for more details" \
               " Exception: %s" % sys.exc_info()[0]

        #email_list = ['snehal@arcgate.com', 'snehaldot@gmail.com', 'baran@arcgate.com', 'manish@arcgate.com']
        email_list = ['snehal@arcgate.com', 'snehaldot@gmail.com']
        send_email_amazon_ses(mail_from='hello@workmobmail.com',
                              mail_to=email_list,
                              message=TEXT)
