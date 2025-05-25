import unittest
import json
from unittest.mock import patch, MagicMock # For mocking external API calls
from backend.app import app, db, User # Assuming app, db, User are in backend.app
from backend.tests.test_config import TestConfig

class OAuthTestCase(unittest.TestCase):
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

    @patch('backend.app.GoogleFlow.from_client_config') # Path to Flow in your app.py
    @patch('backend.app.id_token.verify_oauth2_token') # Path to id_token in your app.py
    def test_google_oauth_new_user(self, mock_verify_id_token, mock_google_flow_from_config):
        """Test Google OAuth callback with a new user."""
        # Mock Google Flow
        mock_flow_instance = MagicMock()
        mock_flow_instance.credentials = MagicMock()
        mock_flow_instance.credentials.id_token = "dummy_google_id_token"
        mock_google_flow_from_config.return_value = mock_flow_instance

        # Mock id_token verification
        mock_verify_id_token.return_value = {
            'iss': 'accounts.google.com',
            'sub': 'test_google_id_123',
            'email': 'new_google_user@example.com',
            'email_verified': True,
            'name': 'Google User'
        }

        # Simulate the callback from Google
        response = self.client.get('/api/auth/google/callback?code=dummy_code&state=dummy_state')
        
        self.assertEqual(response.status_code, 302) # Expecting a redirect
        self.assertIn('frontend/handle_token.html#token=', response.location)

        with app.app_context():
            user = User.query.filter_by(email='new_google_user@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.google_id, 'test_google_id_123')
            self.assertIsNone(user.password_hash) # Social login users might not have a password

        # Check token in redirect URL
        token = response.location.split('#token=')[1]
        import jwt
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        self.assertEqual(decoded_token['email'], 'new_google_user@example.com')
        self.assertEqual(decoded_token['user_id'], user.id)


    @patch('backend.app.GoogleFlow.from_client_config')
    @patch('backend.app.id_token.verify_oauth2_token')
    def test_google_oauth_existing_user_link_account(self, mock_verify_id_token, mock_google_flow_from_config):
        """Test Google OAuth linking to an existing user by email."""
        # Create an existing user
        with app.app_context():
            existing_user = User(email='existing_google_user@example.com', username='existingUser')
            existing_user.set_password('password123') # Existing user might have a password
            db.session.add(existing_user)
            db.session.commit()
            user_id_before_link = existing_user.id

        mock_flow_instance = MagicMock()
        mock_flow_instance.credentials = MagicMock()
        mock_flow_instance.credentials.id_token = "dummy_google_id_token_link"
        mock_google_flow_from_config.return_value = mock_flow_instance

        mock_verify_id_token.return_value = {
            'sub': 'test_google_id_456',
            'email': 'existing_google_user@example.com', # Same email as existing user
            'email_verified': True
        }

        response = self.client.get('/api/auth/google/callback?code=dummy_auth_code')
        self.assertEqual(response.status_code, 302)
        self.assertIn('frontend/handle_token.html#token=', response.location)

        with app.app_context():
            linked_user = User.query.filter_by(email='existing_google_user@example.com').first()
            self.assertIsNotNone(linked_user)
            self.assertEqual(linked_user.google_id, 'test_google_id_456')
            self.assertEqual(linked_user.id, user_id_before_link) # Should be the same user
            self.assertTrue(linked_user.check_password('password123')) # Original password should still work


    @patch('requests.post') # Mock the requests.post call for token exchange
    @patch('requests.get')  # Mock the requests.get call for user info
    def test_github_oauth_new_user(self, mock_requests_get, mock_requests_post):
        """Test GitHub OAuth callback with a new user."""
        # Mock GitHub token exchange
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {'access_token': 'dummy_github_token'}
        mock_requests_post.return_value = mock_token_response

        # Mock GitHub user info fetch
        mock_user_info_response = MagicMock()
        mock_user_info_response.status_code = 200
        mock_user_info_response.json.return_value = {
            'id': 78910,
            'email': 'new_github_user@example.com',
            'login': 'newgithubuser'
        }
        # If your code also fetches /user/emails
        mock_emails_response = MagicMock()
        mock_emails_response.status_code = 200
        mock_emails_response.json.return_value = [
            {'email': 'new_github_user@example.com', 'primary': True, 'verified': True}
        ]
        # Configure mock_requests_get to return different values based on URL
        def side_effect_get(url, headers):
            if 'api.github.com/user/emails' in url:
                return mock_emails_response
            elif 'api.github.com/user' in url:
                return mock_user_info_response
            return MagicMock(status_code=404) # Default for unexpected calls
        mock_requests_get.side_effect = side_effect_get


        response = self.client.get('/api/auth/github/callback?code=dummy_github_code')
        self.assertEqual(response.status_code, 302) # Expecting redirect
        self.assertIn('frontend/handle_token.html#token=', response.location)

        with app.app_context():
            user = User.query.filter_by(email='new_github_user@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.github_id, '78910')
            self.assertEqual(user.username, 'newgithubuser')

        token = response.location.split('#token=')[1]
        import jwt
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        self.assertEqual(decoded_token['email'], 'new_github_user@example.com')

if __name__ == '__main__':
    unittest.main()
