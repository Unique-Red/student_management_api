from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime   

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_number = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    course = db.relationship('CourseRegistered', backref='student', lazy=True)
    grade  = db.relationship('Grade', backref='student', lazy=True)
    

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(120), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    lecturer = db.Column(db.String(120), nullable=False)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 

class CourseRegistered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=True)

