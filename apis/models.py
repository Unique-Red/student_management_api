from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token, create_refresh_token
from functools import wraps
from http import HTTPStatus


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    gpa = db.Column(db.Float, nullable=True, default=0.0)
    password = db.Column(db.String(120), nullable=False, default='studentMA')
    course = db.relationship('CourseRegistered', backref='student', lazy=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(120), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    lecturer = db.Column(db.String(120), nullable=False)
    registered_courses = db.relationship('CourseRegistered', backref='course', lazy=True)
    student_registered = db.relationship('CourseRegistered', viewonly=True, overlaps="course, registered_courses")

    def __repr__(self):
        return '<Course %r>' % self.course_code


class CourseRegistered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=True)
    grade = db.Column(db.String(2), nullable=True)
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(120), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    stud_id = db.Column(db.String(80), nullable=False)
    lecturer = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<CourseRegistered %r>' % self.course_code
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=True)

