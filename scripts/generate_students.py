from app.models import student
from app.models import isu
import random
from google.appengine.ext import db


new_students = []
for x in xrange(1000):
    college = random.choice(isu.colleges.keys())
    major = random.choice(isu.colleges[college])
    course = random.choice(isu.anthropology)
    new_students.append(student.Student(
            age=random.randint(18,30),
            gpa=random.random() * 3.0 + 1.0,
            gender=random.choice([True, False]),
            college=college,
            major=major,
            course=course,
            oncampus=random.choice([True, False]),
            year=random.choice([2012, 2013, 2014])
        ))

db.put(new_students)