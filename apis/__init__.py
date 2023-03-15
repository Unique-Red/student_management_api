from flask import Flask
from flask_restx import Api
from .students.views import student_namespace
from .auth.views import auth_namespace
from .models.users import User
from .models.users import Student
from extensions import db
from .config.config import config_dict
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
 
    app = Flask(__name__)

    app.config.from_object(config)
    
    jwt = JWTManager(app)
    db.init_app(app)

    api = Api(app,
        title='Student Management API',
        version='1.0',
        description='A simple student management API',
        authorizations={
            "apikey":{'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY',
            'description': 'API Key'}
        },
        security='apikey'
    )


    api.add_namespace(student_namespace)
    api.add_namespace(auth_namespace, path='/auth')


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Student': Student, 'User': User}

    return app