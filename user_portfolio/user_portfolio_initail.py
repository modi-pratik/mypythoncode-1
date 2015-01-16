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
    notifications = db['notificationmappings']
    user_protfolio = db['user_protfolio']

    # cronflag

    for user in users.find():
        # tmp_user = list(user_protfolio.find({'_id': user}))
        # import ipdb
        # ipdb.set_trace()
        import ipdb
        ipdb.set_trace()
        follow_count = len(user['follow'])
        follower_count = len(user['follower'])
        companiesfan_count = len(user['companiesfan'])

        user_protfolio.insert({'_id': user, 'follow_count': follow_count,
                               'follower_count': follower_count,
                               'companiesfan_count': companiesfan_count})
