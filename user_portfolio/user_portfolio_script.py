__author__ = 'Snehal'

# from DBSetting import db
import time
from datetime import timedelta
from pymongo import MongoClient


if __name__ == '__main__':
    # connection details
    # connection_string = raw_input("Plesse enter the connection string: i.e mongodb://192.168.4.86:27017/ : ")

    start_time = time.time()

    client = MongoClient('mongodb://192.168.4.86:27017/')
    db = client['mobapi']

    # collections to be used in script
    users = db['users_live']
    # put other collection here too
    notifications = db['notificationmappings']
    user_protfolio = db['user_protfolio']

    # cronflag

    for notification in notifications.find({'cronflag': 0}):
        to_username = notification['to']
        from_username = notification['from']

        # follow_count and follower_count
        if notification['key'] == 'user' and notification['action'] == 'Follow':
            import ipdb
            ipdb.set_trace()

            # updating user follow count
            from_ln = list(user_protfolio.find({'_id': from_username}))

            if from_ln:
                user_protfolio.update({'_id': from_username},
                                      {"$inc": {"follow_count": 1}})
            else:
                user_protfolio.insert({{'_id': from_username,
                                        'follow_count': 1,
                                        'follower_count': 0,
                                        'company_fan_count': 0}})

            # updating user follower count
            to_ln = list(user_protfolio.find({'_id': to_username}))

            if to_ln:
                user_protfolio.update({'_id': to_username},
                                      {'$inc': {'follower_count': 1}})
            else:
                user_protfolio.insert({{'_id': from_username,
                                        'follow_count': 0,
                                        'follower_count': 1,
                                        'company_fan_count': 0}})

            # updating cronflag to make count
            notification['cronflag'] = 1

        # updating company_fan_count

        if notification['key'] == 'company' and notification['action'] == 'fan':
            import ipdb
            ipdb.set_trace()
            user_protfolio.insert({'_id': from_username})

            # updating cronflag to make count
            notification['cronflag'] = 1

    end_time = time.time()
    time_taken = end_time - start_time

    print "time taken (in seconds ): ", end_time - start_time
    print "\nstart time: ", start_time, "end time: ", end_time

    # 0 days 14:12:29

    a = timedelta(seconds=time_taken)
    time_string = "%d days %02d:%02d:%02d" % (a.days, a.seconds / 3600, (a.seconds / 60) % 60, a.seconds % 60)
    print "\n Time taken: %s", time_string



