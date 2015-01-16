import gevent
from DBSetting import db, partition_range, collection_name
from testingDb import print_new
import sys


def foo():
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')
    print("testing from foo")


def bar():
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')
    print("testing from boo")


def tar():
    print('Explicit context to tar')
    gevent.sleep(0)
    print('Implicit context switch back to tar')
    print("testing from too")
    print("testing from too")


# getting collection
# collection_data = db[collection_name]
collection_data = db['queue_compaddresses']

# import ipdb
# ipdb.set_trace()
collection_data_count = collection_data.find().count()

if collection_data_count <= partition_range:
    emp_list = [x for x in collection_data.find()]#[:5]
    gevent.spawn(print_new(emp_list))
    sys.exit()
else:
    start, end = 0, partition_range
    for i in range(0, collection_data.find().count() % partition_range):
        emp_list = collection_data.find()[start:end]
        print("printing from %s to %s" % (start, end))
        # print_new(emp_list)
        gevent.spawn(print_new(emp_list))
        start, end = start + partition_range, end + partition_range


# gevent.spawn(print_new(emp_list))
# gevent.joinall([
#     # gevent.spawn(foo),
#     # gevent.spawn(bar),
#     # gevent.spawn(tar),
#     gevent.spawn(print_new(emp_list))
# ])