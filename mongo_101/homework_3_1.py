__author__ = 'stonex'

import pymongo
import sys


connection = pymongo.Connection('mongodb://localhost', safe=True)

db = connection.school
students = db.students


for student in students.find().skip(1):
    print " current student_id: ", student['_id']
    homework_score_list = []
    scores = []
    for score in student['scores']:
        if score['type'] == 'homework':
            homework_score_list.append(score['score'])
        else:
            scores.append(score)

    if homework_score_list[0] > homework_score_list[1]:
        scores.append({'score': homework_score_list[0], 'type': 'homework'})
    else:
        scores.append({'score': homework_score_list[1], 'type': 'homework'})

    students.update({'_id': student['_id']}, {'$set': {'scores': scores}})

