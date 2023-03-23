from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Student, Courses, CourseRegistered
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

student_namespace = Namespace('Students', description='Student related operations')


student = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The student identifier'),
    'first_name': fields.String(required=True, description="The student's first name"),
    'last_name': fields.String(required=True, description="The student's last name"),
    'email': fields.String(required=True, description='The student email'),
    "matric_number": fields.String(required=True, description='The student matric number'),
    'gpa': fields.Float(required=True, description='The student grade')
})

gpa = student_namespace.model('GPA', {
    "student_id": fields.Integer(required=True, description='The student identifier'),
    "course_code": fields.String(required=True, description='The course code'),
    'gpa': fields.Float(required=True, description='The student grade')
})


@student_namespace.route('/register')
class Register(Resource):
    @student_namespace.doc('register_student')
    @student_namespace.expect(student)
    @student_namespace.marshal_with(student, code=201)
    @jwt_required
    def post(self):
        admin = get_jwt_identity()
        student = Student.query.filter_by(email=request.json['email']).first()
        if student:
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST 
        elif admin['is_admin'] == True:
            new_student = Student(
                first_name=request.json['first_name'],
                last_name=request.json['last_name'],
                email=request.json['email'],
                matric_number=request.json['matric_number'],
                gpa=request.json['gpa']
            )
            db.session.add(new_student)
            db.session.commit()
            return new_student, HTTPStatus.CREATED
        else:
            return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
        
@student_namespace.route('/register_course')
class RegisterCourse(Resource):
    @student_namespace.doc('register_course')
    @student_namespace.expect(gpa)
    @student_namespace.marshal_with(gpa, code=201)
    @jwt_required
    def post(self):
        admin = get_jwt_identity()
        course = Courses.query.filter_by(course_code=request.json['course_code']).first()
        student = Student.query.filter_by(matric_number=request.json['matric_number']).first()
        if course and student:
            if admin['is_admin'] == True:
                new_course = CourseRegistered(
                    student_id=student.id,
                    course_code=request.json['course_code'],
                    gpa=request.json['gpa']
                )
                db.session.add(new_course)
                db.session.commit()
                return new_course, HTTPStatus.CREATED
            else:
                return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
        else:
            return {'message': 'Course or Student does not exist'}, HTTPStatus.BAD_REQUEST
    
    @student_namespace.doc('update_course')
    @student_namespace.expect(gpa)
    @student_namespace.marshal_with(gpa, code=200)
    @jwt_required
    def put(self):
        admin = get_jwt_identity()
        course = CourseRegistered.query.filter_by(course_code=request.json['course_code']).first()
        if course:
            if admin['is_admin'] == True:
                course.gpa = request.json['gpa']
                db.session.commit()
                return course, HTTPStatus.OK
            else:
                return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
        else:
            return {'message': 'Course does not exist'}, HTTPStatus.BAD_REQUEST
        
    @student_namespace.doc('delete_course')
    @student_namespace.expect(gpa)
    @student_namespace.marshal_with(gpa, code=200)
    @jwt_required
    def delete(self):
        admin = get_jwt_identity()
        course = CourseRegistered.query.filter_by(course_code=request.json['course_code']).first()
        if course:
            if admin['is_admin'] == True:
                db.session.delete(course)
                db.session.commit()
                return course, HTTPStatus.OK
            else:
                return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
        else:
            return {'message': 'Course does not exist'}, HTTPStatus.BAD_REQUEST
        
@student_namespace.route('/all')
class AllStudents(Resource):
    @student_namespace.doc('get_all_students')
    @student_namespace.marshal_with(student, code=200)
    @jwt_required
    def get(self):
        admin = get_jwt_identity()
        if admin['is_admin'] == True:
            students = Student.query.all()
            return students, HTTPStatus.OK
        else:
            return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED
    
    @student_namespace.doc('delete_all_students')
    @student_namespace.marshal_with(student, code=200)
    @jwt_required
    def delete(self):
        admin = get_jwt_identity()
        if admin['is_admin'] == True:
            students = Student.query.all()
            for student in students:
                db.session.delete(student)
                db.session.commit()
            return students, HTTPStatus.OK
        else:
            return {'message': 'You are not authorized to perform this action'}, HTTPStatus.UNAUTHORIZED


@student_namespace.route('/<string:matric_number>')
class StudentDetails(Resource):
    @student_namespace.doc('get_student_details')
    @student_namespace.marshal_with(student, code=200)
    def get(self, matric_number):
        student = Student.query.filter_by(matric_number=matric_number).first()
        return student, HTTPStatus.OK

    @student_namespace.doc('delete_student')
    @student_namespace.marshal_with(student, code=200)
    def delete(self, matric_number):
        student = Student.query.filter_by(matric_number=matric_number).first()
        db.session.delete(student)
        db.session.commit()
        return student, HTTPStatus.OK
    
    
@student_namespace.route('/gpa/<string:matric_number>')
class GPA(Resource):
    @student_namespace.doc('get_student_gpa')
    @student_namespace.marshal_with(student, code=200)
    def get(self, matric_number):
        student = Student.query.filter_by(matric_number=matric_number).first()
        return student, HTTPStatus.OK
    
    @student_namespace.doc('update_student_gpa')
    @student_namespace.expect(gpa)
    @student_namespace.marshal_with(student, code=200)
    def put(self, matric_number):
        student = Student.query.filter_by(matric_number=matric_number).first()
        data = student_namespace.payload()
        student.gpa = data['gpa']
        db.session.commit()
        return student, HTTPStatus.OK