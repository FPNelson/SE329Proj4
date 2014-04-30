import hashlib
import uuid
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

from flask_login import login_user
from flask_login import logout_user

ADMIN_ROLE = 'admin'
BASE_USER_ROLE = 'base-user-role'
ROLES = [ADMIN_ROLE, BASE_USER_ROLE]

SECRTE_KEY = 'hey, im a secret key for encrypting user passwords!'

class User(db.Model):
    email = db.StringProperty()
    password = db.StringProperty(indexed=False)
    role = db.StringProperty(indexed=False)
    hash_code = db.StringProperty(indexed=False)

    registration_id = db.StringProperty()
    is_registered = db.BooleanProperty(default=False, indexed=False)

    def get_id(self):
        return str(self.key())

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        return self.role == ADMIN_ROLE

def get_users(limit=None, offset=0):
    return User.all().fetch(limit=limit, offset=offset)

def get_by_id(user_id):
    cached_user = memcache.get(user_id)
    if cached_user:
        return cached_user

    user = db.get(user_id)

    memcache.set(user_id, user)
    return user

def get_by_registration_id(registration_id):
    return User.all().filter('registration_id', registration_id).get()

def hash_password(password, hash_code=None):
    if not hash_code:
        hash_code = uuid.uuid4().hex

    key = '%s%s%s' % (password, hash_code, SECRTE_KEY)
    return hashlib.sha512(key).hexdigest(), hash_code

def create_user(email, role):
    user = User.all().filter('email', email).get()
    if user:
        return user

    registration_id = uuid.uuid4().hex
    user = User(email=email, role=role, registration_id=registration_id)
    user.put()
    return user

def register(registration_id, password):
    user = get_by_registration_id(registration_id)
    if user.is_registered:
        return None

    if user:
        user.is_registered = True
        user.password, user.hash_code = hash_password(password)
        user.put()
        logout()
        login_user(user)
        return user
    return None

def login(email, password):
    user = User.all().filter('email', email).get()
    if not user or not user.is_registered:
        return False

    memcache.set(user.get_id(), user)
    hashed_password, hash_code = hash_password(password, user.hash_code)
    if user.password == hashed_password:
        login_user(user)
        return True

    return False

def logout():
    logout_user()
