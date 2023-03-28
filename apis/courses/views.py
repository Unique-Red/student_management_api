from flask_restx import Resource, fields, Namespace, abort
from extensions import db
from ..models import Student, Courses, CourseRegistered
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

courses_namespace = Namespace('Courses', description='Courses related operations')

course = courses_namespace.model('Course', {
    'id': fields.Integer(required=True, description='The course identifier'),
    "course_code": fields.String(required=True, description='The course code'),
    "course_title": fields.String(required=True, description='The course title'),
    "course_unit": fields.Integer(required=True, description='The course unit'),
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
            course_code=data['course_code'],
            course_title=data['course_title'],
            course_unit=data['course_unit'],
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
    # @courses_namespace.marshal_with(course, code=200)
    
    def delete(self, course_id):
        course = Courses.query.filter_by(id=course_id).first()
        if not course:
            abort(404, message="Course not found")
        db.session.delete(course)
        db.session.commit()

        return {"message": "course deleted"}, HTTPStatus.OK
    
    @courses_namespace.doc('update_course_by_id')
    @courses_namespace.expect(course)
    @courses_namespace.marshal_with(course, code=200)
    
    def put(self, course_id):
        course = Courses.query.filter_by(id=course_id).first()
        data = request.get_json()
        if not course:
            abort(404, message="Course not found")
        course.course_code = data['course_code']
        course.course_title = data['course_title']
        course.course_unit = data['course_unit']
        course.lecturer = data['lecturer']
        db.session.commit()

        return course, HTTPStatus.OK
    
@courses_namespace.route('/register/<int:course_id>/students')
class Register(Resource):
    @courses_namespace.doc('register_course_for_student')
    @courses_namespace.expect(courses_registered)
    @courses_namespace.marshal_with(courses_registered, code=201)
    def post(self, course_id):
        data = request.get_json()
        new_course_registered = CourseRegistered(
            course_id=course_id,
            student_id=data['student_id']
        )
        db.session.add(new_course_registered)
        db.session.commit()

        return new_course_registered, HTTPStatus.CREATED
    
    @courses_namespace.doc('get_all_courses_registered')
    @courses_namespace.marshal_with(courses_registered, code=200)
    def get(self, course_id):
        courses_registered = CourseRegistered.query.filter_by(course_id=course_id).all()

        return courses_registered, HTTPStatus.OK
    
    @courses_namespace.doc('delete_course_registered_by_id')
    @courses_namespace.marshal_with(courses_registered, code=200)
    
    def delete(self, course_id):
        courses_registered = CourseRegistered.query.filter_by(course_id=course_id).all()
        for course_registered in courses_registered:
            db.session.delete(course_registered)
            db.session.commit()

        return courses_registered, HTTPStatus.OK
