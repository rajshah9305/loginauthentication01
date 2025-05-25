import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'

    # Google OAuth Configuration
    # IMPORTANT: Replace these with your actual credentials from Google Cloud Platform
    # Store them securely, preferably in environment variables.
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
    # Ensure this redirect URI is registered in your Google Cloud Console credentials
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", 'http://localhost:5001/api/auth/google/callback')

    # GitHub OAuth Configuration
    # IMPORTANT: Replace these with your actual credentials from your GitHub OAuth App
    # Store them securely, preferably in environment variables.
    GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "YOUR_GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "YOUR_GITHUB_CLIENT_SECRET")
    # Ensure this redirect URI is registered in your GitHub OAuth App settings
    # The port should match your Flask app's running port (e.g., 5001 if that's what you use)
    GITHUB_REDIRECT_URI = os.environ.get("GITHUB_REDIRECT_URI", 'http://localhost:5001/api/auth/github/callback')
