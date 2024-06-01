import datetime

from school import app
from flask import render_template, redirect, url_for, flash, request

from school.form import LoginForm, EventForm
from school.models import *
from flask_login import login_user


@app.route('/')
def hello_world():  # put application's code here
    return render_template("home/dashboard.html")


@app.route('/student', methods=['GET', 'POST'])
def student():
    students = Student.query.all()
    return render_template("home/student.html", student_data=students)


@app.route('/parent', methods=['GET', 'POST'])
def parent():  # put application's code here
    parents = Parent.query.all()
    return render_template("home/parent.html", parent_data=parents)


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():  # put application's code here
    teachers = Teacher.query.all()
    return render_template("home/teacher.html", teacher_data=teachers)


@app.route('/class', methods=['GET', 'POST'])
def classes():  # put application's code here
    class_info = Class.query.all()
    return render_template("home/class.html", class_data=class_info)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():  # put application's code here
    return render_template("home/dashboard.html")


@app.route('/calendar')
def index():
    events = Event.query.all()
    return render_template('home/calendar.html', events=events)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user: User = User.query.filter_by(email=form.email.data).first()
        role = attempted_user.get_role()
        if attempted_user and attempted_user.password == form.password.data:
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.email}', category='success')
            if role == 'admin':
                return redirect('dashboard')
            elif role == 'student':
                return redirect('student')
            elif role == 'teacher':
                return redirect('teacher')
            elif role == 'parent':
                return redirect('parent')
        else:
            flash('Email and password do not match! Please try again', category='danger')
    else:
        print(form.errors)

    return render_template("account/login.html", form=form)


@app.route("/logout")
def logout_page():
    login_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for("home_page"))


@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        student_id = request.form['student_id']
        student_class = request.form['class']
        parent_name = request.form['parent_name']

        Student.add(email, password, name, phone, address, gender, birthdate, student_id, student_class, parent_name)

        flash('Student inserted successfully')

    return redirect(url_for('student'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student_d = Student.query.filter_by(student_id=student_id).first()
        if student_d:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            address = request.form['address']
            gender = request.form['gender']
            print(gender)
            birthdate_form = request.form['birthdate']
            birthdate = datetime.strptime(birthdate_form, '%Y-%m-%d').date()
            student_id = request.form['student_id']
            student_class = request.form['class']
            parent_name = request.form['parent_name']

            student_d.update(email, password, name, phone, address, gender, birthdate, student_id, student_class, parent_name)

    return redirect(url_for('student'))
