import os
from backend.config import Config # Assuming your main config is in backend/config.py

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    SECRET_KEY = 'test_secret_key' # Consistent secret key for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for forms if you use Flask-WTF (not used in this project but good practice)

    # Override OAuth credentials for testing - these won't be used if you mock API calls
    GOOGLE_CLIENT_ID = "test_google_client_id"
    GOOGLE_CLIENT_SECRET = "test_google_client_secret"
    GOOGLE_REDIRECT_URI = "http://localhost:5001/api/auth/google/callback/test" # Test specific redirect

    GITHUB_CLIENT_ID = "test_github_client_id"
    GITHUB_CLIENT_SECRET = "test_github_client_secret"
    GITHUB_REDIRECT_URI = "http://localhost:5001/api/auth/github/callback/test" # Test specific redirect

    # Suppress logging to keep test output clean, or configure for specific test logging
    LOGGING_LEVEL = 'ERROR'

    # For development with OAUTHLIB_INSECURE_TRANSPORT
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
