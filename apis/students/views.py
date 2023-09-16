from flask_restx import Resource, fields, Namespace, abort
from extensions import db
from ..models import Student
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token,create_refresh_token
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint

matric_number = randint(1000000000, 9999999999)

authorizations = {
    "jsonwebtoken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

student_namespace = Namespace('Students', authorizations=authorizations, description='Student related operations')

courses_registered_model = student_namespace.model('Courses Registered', {
    'id': fields.Integer(readOnly=True, description='The course registered unique identifier'),
    'student_id': fields.Integer(required=True, description='The student id'),
    'course_id': fields.Integer(required=True, description='The course id'),
    'date_registered': fields.DateTime(required=True, description='The date registered')
})

course_model = student_namespace.model('Course', {
    'id': fields.Integer(readOnly=True, description='The course unique identifier'),
    'course_code': fields.String(required=True, description='Course code'),
    'course_title': fields.String(required=True, description='Course title'),
    'course_unit': fields.Integer(required=True, description='Course unit'),
    'lecturer': fields.String(required=True, description='Lecturer')
})

grade_model = student_namespace.model('Grade', {
    'id': fields.Integer(readOnly=True, description='The grade unique identifier'),
    'course_id': fields.Integer(required=True, description='The course id'),
    'student_id': fields.Integer(required=True, description='The student id'),
    'percentage': fields.Float(required=True, description='The percentage'),
    'date_registered': fields.DateTime(required=True, description='The date registered')
})

student_model = student_namespace.model('Student', {
    'id': fields.Integer(readOnly=True, description='The student unique identifier'),
    'matric_number': fields.Integer(required=True, description='The student matric number'),
    'first_name': fields.String(required=True, description='The student first name'),
    'last_name': fields.String(required=True, description='The student last name'),
    'email': fields.String(required=True, description='The student email address'),
    'grade': fields.List(fields.Nested(grade_model), description='The student grade'),
    'course': fields.List(fields.Nested(courses_registered_model), description='The student course registered'),
    
})

student_input_model = student_namespace.model('Student Input', {
    'first_name': fields.String(required=True, description='The student first name'),
    'last_name': fields.String(required=True, description='The student last name'),
    'email': fields.String(required=True, description='The student email address')
})


@student_namespace.route('/students')
class StudentListAPI(Resource):
    @student_namespace.marshal_list_with(student_model)
    def get(self):
        students = Student.query.all()
        
        return students, HTTPStatus.OK
    

    
    @student_namespace.expect(student_input_model)
    @student_namespace.marshal_with(student_model)
    def post(self):
        matric_number = randint(1000000000, 9999999999)
        student = Student(matric_number=matric_number, first_name=student_namespace.payload['first_name'], last_name=student_namespace.payload['last_name'], email=student_namespace.payload['email'])
        if Student.query.filter_by(matric_number=matric_number).first():
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST
        if Student.query.filter_by(email=student_namespace.payload['email']).first():
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST
        db.session.add(student)
        db.session.commit()
        return student, HTTPStatus.CREATED
    
@student_namespace.route('/students/<int:id>')
class StudentAPI(Resource):
    @student_namespace.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get_or_404(id)
        return student, HTTPStatus.OK
    
    @student_namespace.expect(student_input_model)
    @student_namespace.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get_or_404(id)
        student.matric_number = randint(1000000000, 9999999999)
        student.first_name = student_namespace.payload['first_name']
        student.last_name = student_namespace.payload['last_name']
        student.email = student_namespace.payload['email']
        student.password = generate_password_hash(student_namespace.payload['password'])
        db.session.commit()
        return student, HTTPStatus.OK
    
    @student_namespace.marshal_with(student_model)
    def delete(self, id):
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT