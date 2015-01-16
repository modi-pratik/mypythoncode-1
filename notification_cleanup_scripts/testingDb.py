# import pymongo
from threading import Thread
from DBSetting import db


# # connection details
# """ 'host' => '192.168.4.86'
# 'database' => 'mobapi'
# 'login' => 'livedb'
# 'password' => 'livedb'
#
# """
# conn = pymongo.Connection('192.168.4.86')
#
# # connecting to db
# db = conn['mobapi']



def print_new(*arg_emp_list):
    # import ipdb
    # ipdb.set_trace()
    print "\n\n\n calling for new partition"
    counter = 0
    for emp in arg_emp_list[0]:
        counter += 1
        print "emp data : ", emp

    # print "\n\n\n count values in partition: ", counter, "\n\n\n"
# getting collection
arcgateemployees = db['arcgateemployees']

try:
    #  creating the whole list of emp for thread to process using list comprehension (which internally uses generators)
    emp_list = [x for x in arcgateemployees.find()]
    # creating Thread object which thread
    # t = Thread(target=print_new, args=emp_list)
    # t.start()

except Thread, e:
    print("error ", e)
