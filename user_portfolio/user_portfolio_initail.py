__author__ = 'Snehal'

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
    # notifications = db['notificationmappings']
    user_protfolios = db['user_protfolios']

    # cronflag

    users_counter = 0
    for user in users.find():
        # tmp_user = list(user_protfolio.find({'_id': user}))
        # import ipdb
        # ipdb.set_trace()
        if 'follow' in user:
            follow_count = len(user['follow'])
        else:
            follow_count = 0

        if 'follower' in user:
            follower_count = len(user['followers'])
        else:
            follower_count = 0

        if 'companiesfan'in user:
            companiesfan_count = len(user['companiesfan'])
        else:
            companiesfan_count = 0

        # import ipdb
        # ipdb.set_trace()
        user_protfolios.insert({'_id': user['_id'],
                                'username': user['username'],
                                'follow_count': follow_count,
                                'follower_count': follower_count,
                                'companiesfan_count': companiesfan_count})
        users_counter += 1
        print "\nuser portfolio updated for user: ", user['username'], "current user count: ", users_counter

    end_time = time.time()

    time_taken = end_time - start_time

    print "time taken (in seconds ): ", time_taken
    print "\nstart time: ", start_time, "end time: ", end_time
