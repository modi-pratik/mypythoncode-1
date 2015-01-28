__author__ = 'stonex'

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['students']

unique_ids = set()

for data in db.grades.find({}, {'student_id': 1}):
    unique_ids.add(data['student_id'])

# print unique_ids

for std_id in unique_ids:
    std_id_grade = list(db.grades.find({'student_id': std_id, 'type': 'homework'}, {'student_id': -1, 'score': 1}))
    # print "removing student_id: ", std_id_grade[0]['student_id']
    if std_id_grade[0]['score'] > std_id_grade[1]['score']:
        db.grades.remove({'_id': std_id_grade[1]['_id']})
        print "part if removing student_id: ", std_id_grade[1]['student_id']
    else:
        db.grades.remove({'_id': std_id_grade[0]['_id']})
        print "part else removing student_id: ", std_id_grade[0]['student_id']
