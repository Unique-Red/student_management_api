from flask import Flask
from flask_restx import Api
from .students.students import student_namespace
from .models.students import Student
from .utils import db
from .config.config import config_dict
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
 
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['RESTX_VALIDATE'] = True
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False
    
    jwt = JWTManager(app)
    db.init_app(app)

    api = Api(
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


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Student': Student}

    return app