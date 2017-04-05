from flask import Flask, request, jsonify
from rollno_parse import main
from database import Courses, Attendence, TimeTable, Students
from flask_migrate import Migrate
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.ext.httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Blog.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
user = ['abhishek',
        'vaibhav']


@auth.verify_password
def verify_password(username, password):
    if username == user[0] and password == user[1]:
        return True
    else:
        return False


@app.route('/')
@app.route('/index')
def Index():
    return "index files"


@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        return login(username, password)
    else:
        return jsonify(invalid_password=username)


@app.route('/students/<rollno>/course_name')
def Course_details(rollno):
    # passing the rollno in a function and checking whether its valid or not
    valuebsr = main(rollno)
    if main(rollno) is False:
        # returning json object of Error due to wrong roll no
        return jsonify(Error={'invalid rollno': 'invalid'})
    else:
        Course = Courses.query.filter_by(
            branch=valuebsr[0], semester=valuebsr[1])
        return jsonify(Course_details=[i.serialize for i in Course])


@app.route('/students/<rollno>/time_table')
def Time_table(rollno):
    # passing the rollno in a function and checking whether its valid or not
    valuebsr = main(rollno)
    if main(rollno) is False:
        # returning json object of Error due to wrong roll no
        return jsonify(Error={'invalid rollno': 'invalid'})
    else:
        return 'hello'


@app.route('/students/<rollno>/attendence')
def Attendence(rollno):
    return "Attendence here"


@app.route('/students/<rollno>/courses/course_code')
def Course_code(rollno):
    # passing the rollno in a function and checking whether its valid or not
    valuebsr = main(rollno)
    if main(rollno) is False:
        # returning json object of Error due to wrong roll no
        return jsonify(Error={'invalid rollno': 'invalid'})
    else:
        # problem up here wait for it
        Course = Courses.query.filter_by(semester=valuebsr[1],
                                         branch=valuebsr[0]).with_entities(Courses.course_code)
        return jsonify(Course=[i.serialize for i in Course])


@app.route('/students/<rollno>/courses/course_code/syllabus')
def Syllabus(rollno):
    return "syllabus here"


@app.route('/students/<rollno>')
def Rollno():
    return "rollno"


@app.route('/students/<rollno>/edit', methods=['GET', 'POST'])
def Edit():
    if request.method == 'POST':
        return "editted data here"
    return "Edit here"


def login(username, password):
    data = {
        'mode': '191',
        'username': username,
        'password': password,
        'a': '1439199700564',
        'producttype': '0'
    }
    send = requests.post('http://172.50.1.1:8090/login.xml', data=data).text
    soup = BeautifulSoup(send)
    if soup.message.string == "You have successfully logged in" or soup.message.string == "You have reached Maximum Login Limit.":
        return "true"
    else:
        return "false"


if __name__ == '__main__':
    app.secret_key = "unknown_cookie_values_present_here_so_that_it_remains_secret_so_dont worry_its still secret"
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
