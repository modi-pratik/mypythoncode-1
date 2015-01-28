__author__ = 'stonex'

import pymongo
import sys


connection = pymongo.Connection('mongodb://localhost', safe=True)

db = connection.students
scores = db.scores


def find():
    print "starting of find function"

    query = {'type': 'exam'}
    selector = {'student_id': 1, '_id': 0}
    try:
        iter = scores.find(query, selector)
    except:
        print " Exception in running find function: ", sys.exc_info()[0]
        return None

    sanity = 0

    for doc in iter:
        print doc
        sanity += 1
        if sanity > 10:
            break

find()


