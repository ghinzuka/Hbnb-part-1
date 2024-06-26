import unittest
import os
import sys

# Ajouter le répertoire parent de src au chemin de recherche de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import create_app, db
from src.models import User
from flask_jwt_extended import create_access_token

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class="src.config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(email="testuser@example.com", first_name="Test", last_name="User", password="password")
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post('/users/login', json={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_protected_route(self):
        # Get a valid token
        access_token = create_access_token(identity={'email': self.user.email, 'is_admin': self.user.is_admin})

        # Access protected route
        response = self.client.get('/places/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged_in_as', data)
        self.assertEqual(data['logged_in_as']['email'], self.user.email)

    def test_invalid_login(self):
        response = self.client.post('/users/login', json={
            'email': 'wronguser@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', response.get_json())

    def test_protected_route_without_token(self):
        response = self.client.get('/places/protected')
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', response.get_json())

if __name__ == '__main__':
    unittest.main()
