from flask import Flask
from .students.views import student_namespace
from .auth.views import auth_namespace
from .courses.views import course_namespace
from .admin.views import admin_namespace
from .models import Student, Course, CourseRegistered, Admin
from extensions import db, jwt, migrate, api
from .config.config import config_dict


def create_app(config=config_dict['dev']):
 
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    api.init_app(app)


    # api = Api(app,
    #     title='Student Management API',
    #     version='1.0',
    #     description='A simple student management API',
    #     authorizations={
    #         "apikey":{'type': 'apiKey',
    #         'in': 'header',
    #         'name': 'X-API-KEY',
    #         'description': 'API Key'}
    #     },
    #     security='apikey'
    # )


    api.add_namespace(student_namespace, path='/students')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(course_namespace, path='/course')


    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Student': Student, 'Course': Course, 'CourseRegistered': CourseRegistered, 'Admin': Admin}

    return app