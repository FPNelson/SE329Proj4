import unittest
from mock import patch

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from app.models import user

user.SECRTE_KEY = 'unit-test-key'
test_hash_code = '314e0c6b453d413885fb2ca432db3c35'

class HashingTestCase(unittest.TestCase):

    def test_password_with_hash(self):
        """
        Ensure that user passwords are encrypted correctly using sha512
        when the secret_key, hash_code, and string password are given.
        """
        user_password, user_hash = user.hash_password('test', test_hash_code)
        self.assertEqual(user_password, '35e00d53f72f27d5fb9d4326d74ede2c248e40f18833fa61fb3128b97239162b93663e30433a2ba1b0197c7f24b42dff0009504ef925fd4ac21cdf07b356e2a7')
        self.assertEqual(user_hash, '314e0c6b453d413885fb2ca432db3c35')

        user_password, user_hash = user.hash_password('Jon Snow', test_hash_code)
        self.assertEqual(user_password, 'f4050ce0fb5dd7b3432ff84fa4642ace952ab90061dcd7c207b9714485d2a32ff8236e2e61fb96408d1f2f20b7460d0fdba7bfa97c9b547c375df2e02e0d2a06')
        self.assertEqual(user_hash, '314e0c6b453d413885fb2ca432db3c35')

        user_password, user_hash = user.hash_password('', test_hash_code)
        self.assertEqual(user_password, 'b04ea78efc1981b980bb847a535e3c16216a2a22f6adff02fd5e8d77c77656472fafae8edd8fe94145729678a9deaaf25096e88d37bdb0f729cbc5c146017f63')
        self.assertEqual(user_hash, '314e0c6b453d413885fb2ca432db3c35')

    def test_no_hash(self):
        """
        Ensure that when calling hash user password with out an initial 
        hash that a new one is generated and returned.  Then verify that
        the password can be rebuilt using that same hash.
        """
        original_user_password = 'abc123'
        user_password, user_hash = user.hash_password(original_user_password)
        rebuilt_user_password, rebuilt_user_hash = user.hash_password(original_user_password, user_hash)
        self.assertEqual(user_password, rebuilt_user_password)
        self.assertEqual(user_hash, rebuilt_user_hash)


class CreateUserTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    @patch('app.models.user.uuid')
    def test_create_user(self, uuid_mock):
        uuid_mock.uuid4.return_value.hex = test_hash_code

        new_email = 'foobar@gmail.com'
        new_user = user.create_user(new_email, user.ADMIN_ROLE)
        self.assertEqual(new_user.email, new_email)
        self.assertEqual(new_user.role, user.ADMIN_ROLE)
        self.assertEqual(new_user.registration_id, test_hash_code)

    def test_if_user_already_exists(self):
        new_email = 'gordan@freeman.com'
        new_user = user.create_user(new_email, user.ADMIN_ROLE)
        old_user = user.create_user(new_email, user.ADMIN_ROLE)

        self.assertEqual(new_user.email, old_user.email)
        self.assertEqual(new_user.role, old_user.role)
        self.assertEqual(new_user.registration_id, old_user.registration_id)


class RegisterUserTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_user_exists(self):
        user.User(registration_id='1234', is_registered=True).put()
        self.assertEqual(user.register('1234', 'fake password'), None)

    @patch('app.models.user.login_user')
    @patch('app.models.user.logout_user')
    def test_success(self, logout_user_mock, login_user_mock):
        new_user = user.create_user('foobar@gmail.com', 'admin')

        new_user = user.register(new_user.registration_id, '1234password')
        password, user_hash = user.hash_password('1234password', new_user.hash_code)

        self.assertEqual(password, new_user.password)

        self.assertEqual(new_user.is_registered, True)



class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    @patch('app.models.user.login_user')
    @patch('app.models.user.logout_user')
    def test_success(self, logout_user_mock, login_user_mock):
        new_user = user.create_user('foobar@gmail.com', 'admin')
        new_user = user.register(new_user.registration_id, '1234password')

        self.assertTrue(user.login('foobar@gmail.com', '1234password'))

    @patch('app.models.user.login_user')
    @patch('app.models.user.logout_user')
    def test_password_incorrect(self, logout_user_mock, login_user_mock):
        new_user = user.create_user('a@gmail.com', 'admin')
        new_user = user.register(new_user.registration_id, 'aaaaaa')

        self.assertFalse(user.login('foobar@gmail.com', 'wrong password'))

    @patch('app.models.user.login_user')
    @patch('app.models.user.logout_user')
    def test_user_dne(self, logout_user_mock, login_user_mock):
        new_user = user.create_user('foobar@gmail.com', 'admin')
        new_user = user.register(new_user.registration_id, '1234password')

        self.assertFalse(user.login('wrongemail@gmail.com', '1234password'))


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_id(self):
        new_user = user.User()
        new_user_key = new_user.put()

        self.assertEqual(new_user_key, new_user.key())

    def test_is_active(self):
        self.assertTrue(user.User().is_active())

    def test_is_anonymous(self):
        self.assertFalse(user.User().is_anonymous())

    def test_is_authenticated(self):
        self.assertTrue(user.User().is_authenticated())
