from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime   

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    matric_number = db.Column(db.String(120), nullable=False)
    gpa = db.Column(db.Integer, nullable=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    courses = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(120), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.Float, nullable=True)
    lecturer = db.Column(db.String(120), nullable=False)
 

class CourseRegistered(db.Model):
    __tablename__ = 'coursesregistered'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    gpa = db.Column(db.Float, nullable=True)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

