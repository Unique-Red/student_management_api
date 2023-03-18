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

@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(admin_model)
    def post(self):
        data = request.get_json()
        user = Admin.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST
        new_user = Admin(
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            is_admin=data.get('is_admin')
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, HTTPStatus.CREATED
    
    @auth_namespace.expect(student_model)
    def post(self):
        data = request.get_json()
        user = Student.query.filter_by(email=data.get('email')).first()
        if user:
            return {'message': 'User already exists'}, HTTPStatus.BAD_REQUEST
        new_user = Student(
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            matric_number=data.get('matric_number'),
            gpa=data.get('gpa')
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, HTTPStatus.CREATED
    
@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(admin_model)
    def post(self):
        data = request.get_json()
        user = Admin.query.filter_by(email=data.get('email')).first()
        if not user or not check_password_hash(user.password, data.get('password')):
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)
        return {
            'message': 'Logged in as {}'.format(user.email),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.OK
    
    @auth_namespace.expect(student_model)
    def post(self):
        data = request.get_json()
        user = Student.query.filter_by(email=data.get('email')).first()
        if not user or not check_password_hash(user.password, data.get('password')):
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)
        return {
            'message': 'Logged in as {}'.format(user.email),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.OK
    
