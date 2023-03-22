from flask import request
from flask_restx import Resource, Namespace, fields
from extensions import db
from ..models import Student, Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('Auth', description='Authentication related operations')

admin_model = auth_namespace.model('Admin', {
    'email': fields.String(required=True, description='Email address of the admin'),
    'password': fields.String(required=True, description='Password of the admin'),
    'first_name': fields.String(required=True, description='First name of the admin'),
    'last_name': fields.String(required=True, description='Last name of the admin'),
    'is_admin': fields.Boolean(required=True, description='Is the user an admin?')
})

login_model = auth_namespace.model('Login', {
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

student_model = auth_namespace.model('Student', {
    'email': fields.String(required=True, description='Email address of the student'),
    'password': fields.String(required=True, description='Password of the student'),
    'first_name': fields.String(required=True, description='First name of the student'),
    'last_name': fields.String(required=True, description='Last name of the student'),
    'matric_number': fields.String(required=True, description='Matric number of the student'),
    'gpa': fields.Float(required=True, description='GPA of the student'),
    'courses': fields.Integer(required=True, description='Courses of the student')
})

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.doc('login_user', description='Login a user')
    @auth_namespace.expect(login_model)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        admin = Admin.query.filter_by(email=email).first()
        student = Student.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                access_token = create_access_token(identity=admin.id)
                refresh_token = create_refresh_token(identity=admin.id)
                return {
                    'message': 'Logged in as admin',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, HTTPStatus.OK
            else:
                return {'message': 'Invalid password'}, HTTPStatus.UNAUTHORIZED
        elif student:
            if check_password_hash(student.password, password):
                access_token = create_access_token(identity=student.id)
                refresh_token = create_refresh_token(identity=student.id)
                return {
                    'message': 'Logged in as student',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, HTTPStatus.OK
            else:
                return {'message': 'Invalid password'}, HTTPStatus.UNAUTHORIZED
        else:
            return {'message': 'Invalid email'}, HTTPStatus.UNAUTHORIZED
        
@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, HTTPStatus.OK
    
@auth_namespace.route("/logout")
class Logout(Resource):
    @jwt_required()
    def post(self):
        return {'message': 'Successfully logged out'}, HTTPStatus.OK