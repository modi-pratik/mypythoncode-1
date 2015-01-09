import pandas as pd
from pymongo import MongoClient
from DBSetting import db, partition_range, collection_name, client


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection='queue_compaddresses', query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    # db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db['queue_compaddresses'].find(query)
    import ipdb
    ipdb.set_trace()
    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

""" 'host' => '192.168.4.86'
'database' => 'mobapi'
'login' => 'livedb'
'password' => 'livedb'

"""

if __name__ == '__main__':
    df = read_mongo(db=db, collection=collection_name, query={}, host='192.168.4.86', port=27017, username='livedb',
               password='livedb')
    print df