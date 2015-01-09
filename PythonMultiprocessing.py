import multiprocessing
from testingDb import print_new
from DBSetting import db, partition_range, collection_name, num_cores
from math import ceil
from itertools import product

if __name__ == '__main__':
    collection_data = db['queue_compaddresses']
    # collection_data = db[collection_name]

    jobs = []

    collection_data_count = collection_data.find().count()
    # import ipdb
    # ipdb.set_trace()
    if collection_data_count <= partition_range:
        # emp_list = [x for x in collection_data.find()]
        print_new(collection_data.find())
    else:
        start, end = 0, partition_range
        round_upper_partitions = int(ceil(float(collection_data_count)/partition_range))
        pool = multiprocessing.Pool(processes=5)
        for i in range(0, round_upper_partitions):
            emp_crx = collection_data.find()[start:end]
            print("printing from %s to %s" % (start, end))
            # partition_crx_list.append(emp_crx)
            # import ipdb
            # ipdb.set_trace()
            # print_new(emp_crx)

            pool.map(print_new, product(emp_crx))

            # print_new(emp_list)
            # p = multiprocessing.Process(target=print_new, args=emp_list)
            # jobs.append(p)
            # p.start()
            # gevent.spawn(print_new(emp_list))
            start, end = start + partition_range, end + partition_range
