from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Student, Courses, CourseRegistered
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

student_namespace = Namespace('Students', description='Student related operations')


student = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The student identifier'),
    'first_name': fields.String(required=True, description="The student's first name"),
    'last_name': fields.String(required=True, description="The student's last name"),
    'email': fields.String(required=True, description='The student email'),
    "matric_number": fields.String(required=True, description='The student matric number'),
    'gpa': fields.Float(required=True, description='The student grade')
})

gpa = student_namespace.model('GPA', {
    "student_id": fields.Integer(required=True, description='The student identifier'),
    "course_code": fields.String(required=True, description='The course code'),
    'gpa': fields.Float(required=True, description='The student grade')
})


@student_namespace.route('/register')
class Register(Resource):
    @student_namespace.doc('register_student')
    @student_namespace.expect(student)
    @student_namespace.marshal_with(student, code=201)
    @jwt_required
    def post(self):
        student = Student.query.filter_by(email=request.json['email']).first()
        if student:
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST 

        data = student_namespace.payload()
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            matric_number=data['matric_number'],
            gpa=data['gpa']
        )
        db.session.add(new_student)
        db.session.commit()

        return new_student, HTTPStatus.CREATED

    @student_namespace.doc('get_all_students')
    @student_namespace.marshal_with(student, code=200)
    def get(self):
        students = Student.query.all()
        return students, HTTPStatus.OK
    
@student_namespace.route('/<int:student_id>')
class Retrieve(Resource):
    @student_namespace.doc('get_student_by_id')
    @student_namespace.marshal_with(student, code=200)
    def get(self, student_id):
        student = Student.query.filter_by(id=student_id).first()
        return student, HTTPStatus.OK
    
    @student_namespace.doc('delete_student_by_id')
    @student_namespace.marshal_with(student, code=200)
    def delete(self, student_id):
        student = Student.query.filter_by(id=student_id).first()
        db.session.delete(student)
        db.session.commit()
        return student, HTTPStatus.OK
    
    