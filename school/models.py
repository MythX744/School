import sqlite3
from datetime import datetime

from school import db, app, login_manager
from school import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(1024), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(1024), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)

    def __init__(self, email, password, name, phone, address, gender, birthdate):
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address
        self.gender = gender
        self.birthdate = birthdate

    def get_role(self):
        if Admin.query.get(self.id):
            return 'admin'
        elif Student.query.get(self.id):
            return 'student'
        elif Teacher.query.get(self.id):
            return 'teacher'
        elif Parent.query.get(self.id):
            return 'parent'
        else:
            return 'None'

    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    school_name = db.Column(db.String(1024), nullable=False)

    def __init__(self, email, password, name, phone, address, gender, birthdate, school_name):
        super().__init__(email=email, password=password, name=name, phone=phone, address=address, gender=gender,
                         birthdate=birthdate)
        self.school_name = school_name

    @staticmethod
    def add(email, password, name, phone, address, gender, birthdate, school_name):
        admin = Admin(email, password, name, phone, address, gender, datetime.strptime(birthdate, "%Y-%m-%d"),
                      school_name)
        db.session.add(admin)
        db.session.commit()


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    parent_name = db.Column(db.String, db.ForeignKey('parent.id'), nullable=False)
    assigned_teachers = db.relationship('Teacher', secondary='student_teacher_association', backref='assigned_students')
    parent = db.relationship("Parent", foreign_keys=[parent_name])
    
    def __init__(self, email, password, name, phone, address, gender, birthdate, student_id, class_id, parent_name):
        super().__init__(email=email, password=password, name=name, phone=phone, address=address, gender=gender,
                         birthdate=birthdate)
        self.student_id = student_id
        self.class_id = class_id
        self.parent_name = parent_name

    @staticmethod
    def add(email, password, name, phone, address, gender, birthdate, student_id, class_id, parent_name):
        student = Student(email, password, name, phone, address, gender, datetime.strptime(birthdate, "%Y-%m-%d"),
                      student_id, class_id, parent_name)
        db.session.add(student)
        db.session.commit()

    def update(self, email, password, name, phone, address, gender, birthdate, student_id, class_id, parent_name):
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address
        self.gender = gender
        self.birthdate = birthdate
        self.student_id = student_id
        self.class_id = class_id
        self.parent_name = parent_name

        db.session.commit()


student_teacher_association = db.Table('student_teacher_association',
                                       db.Column('student_id', db.Integer, db.ForeignKey('student.id'),
                                                 primary_key=True),
                                       db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'),
                                                 primary_key=True)
                                       )


class Parent(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)

    def __init__(self, email, password, name, phone, address, gender, birthdate):
        super().__init__(email=email, password=password, name=name, phone=phone, address=address, gender=gender,
                         birthdate=birthdate)

    @staticmethod
    def add(email, password, name, phone, address, gender, birthdate):
        parent = Parent(email, password, name, phone, address, gender, datetime.strptime(birthdate, "%Y-%m-%d"))
        db.session.add(parent)
        db.session.commit()


class Teacher(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subjects = db.relationship('Subject', primaryjoin='Teacher.subject_id == Subject.id', backref='Teacher')

    def __init__(self, email, password, name, phone, address, gender, birthdate):
        super().__init__(email=email, password=password, name=name, phone=phone, address=address, gender=gender,
                         birthdate=birthdate)

    @staticmethod
    def add(email, password, name, phone, address, gender, birthdate):
        teacher = Teacher(email, password, name, phone, address, gender, datetime.strptime(birthdate, "%Y-%m-%d"))
        db.session.add(teacher)
        db.session.commit()


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        self.name = name


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        self.name = name


class ClassTeacherAssociation(db.Model):
    __tablename__ = 'class_teacher_association'
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), primary_key=True)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Event {self.name}>'


with app.app_context():
    db.create_all()
