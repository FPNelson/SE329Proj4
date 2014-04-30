from app.models import student
from app.models import isu
import random

import sys
sys.path.insert(0, 'C:/Program Files (x86)/Google/google_appengine/')
import google.appengine.ext
new_students = []
for x in xrange(1000):
    college = random.choice(isu.colleges.keys())
    major = random.choice(isu.colleges[college])
    new_students.append(student.Student(
            age=random.randint(18,30),
            gpa=random.random() * 3.0 + 1.0,
            gender=random.choice([True, False]),
            college=college,
            major=major,
            oncampus=random.choice([True, False]),
            year=random.choice([2012, 2013, 2014])
        ))

google.appengine.ext.put(new_students)