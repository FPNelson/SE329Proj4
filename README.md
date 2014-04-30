Uptown Saturday Night
=========
[uptown-prototype.appspot.com](http://uptown-prototype.appspot.com/)

Setting Up
-----------
* Download and Install [Python 2.7](http://www.python.org/download/releases/2.7/)
* Download and Install [GAE Python SDK](https://developers.google.com/appengine/downloads)
* Download and Install [Git](http://git-scm.com/book/en/Getting-Started-Installing-Git)
* Checkout this repository ```git clone https://github.com/theMagicalKarp/uptown-prototype.git uptown```
* Start GAE SDK and select this project.

Running Unit Tests
-----------
To run unit tests with included frameworks use the testing script.
With the script you can target the GAE SDK and testing directory.
For example ```python test.py /usr/local/google_appengine .``` runs all the unit tests.


Libraries and Frameworks Used
-----------
* [Google App Engine](https://developers.google.com/appengine/) *Web framework for running our python enviroment*
* [Flask](http://flask.pocoo.org/) *URL Routing*
* [Flask-Login](https://flask-login.readthedocs.org/en/latest/) *User Authentication*
* [Jinja2](http://jinja.pocoo.org/) *HTML templating*
* [Bootstrap](http://getbootstrap.com/) *HTML Styling*
* [jQuery](http://jquery.com/) *Wrapper for JavaScript... Also required for bootstrap... D:*

What's Going On?!
-----------
[__/app.yaml:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app.yaml) Basic config that Google App Engine uses to understands how to run our application. This is the first thing ran when starting the server.

[__/libs/:__](https://github.com/theMagicalKarp/uptown-prototype/tree/master/libs) Contains external python libraries such as Flask, werkzeug, ect...

[__/app/views.py:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app/views.py) Contains instructions of how to map our application to specific urls. For example this [http://uptown-prototype.appspot.com/](http://uptown-prototype.appspot.com/) is generated from this
```python
@blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')
```

[__/app/models/students.py:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app/models/student.py) This holds information on how our student objects should be stored in the database.

[__/app/templates/:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app/templates) This directory holds html template files that are to be rendered by jinja2.  Each html file extends a base html file that describes how each page should look.  This helps enforce consistancy among all of the pages.  You can find out more about jinja2 templating [here](http://jinja.pocoo.org/docs/templates/).

[__/app/models/isu.py:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app/models/isu.py)  This holds information about Iowa States majors and colleges staticly in memory for quick refrence in our application.

[__/app/models/user.py:__](https://github.com/theMagicalKarp/uptown-prototype/blob/master/app/models/user.py)  This holds information about our user models and authentication.
