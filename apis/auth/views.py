from flask import request
from flask_restx import Resource, Namespace, fields
from extensions import db
from ..models import Student, Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

authorizations = {
    "jsonwebtoken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

auth_namespace = Namespace('Auth', authorizations=authorizations, description='Authentication related operations')

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

change_student_password_model = auth_namespace.model('Change Student Password', {
    'matric_number': fields.Integer(required=True, description='Matric number of the student'),
    'password': fields.String(required=True, description='Password of the student')
})


@auth_namespace.route('/register')
class RegisterAPI(Resource):
    @auth_namespace.expect(admin_model)
    def post(self):
        admin = Admin(email=auth_namespace.payload['email'], password=generate_password_hash(auth_namespace.payload['password'], method='sha256'), first_name=auth_namespace.payload['first_name'], last_name=auth_namespace.payload['last_name'], is_admin=auth_namespace.payload['is_admin'])
        if Admin.query.filter_by(email=auth_namespace.payload['email']).first():
            return {'message': 'Admin already exists'}, HTTPStatus.BAD_REQUEST
        if len(auth_namespace.payload['password']) < 6:
            return {'message': 'Password must be at least 6 characters'}, HTTPStatus.BAD_REQUEST
        
        db.session.add(admin)
        db.session.commit()
        return {'message': 'Admin created successfully'}, HTTPStatus.CREATED
    
@auth_namespace.route('/login')
class LoginAPI(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        admin = Admin.query.filter_by(email=auth_namespace.payload['email']).first()
        if not admin:
            return {'message': 'Admin does not exist'}, HTTPStatus.NOT_FOUND
        if not check_password_hash(admin.password, auth_namespace.payload['password']):
            return {'message': 'Incorrect password'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=admin.id, fresh=True)
        refresh_token = create_refresh_token(identity=admin.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
    
# student authentification
student_login_model = auth_namespace.model('Student Login', {
    'matric_number': fields.Integer(required=True, description='Matric number of the student'),
    'password': fields.String(required=True, description='Password of the student')
})

@auth_namespace.route('/student/login')
class StudentLoginAPI(Resource):
    @auth_namespace.expect(student_login_model)
    def post(self):
        student = Student.query.filter_by(matric_number=auth_namespace.payload['matric_number']).first()
        if not student:
            return {'message': 'Student does not exist'}, HTTPStatus.NOT_FOUND
        # check default password
        if student.password == 'studentMA':
            return {'message': 'Please change your password'}, HTTPStatus.UNAUTHORIZED
        if not check_password_hash(student.password, auth_namespace.payload['password']):
            return {'message': 'Incorrect password'}, HTTPStatus.UNAUTHORIZED
        access_token = create_access_token(identity=student.id, fresh=True)
        refresh_token = create_refresh_token(identity=student.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
    
@auth_namespace.route('/student/change-password')
class StudentChangePasswordAPI(Resource):
    @auth_namespace.expect(change_student_password_model)
    def post(self):
        student = Student.query.filter_by(matric_number=auth_namespace.payload['matric_number']).first()
        if not student:
            return {'message': 'Student does not exist'}, HTTPStatus.NOT_FOUND
        student.password = generate_password_hash(auth_namespace.payload['password'], method='sha256')
        db.session.commit()
        return {'message': 'Password changed successfully'}, HTTPStatus.OK