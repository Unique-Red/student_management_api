from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Admin
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

admin_namespace = Namespace('Admin', description='Admin related operations')

admin = admin_namespace.model('Admin', {
    'id': fields.Integer(required=True, description='The admin identifier'),
    "first name": fields.String(required=True, description='The admin first name'),
    "last name": fields.String(required=True, description='The admin last name'),
    "email": fields.String(required=True, description='The admin email'),
    "password": fields.String(required=True, description='The admin password')
})

admin_register = admin_namespace.model('Admin', {
    "first name": fields.String(required=True, description='The admin first name'),
    "last name": fields.String(required=True, description='The admin last name'),
    "email": fields.String(required=True, description='The admin email'),
    "password": fields.String(required=True, description='The admin password')
})

@admin_namespace.route('/')
class AdminRegister(Resource):
    @admin_namespace.doc('register_admin', description='Register an admin')
    @admin_namespace.expect(admin_register)
    def post(self):
        admin = Admin(
            first_name=request.json['first name'],
            last_name=request.json['last name'],
            email=request.json['email'],
            password = generate_password_hash(request.json['password'])
        )
        db.session.add(admin)
        db.session.commit()
        return {'message': 'Admin created successfully'}, HTTPStatus.CREATED
    
    @admin_namespace.doc('get_all_admins', description='Get all admins')
    @admin_namespace.marshal_list_with(admin)
    def get(self):
        admins = Admin.query.all()
        return admins, HTTPStatus.OK
    
    @admin_namespace.doc('get_admin_by_id', description='Get an admin by id')
    @admin_namespace.marshal_with(admin)
    def get(self, id):
        admin = Admin.query.get(id)
        return admin, HTTPStatus.OK
    
    @admin_namespace.doc('update_admin', description='Update an admin')
    @admin_namespace.expect(admin)
    def put(self, id):
        admin = Admin.query.get(id)
        admin.first_name = request.json['first name']
        admin.last_name = request.json['last name']
        admin.email = request.json['email']
        admin.password = request.json['password']
        db.session.commit()
        return {'message': 'Admin updated successfully'}, HTTPStatus.OK
    
    @admin_namespace.doc('delete_admin', description='Delete an admin')
    def delete(self, id):
        admin = Admin.query.get(id)
        db.session.delete(admin)
        db.session.commit()
        return {'message': 'Admin deleted successfully'}, HTTPStatus.OK
    
@admin_namespace.route('/login')
class AdminLogin(Resource):
    @admin_namespace.doc('login_admin', description='Login an admin')
    @admin_namespace.expect(admin)
    def post(self):
        admin = Admin.query.filter_by(email=request.json['email']).first()
        if admin and check_password_hash(admin.password, request.json['password']):
            return {'message': 'Login successful'}, HTTPStatus.OK
        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
    
