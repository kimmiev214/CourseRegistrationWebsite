'''
This is a flask program to create a website about lacrosse
'''
#imports
import datetime
import re
import logging
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#main
app = Flask(__name__)
db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    '''This runs immediately after the app starts'''
    db.create_all()
    logging.basicConfig(filename = 'myLog.log', level=logging.WARNING,
    format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

class Users(db.Model):
    '''Users database class'''
    username = db.Column('username', db.String, primary_key=True)
    password = db.Column(db.String)
def __init__(username, password):
    '''initialize function'''
    self.username = username
    self.password = password
@app.route('/about/')
def about():
    '''This creates the about webpage'''
    #returns the render
    return render_template('about.html')
@app.route('/gear/')
def gear():
    '''This creates the gear webpage'''
    #returns the render
    return render_template('gear.html')
@app.route('/welcome/')
def welcome():
    '''This creates the welcome webpage'''
    #returns the render
    return render_template('welcome.html', utc_dt=datetime.datetime.now())
@app.route('/links/')
def links():
    '''This creates the links webpage'''
    #returns the render
    return render_template('links.html')
@app.route('/photos/', methods =['GET','POST'])
def photos():
    '''This creates the photos webpage'''
    #returns the render
    return render_template('photos.html')
if __name__=='__main__':
    db.create_all()
    app.run(debug = True)
@app.route('/register/', methods =['GET','POST'])
def register():
    '''This creates the register webpage'''
    #returns the render
    if request.method == 'POST':
        if request.form['password'] == request.form['confirmpassword']:
            if password_okay(request.form['password']):
                if request.form['username']!="":
                    user = Users(username = request.form['username'],
                        password = request.form['password'])
                    db.session.add(user)
                    db.session.commit()
                    msg = "Success, user created."
                else:
                    msg = "Please add username"
            else:
                msg = ("Password must contain 1 uppercase, 1 lowercase, 1 number," +
                    " 1 special character, and be at least 12 characters long.")
        else:
            msg = "Password does not match Confirm Password box."
        return render_template('register.html', msg = msg)
    return render_template('register.html')
def password_okay(password):
    '''This method uses regex to check the password to meet criteria'''
    #this logic was found on stackoverflow.com will provide source if requested
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
    if request.method == 'POST':
        try:
            user=Users.query.filter_by(username = request.form['username']).first()
            if user.password==request.form['password']:
                msg = 'Congratulations, log in successful.'
                return render_template('login.html', msg=msg)
        except AttributeError:
            app.logger.warning('Inaccurate credentials')
            msg = 'Incorrect credentials.'
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)
