from google.appengine.ext import db

# You can find more out about types and properties of google app engine 
# database models here! 
# https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses
class Student(db.Model):
    age = db.IntegerProperty(required=True)
    gpa = db.FloatProperty(required=True)
    major = db.StringProperty(required=True)
    college = db.StringProperty(required=True)
    gender = db.BooleanProperty(required=True)
    oncampus = db.BooleanProperty(required=True)
    homestate = db.StringProperty()
    year = db.IntegerProperty(required=True)
    course = db.StringProperty()
    grade = db.StringProperty()

def fetch_students_by_gpa(gpa):
    return Student.all().filter('gpa', gpa).fetch(limit=None)

def fetch_students_by_department(college):
    return Student.all().filter('college', college).fetch(limit=None)

def fetch_students_by_gender(gender):
    return Student.all().filter('gender', gender).fetch(limit=None)

def fetch_students_by_age(age):
    return Student.all().filter('age', age).fetch(limit=None)

def fetch_students_by_major(major):
    return Student.all().filter('major', major).fetch(limit=None)

def fetch_students_by_homestate(homestate):
    return Student.all().filter('homestate', homestate).fetch(limit=None)

def fetch_students(limit=100, offset=0):
    return Student.all().fetch(limit=limit, offset=offset)

def fetch_students_by_course(course):
    return Student.all().filter('course', course)

def fetch_students_by_grade(grade):
    return Student.all().filter('grade', grade)

def create_student(age, gpa, gender, major, college, homestate, oncampus, year):
    new_student = Student(age=int(age), gpa = float(gpa), gender = gender, major = major, college = college, homestate = homestate, oncampus = oncampus, year=year) # Create new database model!
    new_student.put() # Store it in the database!

    return new_student