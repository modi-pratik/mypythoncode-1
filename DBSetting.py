# Mongo db setting file:
# which returns db object

import pymongo
from pymongo import MongoClient

# connection details
""" 'host' => '192.168.4.86'
'database' => 'mobapi'
'login' => 'livedb'
'password' => 'livedb'

"""


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


client = MongoClient('mongodb://192.168.4.86:27017/')

# conn = pymongo.Connection('192.168.4.86')


# connecting to db
db = client['mobapi']

# range for data partition
partition_range = 10000

# collection name
collection_name = 'arcgateemployees'

# Number of multiple python processes to run
num_cores = 5


def delete_notification_records(arg_username):
    # import ipdb
    # ipdb.set_trace()
    # client = MongoClient('mongodb://192.168.4.86:27017/')
    conn = pymongo.Connection('192.168.4.86')

    # connecting to db
    db = conn.mobapi
    notifications = db.notifications_copy
    import ipdb
    ipdb.set_trace()
    # try to built here dict so that at delete loop will be faster one
    # op_result_inter = notifications.find({'to': arg_username}).skip(20).sort('created', -1)
    # op_result_inter = notifications.find({'to': arg_username,
    #  'created': {'$lte': arg_timestamp}}).skip(20).sort('created', 1)

    op_result_inter = 'testing'
    # for record in op_result_inter:
    #     notifications.remove({'_id': record['_id']})
    print op_result_inter
    # return op_result_inter