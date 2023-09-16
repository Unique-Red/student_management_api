from flask_restx import Resource, fields, Namespace, abort
from extensions import db
from ..models import Student, Course, CourseRegistered
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

authorizations = {
    "jsonwebtoken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

course_namespace = Namespace('Course', authorizations=authorizations, description='Course related operations')

course_model = course_namespace.model('Course', {
    'id': fields.Integer(readOnly=True, description='The course unique identifier'),
    'course_code': fields.String(required=True, description='Course code'),
    'course_title': fields.String(required=True, description='Course title'),
    'course_unit': fields.Integer(required=True, description='Course unit'),
    'lecturer': fields.String(required=True, description='Lecturer')
})

course_input_model = course_namespace.model('Course Input', {
    'course_code': fields.String(required=True, description='Course code'),
    'course_title': fields.String(required=True, description='Course title'),
    'course_unit': fields.Integer(required=True, description='Course unit'),
    'lecturer': fields.String(required=True, description='Lecturer')
})

@course_namespace.route('/courses')
class CourseListAPI(Resource):
    method_decorators = [jwt_required()]

    @course_namespace.doc(security='jsonwebtoken')

    @course_namespace.marshal_list_with(course_model)
    def get(self):
        courses = Course.query.all()
        return courses, HTTPStatus.OK
    
    @course_namespace.expect(course_input_model)
    @course_namespace.marshal_with(course_model)
    def post(self):
        course = Course(course_code=course_namespace.payload['course_code'], course_title=course_namespace.payload['course_title'], course_unit=course_namespace.payload['course_unit'], lecturer=course_namespace.payload['lecturer'])
        if Course.query.filter_by(course_code=course_namespace.payload['course_code']).first():
            return {'message': 'Course already exists'}, HTTPStatus.BAD_REQUEST
        if Course.query.filter_by(course_title=course_namespace.payload['course_title']).first():
            return {'message': 'Course already exists'}, HTTPStatus.BAD_REQUEST
        
        db.session.add(course)
        db.session.commit()
        return course, HTTPStatus.CREATED
    
@course_namespace.route('/courses/<int:id>')
class CourseAPI(Resource):
    @course_namespace.marshal_with(course_model)
    def get(self, id):
        course = Course.query.get_or_404(id)
        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_input_model)
    @course_namespace.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get_or_404(id)
        course.course_code = course_namespace.payload['course_code']
        course.course_title = course_namespace.payload['course_title']
        course.course_unit = course_namespace.payload['course_unit']
        course.lecturer = course_namespace.payload['lecturer']
        db.session.commit()
        return course, HTTPStatus.OK
    
    @course_namespace.marshal_with(course_model)
    def delete(self, id):
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return '', HTTPStatus.NO_CONTENT
