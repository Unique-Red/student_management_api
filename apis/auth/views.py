from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,get_jwt_identity, get_raw_jwt
from ..utils import db
from ..models.students import Student
from http import HTTPStatus


student_namespace = Namespace('Students', description='Student related operations')

student_signup = student_namespace.model('StudentSignUp', {
    'id': fields.Integer(required=True, description='The student identifier'),
    'name': fields.String(required=True, description='The student name'),
    'email': fields.String(required=True, description='The student email'),
    'password': fields.String(required=True, description='The student password')
})

student_login = student_namespace.model('StudentLogin', {
    'email': fields.String(required=True, description='The student email'),
    'password': fields.String(required=True, description='The student password')
})

@student_namespace.route('/register')
class StudentRegister(Resource):
    @student_namespace.doc('register_student')
    @student_namespace.expect(student_signup)
    def post(self):
        student = Student(**student_namespace.payload)
        db.session.add(student)
        db.session.commit()
        return {'message': 'Student created successfully'}, HTTPStatus.CREATED

@student_namespace.route('/login')
class StudentLogin(Resource):
    @student_namespace.doc('login_student')
    @student_namespace.expect(student_login)
    def post(self):
        student = Student.query.filter_by(email=student_namespace.payload['email']).first()
        if student and student.check_password(student_namespace.payload['password']):
            access_token = create_access_token(identity=student.id)
            refresh_token = create_refresh_token(identity=student.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
    
@student_namespace.route('/refresh')
class StudentRefresh(Resource):
    @student_namespace.doc('refresh_student')
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, HTTPStatus.OK
    