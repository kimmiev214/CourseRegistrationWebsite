'''
This is a flask program to create a course registration website for a hypothetical university
'''
#imports
import datetime
import re
import logging
import bcrypt

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#main
app = Flask(__name__)
db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    '''This runs immediately after the app starts'''
    #this creates the database
    db.create_all()
    #this sets up the log file and formats the outputs
    logging.basicConfig(filename = 'myLog.log', level=logging.WARNING,
    format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#this creates the users database object
class Users(db.Model):
    '''Users database class'''
    #username column
    username = db.Column('username', db.String(20), primary_key=True, nullable = False)
    #password column
    password = db.Column(db.String(60), nullable = False)
def __init__(username, password):
    '''initialize function'''
    self.username = username
    self.password = password
#the @app.route command determines what happens when the given hyperlink is clicked
@app.route('/administration/')
def administration():
    '''This creates the administration webpage'''
    #returns the render
    return render_template('administration.html')
@app.route('/welcome/')
def welcome():
    '''This creates the welcome webpage'''
    #returns the render
    return render_template('welcome.html', utc_dt=datetime.datetime.now())
@app.route('/courses/')
def courses():
    '''This creates the courses webpage'''
    #returns the render
    return render_template('courses.html')
@app.route('/register/', methods =['GET','POST'])
def register():
    '''This creates the register webpage'''
    #returns the render
    #request.method is what happens when the submit button is clicked
    if request.method == 'POST':
        #if password and confirm password box contents match
        if request.form['password'] == request.form['confirmpassword']:
            #if password passes password_okay method
            if password_okay(request.form['password']):
                password = request.form['password']
                #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                #if username is not blank
                if request.form['username']!="":
                    #set user username and password info
                    user = Users(username = request.form['username'],
                        password = password)
                    #add user to database
                    db.session.add(user)
                    #commit the database
                    db.session.commit()
                    #success message
                    msg = "Success, you are now registered."
                else:
                    #Please add username message
                    msg = "Please add username"
            else:
                #unsuccessful password_okay check
                msg = ("Password must contain 1 uppercase, 1 lowercase, 1 number," +
                    " 1 special character, and be at least 12 characters long.")
        else:
            #password and confirm password do not match
            msg = "Password does not match Confirm Password box."
        #render the register webpage with the message
        return render_template('register.html', msg = msg)
    #redundant register
    return render_template('register.html')
def password_okay(password):
    '''This method uses regex to check the password to meet criteria'''
    length = len(password)<12
    num = re.search(r"\d", password) is None
    capital = re.search(r"[A-Z]", password) is None
    lower = re.search(r"[a-z]", password) is None
    symbol = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    return not(length or num or capital or lower or symbol)
@app.route('/login/', methods =['GET','POST'])
def login():
    '''This creates the login webpage'''
    #returns the render
    msg = ''
    #when submit is clicked
    if request.method == 'POST':
        #try to log in with credentials
        try:
            #set user to user in appropriate database
            user=Users.query.filter_by(username = request.form['username']).first()
            if user.password==request.form['password']:
                msg = 'Congratulations, log in successful.'
                #render page with message
                return render_template('login.html', msg=msg)
        #if inaccurate username and password
        except AttributeError:
            app.logger.warning('Inaccurate credentials')
            msg = 'Incorrect credentials.'
            #render page with message
            return render_template('login.html', msg=msg)
    #redundant render
    return render_template('login.html', msg=msg)
