'''
This is a flask program to create a course registration website for a hypothetical university
'''
#imports
from vmuniversity_flask import app, db, bcrypt
from vmuniversity_flask.forms import RegistrationForm, LoginForm, AdminForm, CreateCourseForm
from vmuniversity_flask.models import User, Course
from flask import redirect, render_template, url_for, flash
import re
from flask_login import  login_user, logout_user, current_user


#the @app.route command determines what happens when the given hyperlink is clicked
@app.route('/register/', methods =['GET','POST'])
def register():
    '''This creates the register webpage'''
    form=RegistrationForm()
    if form.validate_on_submit():
        encrypted_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration Page', form=form)

@app.route('/login/', methods =['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('studentaccount'))
    '''This creates the login webpage'''
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Login successful for {form.email.data}', category='success')
            return redirect(url_for('welcome'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/administration/', methods =['POST', 'GET'])
def administration():
    '''This creates the administration webpage'''
    form=AdminForm()
    if form.validate_on_submit():
        if form.email.data=='admin.access@vmu.edu' and form.password.data=='adminS3tup@cc3ss!':
            flash(f'Successfully logged in as Administrator for {form.email.data}', category='success')
            return redirect(url_for('admincourses'))
        else:
            flash(f'Login unsuccessful for {form.email.data}', category='danger')
    #returns the render
    return render_template('administration.html', title='Administration Page', form=form)

@app.route('/')
def welcome():
    '''This creates the welcome webpage'''
    #returns the render
    return render_template('welcome.html', title='Welcome Page')
headings = ('Course Number','Title','Options')
data = (
    ('CSVMU150','Introduction to Computer Science'),
    ('CSVMU160','Introduction to Python'),
    ('CSVMU200','Intermediate Programming'),
    ('CSVMU310','Introduction to Data Structures'),
    ('CSVMU332','History of Technology Innovation'),
    ('CSVMU415','Computer Graphics'),
    ('CSVMU425','Compiler Theory and Design'),
    ('CSVMU490','Projects and Trends in Computer Science')
    )
@app.route('/courses/')
def courses():
    '''This creates the courses webpage'''
    #returns the render
    return render_template('courses.html', title='Course Page', headings = headings, data = data)

@app.route('/studentaccount/')
def studentaccount():
    '''This creates the student courses webpage'''
    #returns the render
    return render_template('studentaccount.html', title='My Account', headings = headings, data = data)

@app.route('/admincourses/', methods =['POST', 'GET'])
def admincourses():
    '''This creates the admin webpage'''
    form=CreateCourseForm()
    if form.validate_on_submit():
        course=Course(name=form.name.data, description=form.description.data, professor=form.professor.data)
        db.session.add(course)
        db.session.commit()
        flash(f'Course created successfully for {form.name.data}', category='success')
    #returns the render
    return render_template('admincourses.html', title='Admin Access Page', form=form)

def password_okay(password):
    '''This method uses regex to check the password to meet criteria'''
    length = len(password)<12
    num = re.search(r"\d", password) is None
    capital = re.search(r"[A-Z]", password) is None
    lower = re.search(r"[a-z]", password) is None
    symbol = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    return not(length or num or capital or lower or symbol)
