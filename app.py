from flask import Flask
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

@api.route('/students')
class StudentList(Resource):
    @jwt_required
    def get(self):
        students = Student.query.all()
        return {'students': [{'name': student.name, 'age': student.age} for student in students]}

    def post(self):
        data = api.payload
        student = Student(name=data['name'], age=data['age'])
        db.session.add(student)
        db.session.commit()
        return {'id': student.id, 'name': student.name, 'age': student.age}

@api.route('/students/<int:id>')
class StudentDetail(Resource):
    @jwt_required
    def get(self, id):
        student = Student.query.get_or_404(id)
        return {'id': student.id, 'name': student.name, 'age': student.age}

    def put(self, id):
        data = api.payload
        student = Student.query.get_or_404(id)
        student.name = data['name']
        student.age = data['age']
        db.session.commit()
        return {'id': student.id, 'name': student.name, 'age': student.age}

    def delete(self, id):
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted successfully'}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# @jwt.user_loader_callback
# def user_loader_callback(identity):
#     return User.query.get(identity)

if __name__ == '__main__':
    app.run(debug=True)