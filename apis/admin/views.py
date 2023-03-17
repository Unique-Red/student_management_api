from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Admin
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

admin_namespace = Namespace('Admin', description='Admin related operations')

admin = admin_namespace.model('Admin', {
    'id': fields.Integer(required=True, description='The admin identifier'),
    "first name": fields.String(required=True, description='The admin first name'),
    "last name": fields.String(required=True, description='The admin last name'),
    "email": fields.String(required=True, description='The admin email'),
    "password": fields.String(required=True, description='The admin password')
})

@admin_namespace.route('/register')
class Register(Resource):
    @admin_namespace.doc('register_admin')
    @admin_namespace.expect(admin)
    @admin_namespace.marshal_with(admin, code=201)
    def post(self):
        admin = Admin(
            first_name=request.json['first name'],
            last_name=request.json['last name'],
            email=request.json['email'],
            password=request.json['password']
        )
        db.session.add(admin)
        db.session.commit()

        return admin, HTTPStatus.CREATED
    
    @admin_namespace.doc('get_all_admins')
    @admin_namespace.marshal_with(admin, code=200)
    def get(self):
        admins = Admin.query.all()
        return admins, HTTPStatus.OK
    
@admin_namespace.route('/register/<int:admin_id>')
class Register(Resource):
    @admin_namespace.doc('get_admin_by_id')
    @admin_namespace.marshal_with(admin, code=200)
    def get(self, admin_id):
        admin = Admin.query.filter_by(id=admin_id).first()
        return admin, HTTPStatus.OK

    @admin_namespace.doc('delete_admin_by_id')
    @admin_namespace.marshal_with(admin, code=200)
    def delete(self, admin_id):
        admin = Admin.query.filter_by(id=admin_id).first()
        db.session.delete(admin)
        db.session.commit()
        return admin, HTTPStatus.OK

    @admin_namespace.doc('update_admin_by_id')
    @admin_namespace.marshal_with(admin, code=200)
    def put(self, admin_id):
        admin = Admin.query.filter_by(id=admin_id).first()
        admin.first_name = request.json['first name']
        admin.last_name = request.json['last name']
        admin.email = request.json['email']
        admin.password = request.json['password']
        db.session.commit()
        return admin, HTTPStatus.OK
    
@admin_namespace.route('/login')
class Login(Resource):
    @admin_namespace.doc('login_admin')
    @admin_namespace.expect(admin)
    def post(self):
        admin = Admin.query.filter_by(email=request.json['email']).first()
        if admin.password == request.json['password']:
            return admin, HTTPStatus.OK
        else:
            return "Wrong password", HTTPStatus.BAD_REQUEST
        
@admin_namespace.route('/logout')
class Logout(Resource):
    @admin_namespace.doc('logout_admin')
    @admin_namespace.expect(admin)
    def post(self):
        return "Logged out", HTTPStatus.OK
    
