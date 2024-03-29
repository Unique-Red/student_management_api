from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
api = Api(
    version='1.0',
    title='Student Management System',
    description='A simple Student Management System API'
)