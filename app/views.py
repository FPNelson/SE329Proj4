import logging
import random
import json

from google.appengine.ext import db

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import login_required
from flask_login import current_user

from app.models import student
from app.models import user
from app.models import isu

blueprint = Blueprint('views', __name__)


@blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@blueprint.route('/charts', methods=['GET', 'POST'])
def charts():

    if not current_user.is_authenticated():
        return redirect(url_for('views.home'), code=302)
    if request.method == 'POST':
        student_query = student.Student.all()
        students = student_query.fetch(limit=None)
        query_form = request.form
        college = query_form.get('college')
        major = query_form.get('major')
        student_type = query_form.get('student_type')
        year = query_form.get('year')
        course = query_form.get('course')

        try:
            year = int(year)
        except ValueError:
            pass


        students = []
        if course:
            student_query = student.Student.all().filter('course', course)
        elif major:
            student_query = student.Student.all().filter('major', major)
        elif college:
            student_query = student.Student.all().filter('college', college)
        else:
            student_query = student.Student.all()

        if year == 'all':
            students = student_query.fetch(limit=None)
        else:
            students = student_query.filter('year', year).fetch(limit=None)


        distribution = {}
        grades = ['A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']

        for s in students:
            key = getattr(s, student_type)

            if student_type == 'gpa':
                key = "%.1f" % (key,)
            elif student_type == 'gender':
                key = 'Male' if key else 'Female'
            elif student_type == 'oncampus':
                key = 'On Campus' if key else 'Off Campus'
            elif student_type == 'major':
                key = s.major
            elif student_type == 'grade':
                if s.grade is None:
                    s.grade = random.choice(['A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'])
                key = s.grade
                for g in grades:
                    distribution[s.year] = distribution.get(s.year, {})
                    distribution[s.year][g] = distribution[s.year].get(g, 0)


            distribution[s.year] = distribution.get(s.year, {})
            distribution[s.year][key] = distribution[s.year].get(key, 0) + 1
            logging.info("value of distribution at s.year = %s and key = %s is %s", s.year, key, distribution[s.year].get(key, 0))
        return json.dumps({
            'distribution': distribution
        })


    return render_template('chart.html', colleges=isu.colleges.keys())


@blueprint.route('/isu/<college>/', methods=['GET'])
def iowa_state(college):
    return json.dumps(isu.colleges.get(college, []))


@blueprint.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('views.home'), code=302)

    if request.method == 'POST':
        login_form = request.form

        user.login(login_form.get('email'), login_form.get('password'))

        if current_user.is_authenticated():
            next_url = request.args.get('next',url_for('views.home'))
            return redirect(next_url, code=302)
        else:
            return render_template('login.html', failure=True, email=login_form.get('email'))

    return render_template('login.html', failure=False, email='')


@blueprint.route('/auth/logout', methods=['GET'])
def logout():
    user.logout()
    return redirect(url_for('views.home'), code=302)


@blueprint.route('/auth/register/<registration_id>', methods=['GET', 'POST'])
def register(registration_id):
    new_user = user.get_by_registration_id(registration_id)
    if not new_user or new_user.is_registered:
        return redirect(url_for('views.home'), code=302)

    if request.method == 'POST':
        registration_form = request.form
        new_password = registration_form.get('password', '')
        if len(new_password) < 6:
            return render_template('register.html', attempt={'failure':True}, user=new_user)

        user.register(registration_id, new_password)
        return redirect(url_for('views.home'), code=302)

    return render_template('register.html', attempt={}, user=new_user)


@blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin():
        return redirect(url_for('views.home'), code=302)

    if request.method == 'POST':
        admin_form = request.form
        user_role = admin_form.get('role', user.BASE_USER_ROLE)

        new_user = user.create_user(admin_form.get('email'), user_role)
        registration_url = url_for('views.register', registration_id=new_user.registration_id)

        return render_template('admin.html', new_user=new_user,
                                             registration_url=registration_url,
                                             users=user.get_users())

    return render_template('admin.html', new_user=None, users=user.get_users())

