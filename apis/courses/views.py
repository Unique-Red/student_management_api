from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Student, Courses
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

courses_namespace = Namespace('Courses', description='Courses related operations')

course = courses_namespace.model('Course', {
    'id': fields.Integer(required=True, description='The course identifier'),
    "course code": fields.String(required=True, description='The course code'),
    "course title": fields.String(required=True, description='The course title'),
    "course unit": fields.Integer(required=True, description='The course unit'),
    "lecturer": fields.String(required=True, description='The course lecturer')
})

courses_registered = courses_namespace.model('Courses Registered', {
    "course_id": fields.Integer(required=True, description='The course identifier'),
    "student_id": fields.Integer(required=True, description='The student identifier')
})

@courses_namespace.route('/register')
class Register(Resource):
    @courses_namespace.doc('register_course')
    @courses_namespace.expect(course)
    @courses_namespace.marshal_with(course, code=201)
    def post(self):
        data = request.get_json()
        new_course = Courses(
            course_code=data['course code'],
            course_title=data['course title'],
            course_unit=data['course unit'],
            lecturer=data['lecturer'],
        )
        db.session.add(new_course)
        db.session.commit()

        return new_course, HTTPStatus.CREATED
    
    @courses_namespace.doc('get_all_courses')
    @courses_namespace.marshal_with(course, code=200)
    def get(self):
        courses = Courses.query.all()
        return courses, HTTPStatus.OK
    
@courses_namespace.route('/register/<int:course_id>')
class Register(Resource):
    @courses_namespace.doc('get_course_by_id')
    @courses_namespace.marshal_with(course, code=200)
    def get(self, course_id):
        course = Courses.query.filter_by(id=course_id).first()
        return course, HTTPStatus.OK
    
    @courses_namespace.doc('delete_course_by_id')
    @courses_namespace.marshal_with(course, code=200)
    def delete(self, course_id):
        course = Courses.query.filter_by(id=course_id).first()
        db.session.delete(course)
        db.session.commit()

        return course, HTTPStatus.OK
