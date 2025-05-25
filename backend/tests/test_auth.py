import unittest
import json
from backend.app import app, db, User # Assuming app, db, User are in backend.app
from backend.tests.test_config import TestConfig

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        app.config.from_object(TestConfig)
        self.client = app.test_client()

        # Propagate the exceptions to the test client
        app.testing = True
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down all initialized variables."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration_success(self):
        """Test user registration with valid data."""
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/register', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('user_id', data)
        
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')
            self.assertTrue(user.check_password('password123'))

    def test_user_registration_duplicate_email(self):
        """Test registration with a duplicate email."""
        # First registration
        payload1 = {'email': 'duplicate@example.com', 'password': 'password123'}
        self.client.post('/api/register', data=json.dumps(payload1), content_type='application/json')
        
        # Attempt second registration with same email
        payload2 = {'email': 'duplicate@example.com', 'password': 'password456'}
        response = self.client.post('/api/register', data=json.dumps(payload2), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('Email already registered', data['message'])

    def test_user_registration_invalid_payload(self):
        """Test registration with missing email or password."""
        # Missing password
        payload_no_pass = {'email': 'nopass@example.com'}
        response = self.client.post('/api/register', data=json.dumps(payload_no_pass), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Password is required', data['message'])

        # Missing email
        payload_no_email = {'password': 'password123'}
        response = self.client.post('/api/register', data=json.dumps(payload_no_email), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Email is required', data['message'])

    def test_password_hashing(self):
        """Test password hashing and checking directly."""
        user = User(email='hash@example.com')
        user.set_password('securepassword')
        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, 'securepassword')
        self.assertTrue(user.check_password('securepassword'))
        self.assertFalse(user.check_password('wrongpassword'))

    def test_user_login_success(self):
        """Test user login with correct credentials."""
        # Register user first
        reg_payload = {'email': 'login_success@example.com', 'password': 'password123', 'username': 'loginsuccess'}
        self.client.post('/api/register', data=json.dumps(reg_payload), content_type='application/json')
        
        login_payload = {'email': 'login_success@example.com', 'password': 'password123'}
        response = self.client.post('/api/login', data=json.dumps(login_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        
        # Test JWT generation and decoding (basic check)
        import jwt
        token = data['access_token']
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        self.assertEqual(decoded_token['email'], 'login_success@example.com')
        self.assertIn('user_id', decoded_token)

    def test_user_login_invalid_credentials(self):
        """Test user login with incorrect password or non-existent email."""
        # Register user first
        reg_payload = {'email': 'login_fail@example.com', 'password': 'password123'}
        self.client.post('/api/register', data=json.dumps(reg_payload), content_type='application/json')

        # Incorrect password
        login_payload_wrong_pass = {'email': 'login_fail@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/api/login', data=json.dumps(login_payload_wrong_pass), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Invalid email or password', data['message'])

        # Non-existent email
        login_payload_wrong_email = {'email': 'nosuchuser@example.com', 'password': 'password123'}
        response = self.client.post('/api/login', data=json.dumps(login_payload_wrong_email), content_type='application/json')
        self.assertEqual(response.status_code, 401) # Should also be 401 or a clear indication of failure
        data = json.loads(response.data)
        self.assertIn('Invalid email or password', data['message']) # Message could be generic for security

if __name__ == '__main__':
    unittest.main()
