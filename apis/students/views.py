from flask_restx import Resource, fields, Namespace
from extensions import db
from ..models import Student

student_namespace = Namespace('Students', description='Student related operations')


student = student_namespace.model('Student', {
    'id': fields.Integer(required=True, description='The student identifier'),
    'first_name': fields.String(required=True, description="The student's first name"),
    'last_name': fields.String(required=True, description="The student's last name"),
    'email': fields.String(required=True, description='The student email'),
    "matric_number": fields.String(required=True, description='The student matric number'),
    'gpa': fields.Float(required=True, description='The student grade')
})


@student_namespace.route('/')
class StudentList(Resource):
    @student_namespace.doc("list_students")
    @student_namespace.marshal_list_with(student)
    def get(self):
        STUDENTS = Student.query.all()
        return STUDENTS
    

@student_namespace.route('/<int:id>')
@student_namespace.param('id', 'The student identifier')
@student_namespace.response(404, 'Student not found')
class Student(Resource):
    @student_namespace.doc('get_student')
    @student_namespace.marshal_with(student)
    def get(self, id):
        STUDENTS = Student.query.all()
        for student in STUDENTS:
            if student['id'] == id:
                return student
        student_namespace.abort(404, f"Student {id} doesn't exist")

    @student_namespace.doc('create_student')
    @student_namespace.expect(student)
    @student_namespace.marshal_with(student, code=201)
    def post(self, id):
        student = student_namespace.payload
        student['id'] = id
        STUDENTS = Student.query.all()
        STUDENTS.append(student)
        db.session.commit()
        return student, 201

    @student_namespace.doc('update_student')
    @student_namespace.expect(student)
    @student_namespace.marshal_with(student)
    def put(self, id):
        STUDENTS = Student.query.all()
        for student in STUDENTS:
            if student['id'] == id:
                student.update(student_namespace.payload)
                return student
        student_namespace.abort(404, f"Student {id} doesn't exist")

    @student_namespace.doc('delete_student')
    @student_namespace.marshal_with(student)
    def delete(self, id):
        STUDENTS = Student.query.all()
        for i, student in enumerate(STUDENTS):
            if student['id'] == id:
                del STUDENTS[i]
                return '', 204
        student_namespace.abort(404, f"Student {id} doesn't exist")