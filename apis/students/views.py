from flask_restx import Resource, fields, Namespace, abort
from extensions import db
from ..models import Student, Courses, CourseRegistered, Grade
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token,create_refresh_token
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

student_namespace = Namespace('Students', description='Student related operations')

student_register = student_namespace.model('StudentRegister', {
    'first_name': fields.String(required=True, description="The student's first name"),
    'last_name': fields.String(required=True, description="The student's last name"),
    'email': fields.String(required=True, description='The student email'),
    "matric_number": fields.String(required=True, description='The student matric number'),
    'password': fields.String(required=True, description='The student password')
})

student_login = student_namespace.model('StudentLogin', {
    'email': fields.String(required=True, description='The student email'),
    'password': fields.String(required=True, description='The student password')
})

student = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The student identifier'),
    'first_name': fields.String(required=True, description="The student's first name"),
    'last_name': fields.String(required=True, description="The student's last name"),
    'email': fields.String(required=True, description='The student email'),
    "matric_number": fields.String(required=True, description='The student matric number'),
    'password': fields.String(required=True, description='The student password')    
})

grade = student_namespace.model('Grade', {
    'id': fields.Integer(required=True, description='The grade identifier'),
    'percentage': fields.Float(required=True, description='The student grade'),
    'course_id': fields.Integer(required=True, description='The course identifier'),
    'student_id': fields.Integer(required=True, description='The student identifier')
})

course = student_namespace.model('Course', {
    'id': fields.Integer(required=True, description='The course identifier'),
    'course_name': fields.String(required=True, description='The course name'),
    'course_code': fields.String(required=True, description='The course code'),
    'course_unit': fields.Integer(required=True, description='The course unit'),
    'student_id': fields.Integer(required=True, description='The student identifier')
})



def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        student = get_jwt_identity()
        if student['is_admin'] == False:
            return f(*args, **kwargs)
        else:
            return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        admin = get_jwt_identity()
        if admin['is_admin'] == True:
            return f(*args, **kwargs)
        else:
            return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
    return decorated_function

@student_namespace.route('/register')
class Register(Resource):
    @student_namespace.doc('register_student')
    @student_namespace.expect(student_register)
    @student_namespace.marshal_with(student, code=201)
    def post(self):
        data = student_namespace.payload
        student = Student.query.filter_by(email=data['email']).first()
        if student:
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST
        else:
            new_student = Student(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                matric_number=data['matric_number'],
                password=generate_password_hash(data['password'])
            )
            db.session.add(new_student)
            db.session.commit()
            return new_student, HTTPStatus.CREATED

@student_namespace.route('/login')
class Login(Resource):
    @student_namespace.doc('login_student')
    @student_namespace.expect(student_login)
    def post(self):
        data = student_namespace.payload
        student = Student.query.filter_by(email=data['email']).first()
        if student and check_password_hash(student.password, data['password']):
            access = create_access_token(identity=student.id)
            refresh = create_refresh_token(identity=student.id)
            return {
                'access_token': access,
                'refresh_token': refresh
            }, HTTPStatus.OK
        else:
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        
@student_namespace.route('/<int:id>')
@student_namespace.param('id', 'The student identifier')
@student_namespace.response(404, 'Student not found')
class StudentResource(Resource):
    @student_namespace.doc('get_student')
    @student_namespace.marshal_with(student)
    def get(self, id):
        student = Student.query.get_or_404(id)
        return student, HTTPStatus.OK
    
    @student_namespace.doc('update_student')
    @student_namespace.expect(student)
    @student_namespace.marshal_with(student)
    @admin_required
    def put(self, id):
        data = student_namespace.payload
        student = Student.query.get_or_404(id)
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.matric_number = data['matric_number']
        student.grade = data['grade']
        student.password = data['password']
        db.session.commit()
        return student, HTTPStatus.OK
    
    @student_namespace.doc('delete_student')
    @student_namespace.response(204, 'Student deleted')
    def delete(self, id):
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    
@student_namespace.route('/<int:id>/courses')
@student_namespace.param('id', 'The student identifier')
@student_namespace.response(404, 'Student not found')
class StudentCoursesResource(Resource):
    @student_namespace.doc('get_student_courses')
    def get(self, id):
        student = Student.query.get_or_404(id)
        courses = student.courses
        return courses, HTTPStatus.OK
    
    @student_namespace.doc('add_student_course')
    @student_namespace.expect(course)
    @student_namespace.marshal_with(course, code=201)
    def post(self, id):
        data = student_namespace.payload
        student = Student.query.get(id)
        if not student:
            abort(404, message="Student {} doesn't exist".format(id))
        courses = Courses.query.get(data['id'])
        if not courses:
            abort(404, message="Course {} doesn't exist".format(data['course_title']))
        student.courses.append(courses)
        db.session.commit()
        return courses, HTTPStatus.CREATED
    
@student_namespace.route('/<int:id>/grades')
@student_namespace.param('id', 'The student identifier')
@student_namespace.response(404, 'Student not found')
class StudentGradesResource(Resource):
    @student_namespace.doc('get_student_grades')
    def get(self, id):
        student = Student.query.get_or_404(id)
        grades = student.grade
        return grades, HTTPStatus.OK
    
    @student_namespace.doc('add_student_grade')
    @student_namespace.expect(grade)
    @student_namespace.marshal_with(grade, code=201)
    def post(self, id):
        data = student_namespace.payload
        student = Student.query.get(id)
        if not student:
            abort(404, message="Student {} doesn't exist".format(id))
        courses = Courses.query.get(data['course_id'])
        if not courses:
            abort(404, message="Course {} doesn't exist".format(data['course_id']))
        new_grade = Grade(
            percentage=data['grade'],
            course_id=courses.id,
            student_id=student.id
        )
        db.session.add(new_grade)
        db.session.commit()
        return new_grade, HTTPStatus.CREATED
    

    
@student_namespace.route('/<int:id>/courses/<int:course_id>')
@student_namespace.param('id', 'The student identifier')
@student_namespace.param('course_id', 'The course identifier')
@student_namespace.response(404, 'Student not found')
class StudentCourseResource(Resource):
    @student_namespace.doc('get_student_course')
    def get(self, id, course_id):
        student = Student.query.get_or_404(id)
        course = Courses.filter_by(id=course_id).first()
        return course, HTTPStatus.OK
    
    @student_namespace.doc('delete_student_course')
    @student_namespace.response(204, 'Student course deleted')
    def delete(self, id, course_id):
        student = Student.query.get_or_404(id)
        course = student.courses.filter_by(id=course_id).first()
        student.courses.remove(course)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
    
@student_namespace.route('/<int:id>/grades/<int:grade_id>')
@student_namespace.param('id', 'The student identifier')
@student_namespace.param('grade_id', 'The grade identifier')
@student_namespace.response(404, 'Student not found')
class StudentGradeResource(Resource):
    @student_namespace.doc('get_student_grade')
    def get(self, id, grade_id):
        student = Student.query.get_or_404(id)
        grade = student.grades.filter_by(id=grade_id).first()
        return grade, HTTPStatus.OK
    
    @student_namespace.doc('delete_student_grade')
    @student_namespace.response(204, 'Student grade deleted')
    def delete(self, id, grade_id):
        student = Student.query.get_or_404(id)
        grade = student.grades.filter_by(id=grade_id).first()
        student.grades.remove(grade)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT

    @student_namespace.doc('update_student_grade')
    @student_namespace.expect(grade)
    @student_namespace.marshal_with(grade)
    def put(self, id, grade_id):
        data = student_namespace.payload
        student = Student.query.get_or_404(id)
        grade = student.grades.filter_by(id=grade_id).first()
        grade.grade = data['grade']
        db.session.commit()
        return grade, HTTPStatus.OK
    

