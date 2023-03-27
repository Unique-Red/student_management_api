from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Admin
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

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


admin_namespace = Namespace('Admin', description='Admin related operations')

admin = admin_namespace.model('Admin', {
    'id': fields.Integer(required=True, description='The admin identifier'),
    "first_name": fields.String(required=True, description='The admin first name'),
    "last_name": fields.String(required=True, description='The admin last name'),
    "email": fields.String(required=True, description='The admin email'),
    "password": fields.String(required=True, description='The admin password'),
    "is_admin": fields.Boolean(required=True, description="True if admin, False if not")
})

admin_register = admin_namespace.model('AdminRegister', {
    "first_name": fields.String(required=True, description='The admin first name'),
    "last_name": fields.String(required=True, description='The admin last name'),
    "email": fields.String(required=True, description='The admin email'),
    "password": fields.String(required=True, description='The admin password')
})


@admin_namespace.route('/register')
class Register(Resource):
    @admin_namespace.doc('register_admin')
    @admin_namespace.expect(admin_register)
    @admin_namespace.marshal_with(admin, code=201)
    def post(self):
        data = admin_namespace.payload
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin:
            return {'message': 'Admin already exists'}, HTTPStatus.BAD_REQUEST
        else:
            new_admin = Admin(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=generate_password_hash(data['password']),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            return new_admin, HTTPStatus.CREATED
        
@admin_namespace.route('/login')
class Login(Resource):
    @admin_namespace.doc('login_admin')
    @admin_namespace.expect(admin_register)
    @admin_namespace.marshal_with(admin, code=200)
    def post(self):
        data = admin_namespace.payload
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin and check_password_hash(admin.password, data['password']):
            return admin, HTTPStatus.OK
        else:
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        
@admin_namespace.route('/<int:id>')
class AdminDetails(Resource):
    @admin_namespace.doc('get_admin')
    @admin_namespace.marshal_with(admin, code=200)
    @admin_required
    def get(self, id):
        admin = Admin.query.get_or_404(id)
        return admin, HTTPStatus.OK
    
    @admin_namespace.doc('delete_admin')
    @admin_required
    def delete(self, id):
        admin = Admin.query.get_or_404(id)
        db.session.delete(admin)
        db.session.commit()
        return {}, HTTPStatus.NO_CONTENT

    @admin_namespace.doc('update_admin')
    @admin_required
    @admin_namespace.expect(admin)
    @admin_namespace.marshal_with(admin, code=200)
    def put(self, id):
        data = admin_namespace.payload
        admin = Admin.query.get_or_404(id)
        admin.first_name = data['first_name']
        admin.last_name = data['last_name']
        admin.email = data['email']
        admin.password = generate_password_hash(data['password'])
        admin.is_admin = data['is_admin']
        db.session.add(admin)
        db.session.commit()
        return admin, HTTPStatus.OK
    
