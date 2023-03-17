from flask import request
from flask_restx import Resource, Namespace, fields
from extensions import db
from ..models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('Auth', description='Authentication related operations')

register_user = auth_namespace.model('Register', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password'),
    'email': fields.String(required=True, description='The user email'),
    'admin': fields.Boolean(required=True, description='The user admin status')
})

user = auth_namespace.model('User', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password'),
    'email': fields.String(required=True, description='The user email'),
    'admin': fields.Boolean(required=True, description='The user admin status')
})

login_user = auth_namespace.model('Login', {
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password')
})


@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.doc('register_user')
    @auth_namespace.expect(user)
    @auth_namespace.marshal_with(user, code=201)
    def post(self):
        data = request.get_json()
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            password = generate_password_hash(data['password'], method='sha256'),
            admin=data['admin']
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.doc('login_user')
    @auth_namespace.expect(login_user)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        if check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }, HTTPStatus.OK
        else:
            return {'message': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED
        
@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK