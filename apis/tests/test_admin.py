import unittest
from ..models import Admin
from http import HTTPStatus
from ..config.config import config_dict
from .. import create_app
from extensions import db

class UserTestCase(unittest.TestCase):
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

    def test_register_admin(self):
        response = self.client.post('/admin/register', json={
            'first name': 'admin',
            'last name': 'admin',
            'email': 'demoadmin@gmail.com',
            'password': 'admin'
        })

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json['first name'], 'admin')
        self.assertEqual(response.json['last name'], 'admin')
        self.assertEqual(response.json['email'], 'deomadmin@gmail.com')

    def test_get_all_admins(self):
        admin = Admin(
            first_name='admin',
            last_name='admin',
            email='deomadmin@gmail.com')
        db.session.add(admin)
        db.session.commit()



