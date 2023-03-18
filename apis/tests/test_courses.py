import unittest
from ..models import Courses
from http import HTTPStatus
from ..config.config import config_dict
from .. import create_app
from extensions import db

class CourseTestCase(unittest.TestCase):
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

    def test_register_course(self):
        response = self.client.post('/courses/register', json={
            'course name': 'python',
            'course code': 'pyt',
            'course description': 'python course',
            'course instructor': 'james'
        })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json['course name'], 'python')
        self.assertEqual(response.json['course code'], 'pyt')
        self.assertEqual(response.json['course description'], 'python course')
        self.assertEqual(response.json['course instructor'], 'james')

    def test_get_all_courses(self):
        course = Courses(
            course_name='python',
            course_code='pyt',
            course_description='python course',
            course_instructor='james'
        )
        db.session.add(course)
        db.session.commit()

        response = self.client.get('/courses')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['course name'], 'python')
        self.assertEqual(response.json[0]['course code'], 'pyt')
        self.assertEqual(response.json[0]['course description'], 'python course')
        self.assertEqual(response.json[0]['course instructor'], 'james')

    def test_get_course_by_id(self):
        course = Courses(
            course_name='python',
            course_code='pyt',
            course_description='python course',
            course_instructor='james'
        )
        db.session.add(course)
        db.session.commit()

        response = self.client.get(f'/courses/{course.id}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json['course name'], 'python')
        self.assertEqual(response.json['course code'], 'pyt')
        self.assertEqual(response.json['course description'], 'python course')
        self.assertEqual(response.json['course instructor'], 'james')

    def test_update_course(self):
        course = Courses(
            course_name='python',
            course_code='pyt',
            course_description='python course',
            course_instructor='james'
        )
        db.session.add(course)
        db.session.commit()
        