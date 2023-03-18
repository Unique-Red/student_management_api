import unittest
from ..models import Students
from http import HTTPStatus
from ..config.config import config_dict
from .. import create_app
from extensions import db

class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_dict['test'])
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_student(self):
        response = self.client.post('/students/register', json={
            'first name': 'student',
            'last name': 'student',
            'email': 'demostudent@gmail.com'
        })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json['first name'], 'student')
        self.assertEqual(response.json['last name'], 'student')
        self.assertEqual(response.json['email'], 'demostudent@gmail.com')

    def test_get_all_students(self):
        student = Students(
            first_name='student',
            last_name='student',
            email='demostudent@gmail.com')
        db.session.add(student)
        db.session.commit()
        