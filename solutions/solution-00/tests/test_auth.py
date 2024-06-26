import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src import create_app, db
from src.models import User
from src import bcrypt

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the test environment...")
        self.app = create_app(config_class="src.config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        print("Creating a test user...")
        self.user = User(email="testuser@example.com", first_name="Test", last_name="User", password="password")
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        print("\nTearing down the test environment...")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        print("\nTesting login with valid credentials...")
        response = self.client.post('/users/login', json={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        data = response.get_json()
        print(f"Response: {response.status_code}, Data: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_protected_route(self):
        print("\nTesting access to protected route with valid token...")
        access_token = create_access_token(identity={'email': self.user.email, 'is_admin': self.user.is_admin})
        print(f"Generated access token: {access_token}")
        
        response = self.client.get('/places/protected', headers={
            'Authorization': f'Bearer {access_token}'
        })
        data = response.get_json()
        print(f"Response: {response.status_code}, Data: {data}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged_in_as', data)
        self.assertEqual(data['logged_in_as']['email'], self.user.email)

    def test_invalid_login(self):
        print("\nTesting login with invalid credentials...")
        response = self.client.post('/users/login', json={
            'email': 'wronguser@example.com',
            'password': 'password'
        })
        data = response.get_json()
        print(f"Response: {response.status_code}, Data: {data}")
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', data)

    def test_protected_route_without_token(self):
        print("\nTesting access to protected route without token...")
        response = self.client.get('/places/protected')
        data = response.get_json()
        print(f"Response: {response.status_code}, Data: {data}")
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', data)

if __name__ == '__main__':
    unittest.main()
