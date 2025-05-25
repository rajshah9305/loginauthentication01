import os
import re
import datetime
import jwt
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from google_auth_oauthlib.flow import Flow as GoogleFlow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests # For fetching userinfo if needed, though id_token is preferred

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Ensure os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' is set for development if not using HTTPS for callback
# This is typically set when running the Flask app for local development.
# For production, HTTPS is required.
if app.debug:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# --- Database Model ---
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    github_id = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.email}>'

# --- Utility Functions ---
def is_valid_email(email):
    """Basic email validation."""
    if not email:
        return False
    # Basic regex for email validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

# --- API Endpoints ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Request body must be JSON'}), 400

    email = data.get('email')
    password = data.get('password')
    username = data.get('username') # Optional

    # Input Validation
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format'}), 400
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    try:
        # Check if email or username already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already registered'}), 409
        if username and User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already taken'}), 409

        new_user = User(email=email, username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        # Log the error for debugging: print(e) or use a proper logger
        return jsonify({'message': 'An error occurred during registration. Please try again.'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Request body must be JSON'}), 400

    email = data.get('email')
    password = data.get('password')

    # Input Validation
    if not email:
        return jsonify({'message': 'Email is required'}), 400
    if not is_valid_email(email): # Assuming you have this utility function from register
        return jsonify({'message': 'Invalid email format'}), 400
    if not password:
        return jsonify({'message': 'Password is required'}), 400

    try:
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Password is correct, generate JWT
            token_payload = {
                'user_id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Token expires in 24 hours
            }
            access_token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({'access_token': access_token}), 200
        else:
            # Invalid credentials
            return jsonify({'message': 'Invalid email or password'}), 401

    except Exception as e:
        # Log the error for debugging: print(e) or use a proper logger
        return jsonify({'message': 'An error occurred during login. Please try again.'}), 500


# --- Google OAuth Endpoints ---
def get_google_flow():
    client_config = {
        "web": {
            "client_id": app.config['GOOGLE_CLIENT_ID'],
            "client_secret": app.config['GOOGLE_CLIENT_SECRET'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [app.config['GOOGLE_REDIRECT_URI']],
            "javascript_origins": ["http://localhost:5000", "http://localhost:5001"] # Adjust as needed
        }
    }
    scopes = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
    flow = GoogleFlow.from_client_config(
        client_config,
        scopes=scopes,
        redirect_uri=app.config['GOOGLE_REDIRECT_URI']
    )
    return flow

@app.route('/api/auth/google', methods=['GET'])
def auth_google():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # Store the state in session or a temporary store if you need to verify it later
    # For simplicity, we're not storing it here, but it's recommended for security.
    # session['oauth_state'] = state 
    return redirect(authorization_url)

@app.route('/api/auth/google/callback', methods=['GET'])
def auth_google_callback():
    flow = get_google_flow()
    code = request.args.get('code')

    if not code:
        return jsonify({'message': 'Authorization code not found.'}), 400

    try:
        # Exchange code for token
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Verify ID token and get user info
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            google_requests.Request(),
            app.config['GOOGLE_CLIENT_ID']
        )

        google_id = id_info.get('sub')
        email = id_info.get('email')
        # name = id_info.get('name') # Full name
        # first_name = id_info.get('given_name')
        # last_name = id_info.get('family_name')
        
        if not email:
            return jsonify({'message': 'Email not provided by Google.'}), 400

        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            # No user with this google_id, check by email
            user = User.query.filter_by(email=email).first()
            if not user:
                # New user: create one
                # Decide on username: use email prefix, or name if available, or prompt user later
                username_candidate = email.split('@')[0] # Simple username from email
                # check if username_candidate is already taken
                existing_username = User.query.filter_by(username=username_candidate).first()
                if existing_username:
                    username_candidate = f"{username_candidate}_{google_id[:6]}" # make it more unique

                user = User(
                    email=email,
                    google_id=google_id,
                    username=username_candidate # Or use 'name' if you prefer and handle uniqueness
                    # password_hash remains None for social logins initially
                )
                db.session.add(user)
            else:
                # Existing user by email, link Google ID
                user.google_id = google_id
            db.session.commit()
        
        # At this point, 'user' is the authenticated user (either found or created)
        # Generate your application's JWT for this user
        token_payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        app_access_token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

        # For SPAs, returning JSON is common.
        # You might redirect to a frontend URL with the token as a query parameter,
        # but that can expose the token in browser history.
        # A common pattern is for the frontend to open a popup for Google login,
        # and the callback sets the token in localStorage/sessionStorage of the parent window
        # or communicates back via window.postMessage.
        # Redirect to frontend with the token in the URL hash/fragment
        # The frontend (handle_token.html) will pick this up.
        frontend_redirect_url = f"{request.host_url.replace('http://', 'http://localhost:5000/').replace('0.0.0.0:5001', 'localhost:5000')}frontend/handle_token.html#token={app_access_token}"
        # A more robust way to determine frontend URL might be needed if not always localhost:5000
        # For example, use an environment variable for FRONTEND_BASE_URL
        if 'localhost:5001' in request.host_url or '0.0.0.0:5001' in request.host_url : # common dev server
             frontend_redirect_url = f"http://localhost:5000/frontend/handle_token.html#token={app_access_token}"


        return redirect(frontend_redirect_url)
        # Old: return jsonify({'access_token': app_access_token, 'user_id': user.id, 'email': user.email}), 200

    except ValueError as ve: # Catches specific id_token.verify_oauth2_token errors
        app.logger.error(f"Google ID token verification failed: {ve}")
        return jsonify({'message': f'Google authentication failed: {str(ve)}'}), 401
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error during Google OAuth callback: {e}")
        # Be careful not to expose too much error detail to the client
        error_message = 'An error occurred during Google authentication.'
        if app.debug:
            error_message = f'An error occurred during Google authentication: {str(e)}'
        
        frontend_error_redirect_url = f"http://localhost:5000/frontend/signin.html?error={jwt.utils.base64url_encode(error_message.encode()).decode()}"
        return redirect(frontend_error_redirect_url)
        # Old: return jsonify({'message': 'An error occurred during Google authentication.'}), 500


# --- GitHub OAuth Endpoints ---
@app.route('/api/auth/github', methods=['GET'])
def auth_github():
    # For simplicity, state is not implemented here, but it's recommended for CSRF protection.
    # You would typically generate a random string, store it in session, and verify it in the callback.
    # session['oauth_state_github'] = generated_state_string
    github_authorize_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={app.config['GITHUB_CLIENT_ID']}&"
        f"redirect_uri={app.config['GITHUB_REDIRECT_URI']}&"
        f"scope=user:email read:user" # user:email for private emails, read:user for profile
        # f"&state={generated_state_string}" # If using state
    )
    return redirect(github_authorize_url)

@app.route('/api/auth/github/callback', methods=['GET'])
def auth_github_callback():
    code = request.args.get('code')
    # state = request.args.get('state') # If using state, verify it here against session['oauth_state_github']

    if not code:
        return jsonify({'message': 'Authorization code not found.'}), 400

    try:
        # Exchange code for access token
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': app.config['GITHUB_CLIENT_ID'],
                'client_secret': app.config['GITHUB_CLIENT_SECRET'],
                'code': code,
                'redirect_uri': app.config['GITHUB_REDIRECT_URI']
            },
            headers={'Accept': 'application/json'}
        )
        token_response.raise_for_status() # Raise an exception for bad status codes
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if not access_token:
            error_description = token_json.get('error_description', 'GitHub token exchange failed.')
            return jsonify({'message': error_description}), 500

        # Fetch user info from GitHub API
        user_info_headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        user_info_response = requests.get('https://api.github.com/user', headers=user_info_headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        github_id = str(user_info.get('id')) # Ensure github_id is stored as string
        email = user_info.get('email')
        github_login = user_info.get('login') # GitHub username
        name = user_info.get('name') # User's full name (can be null)

        # If primary email is not public, fetch from /user/emails
        if not email:
            emails_response = requests.get('https://api.github.com/user/emails', headers=user_info_headers)
            emails_response.raise_for_status()
            emails_data = emails_response.json()
            
            if emails_data and isinstance(emails_data, list):
                primary_email_obj = next((e for e in emails_data if e.get('primary') and e.get('verified')), None)
                if primary_email_obj:
                    email = primary_email_obj['email']
                else: # Fallback to first verified email
                    verified_email_obj = next((e for e in emails_data if e.get('verified')), None)
                    if verified_email_obj:
                        email = verified_email_obj['email']
        
        if not email:
            # If still no email, this means the user has no public/primary verified email.
            # You might redirect them to a page to set an email or deny login.
            return jsonify({'message': 'Could not retrieve a verified email from GitHub. Please ensure you have a primary, verified email set on GitHub.'}), 400

        user = User.query.filter_by(github_id=github_id).first()

        if not user:
            user = User.query.filter_by(email=email).first()
            if not user:
                # New user: create one
                username_candidate = github_login or email.split('@')[0]
                # Ensure username uniqueness
                existing_username = User.query.filter_by(username=username_candidate).first()
                if existing_username:
                    username_candidate = f"{username_candidate}_{github_id[:6]}"

                user = User(
                    email=email,
                    github_id=github_id,
                    username=username_candidate,
                    # password_hash remains None for social logins
                )
                db.session.add(user)
            else:
                # Existing user by email, link GitHub ID
                user.github_id = github_id
            db.session.commit()

        # Generate application JWT
        token_payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        app_access_token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

        # Redirect to frontend with the token in the URL hash/fragment
        frontend_redirect_url = f"http://localhost:5000/frontend/handle_token.html#token={app_access_token}"
        return redirect(frontend_redirect_url)
        # Old: return jsonify({'access_token': app_access_token, 'user_id': user.id, 'email': user.email}), 200

    except requests.exceptions.RequestException as re:
        app.logger.error(f"GitHub OAuth request failed: {re}")
        return jsonify({'message': f'Communication error with GitHub: {str(re)}'}), 502 # Bad Gateway
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error during GitHub OAuth callback: {e}")
        error_message = 'An error occurred during GitHub authentication.'
        if app.debug:
            error_message = f'An error occurred during GitHub authentication: {str(e)}'

        frontend_error_redirect_url = f"http://localhost:5000/frontend/signin.html?error={jwt.utils.base64url_encode(error_message.encode()).decode()}"
        return redirect(frontend_error_redirect_url)
        # Old: return jsonify({'message': 'An error occurred during GitHub authentication.'}), 500


# --- Main Execution ---
if __name__ == '__main__':
    # Create tables if they don't exist
    # This is okay for development, but for production, migrations (e.g., Alembic) are better.
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
