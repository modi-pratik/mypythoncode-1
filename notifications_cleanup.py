# from DBSetting import db #, delete_notification_records
import time
import multiprocessing
from datetime import timedelta
from pymongo import MongoClient
import smtplib
# import sys
# from itertools import product
# from pymongo import MongoClient


# Following are settings variables for script
no_min_notifications = 20
days_in_seconds = 604800
timestamp_days_back = int(time.time()) - days_in_seconds

# connection details
# connection_string = raw_input("Plesse enter the connection string: i.e mongodb://192.168.4.86:27017/ : ")

client = MongoClient('mongodb://192.168.4.86:27017/')
db = client['mobapi']

users = db['users_live']
notifications = db['notification_live_copy']


def delete_notification_records(arg_username):
    user_notification_count_whole = notifications.find({'to': arg_username}).sort('created', -1).skip(20).count()
    user_notifications = notifications.find({'to': arg_username}).sort('created', -1).skip(20)

    for record in user_notifications:
        # remove = notifications.find({'_id': record['_id']})
        remove = notifications.remove({'_id': record['_id']})
    print "\n\n for user: ", arg_username, " there is no notifications in last week," \
        " notification delete count: ", (user_notification_count_whole - 20)


if __name__ == "__main__":
    no_of_processes = int(raw_input("Please enter the number of processes you want to run: "))
    pool = multiprocessing.Pool(processes=no_of_processes)
    start_time = time.time()
    user_list = []
    counter = 1
    # settings for skipping and processing user in batch
    users_to_process = 100 #int(raw_input("Enter the number of user you want to process: "))
    user_to_skip = 0
    for user in users.find(timeout=False): #.sort({'username': 1}).skip(user_to_skip).limit(users_to_process):
        username = user['username']
        print "\n\n\n\n username :", username, "counter: ", counter

        # total notifications count
        notifications_count = notifications.find({'to': username}).count()

        # count the no of counts for last 7 days
        user_notification_count_week = notifications.find({'to': username,
                                                           'created': {'$gte': timestamp_days_back}}).count()

        if notifications_count == 0:
            print "\n\n for user: ", username, " there is no notifications"

        elif user_notification_count_week == 0 and notifications_count > no_min_notifications:
            # no notification in last 7 days, so pull past notifications and keep 20 and delete rest

            print " 1 user: ", username, " added to user_list for delete ltr using multiprocess"
            user_list.append(username)
            continue

        elif user_notification_count_week > no_min_notifications:
            # notifications are more then 20 for 7 days, delete all notifications older then 7 days

            op_result_inter = notifications.remove({'to': username, 'created': {'$lte': timestamp_days_back}})
            print "\n\n From if,  username: ", username, " delete notification count: ", op_result_inter
            continue

        elif user_notification_count_week < no_min_notifications < notifications_count:
            print " 1 user: ", username, " added to user_list for delete ltr using multiprocess"
            user_list.append(username)
            continue
        counter += 1
        # stop here with user count more then that
        # if counter == 200:

    map(delete_notification_records, user_list)

    end_time = time.time()
    time_taken = end_time - start_time

    print "time taken (in seconds ): ", end_time - start_time
    print "\nstart time: ", start_time, "end time: ", end_time

    # 0 days 14:12:29

    a = timedelta(seconds=time_taken)
    time_string = "\nTime taken: %d days %02d:%02d:%02d" % (a.days, a.seconds / 3600, (a.seconds / 60) % 60, a.seconds % 60)
    print "\nTime taken: %d days %02d:%02d:%02d" % (a.days, a.seconds / 3600, (a.seconds / 60) % 60, a.seconds % 60)

    # ======================================================================================================
    # following are mail settings, please config it, or use your own mail send function and attach excel file created here

    mail_user = ""
    mail_pwd = ""
    FROM = ''
    TO = ['manish@arcgate.com', 'snehaldot@gmail.com'] #must be a list
    SUBJECT = "Script Output for workmob notifications"
    TEXT = ("""MIME-Version: 1.0
              Content-type: text/html
              Subject: SMTP HTML e-mail test

              This is an e-mail message to be sent in HTML format

              time taken for the script:  %s and currently total no. notifications: %s""") %(time_string,
                                                                                             notifications.count())

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(mail_user, mail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
        # return 0
    except:
        print "failed to send mail"
        # return 1
