import multiprocessing
import time
# import company_feeds
# from company_feeds import facebook_feed_pull
from pymongo import MongoClient


def get_collection(collection_name):
    connection_string = 'mongodb://192.168.4.86:27017/'

    client = MongoClient(connection_string)
    db = client['mobapi']
    collection_name = db[collection_name]
    return collection_name


def do_calculation(data):
    # get_collection_func =
    # fp = open('new.txt', 'a')
    # fp.write(str(data)+"\n")
    collection = get_collection('queue_sociallinks')
    # import ipdb
    # ipdb.set_trace()
    return data * 2


def start_process():
    print 'Starting', multiprocessing.current_process().name

if __name__ == '__main__':
    inputs = list(range(1000))
    print 'Input   :', inputs

    builtin_start_time = time.time()
    builtin_outputs = map(do_calculation, inputs)
    print 'Built-in:', builtin_outputs
    builtin_end_time = time.time()
    # time taken: 0.00413799285889

    pool_start_time = time.time()
    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(processes=pool_size,
                                initializer=start_process,
                                )
    pool_output = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks
    pool_end_time = time.time()
    #  time taken: 0.194107055664

    simple_start_time = time.time()
    pool_output = []
    for each in inputs:
        pool_output.append(do_calculation(each))
    simple_end_time = time.time()
    # time taken: 0.00377488136292

    end_time = time.time()
    print 'Pool    :', pool_output

    print "builtin time taken: %s" % (builtin_end_time - builtin_start_time)
    print "Pool time taken: %s" % (pool_end_time - pool_start_time)
    print "simple time taken: %s" % (simple_end_time - simple_start_time)
