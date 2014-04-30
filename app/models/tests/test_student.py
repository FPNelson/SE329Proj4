import unittest
from mock import patch

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from app.models import student


class CreateStudentTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_create(self):
        new_student = student.create_student(21, 2.5, True,
            'Software Engineering', 'Liberal Arts and Sciences', 'Iowa', False, 2014)

        self.assertEqual(new_student.age, 21)
        self.assertEqual(new_student.gpa, 2.5)
        self.assertEqual(new_student.gender, True)
        self.assertEqual(new_student.major, 'Software Engineering')
        self.assertEqual(new_student.college, 'Liberal Arts and Sciences')
        self.assertEqual(new_student.homestate, 'Iowa')
        self.assertEqual(new_student.oncampus, False)
        self.assertEqual(new_student.year, 2014)
