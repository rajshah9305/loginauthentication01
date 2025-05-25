# User Authentication System

This project provides a template for user authentication with sign-in, sign-up, and social login options (Google & GitHub).

It includes a Python Flask backend and a simple HTML, CSS, and JavaScript frontend.

## Features
- Email/Password Registration
- Email/Password Sign-In
- Google OAuth 2.0 Sign-In
- GitHub OAuth 2.0 Sign-In
- JWT-based authentication for API access
- Basic database schema for users
- Frontend pages for Sign Up, Sign In, and a simple Dashboard.

## Project Structure
```
/
├── frontend/                 # HTML, CSS, JS for the user interface
│   ├── signin.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── handle_token.html     # Processes OAuth tokens
│   ├── style.css
│   ├── signin.js
│   ├── signup.js
│   ├── dashboard.js
│   └── handle_token.js
├── backend/                  # Flask application for API and authentication logic
│   ├── app.py                # Main Flask application
│   ├── config.py             # Configuration (DB URI, OAuth keys)
│   ├── requirements.txt      # Python dependencies
│   └── ... (other potential modules)
├── database/                 # Database related files
│   └── schema.sql            # SQL schema for the users table
└── README.md                 # This file
```

## Running the Project

### 1. Backend Setup
- Requires Python 3.7+.
- Navigate to the `backend` directory:
  ```bash
  cd backend
  ```
- Create a virtual environment:
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment:
  - On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```
  - On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- **Configure `backend/config.py`**:
    - Open `backend/config.py`.
    - Update `SQLALCHEMY_DATABASE_URI` with your actual database connection string (e.g., `postgresql://user:password@host:port/database_name`).
    - **Crucially, update OAuth credentials**:
        - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`
        - `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_REDIRECT_URI`
    - Replace placeholder values like `"YOUR_GOOGLE_CLIENT_ID"` with your actual credentials obtained from Google Cloud Platform and GitHub OAuth Apps.
    - Ensure the `*_REDIRECT_URI` values match what you've configured in your OAuth provider settings and generally point to your backend's callback paths (e.g., `http://localhost:5001/api/auth/google/callback`).
    - Set a strong `SECRET_KEY` for JWT and session security.
- **Initialize the Database**:
    - The Flask application in `backend/app.py` currently uses `db.create_all()` within an application context when run directly (`if __name__ == '__main__':`). This will create the necessary tables based on the SQLAlchemy models if they don't already exist.
    - For the first run, ensure your database server is running and accessible with the credentials provided in `config.py`.
    - Alternatively, you can use the `database/schema.sql` to manually set up the `users` table in your PostgreSQL database if you prefer not to use `db.create_all()` or are using a different database system initially.
- **Run the Flask development server**:
  ```bash
  python app.py
  ```
  The backend will typically run on `http://localhost:5001`.

### 2. Frontend Setup
- No build step is required for this simple HTML, CSS, and JavaScript setup.
- Open the `.html` files from the `frontend` directory directly in your browser using the `File -> Open File...` menu:
    - For example, open `frontend/signup.html` or `frontend/signin.html`.
- **Important**: For the frontend to correctly communicate with the backend (especially for OAuth redirects and API calls):
    - Ensure the backend server is running and accessible (usually at `http://localhost:5001`).
    - The frontend JavaScript files (`signin.js`, `signup.js`, `handle_token.js`) make API calls to relative paths like `/api/register`. For these to work correctly when opening HTML files directly, it's often best to serve the `frontend` directory through a simple HTTP server. Many tools can do this, for example, using Python:
      ```bash
      # Navigate to the root of the project, then:
      cd frontend
      python -m http.server 5000
      ```
      Then access the frontend at `http://localhost:5000/signin.html` or `http://localhost:5000/signup.html`. This ensures that requests from the frontend to the backend (e.g., `http://localhost:5001/api/...`) are handled correctly by the browser without cross-origin issues if both servers are on `localhost` but different ports.
    - Note: The OAuth redirect URIs in `backend/config.py` and in your OAuth provider settings should ultimately point to the backend's callback endpoint (e.g., `http://localhost:5001/api/auth/google/callback`). The backend then redirects to `frontend/handle_token.html` with the application token. The hardcoded frontend URL in `backend/app.py` for this redirect is `http://localhost:5000/frontend/handle_token.html`. If you serve your frontend on a different port, this will need adjustment in `backend/app.py`.

## API Endpoints (Backend)
- **POST /api/register**: User registration.
- **POST /api/login**: User login, returns JWT.
- **GET /api/auth/google**: Initiates Google OAuth flow.
- **GET /api/auth/google/callback**: Handles Google OAuth callback.
- **GET /api/auth/github**: Initiates GitHub OAuth flow.
- **GET /api/auth/github/callback**: Handles GitHub OAuth callback.

(Further details on request/response formats can be added here if needed.)

## Testing

The backend includes a suite of unit tests to ensure functionality and catch regressions.

### Running Tests
1.  **Ensure you are in the root directory of the project.**
2.  **Activate your virtual environment** (if you created one for the backend, as described in "Backend Setup").
    ```bash
    # Example for macOS/Linux:
    # source backend/venv/bin/activate
    # Example for Windows:
    # backend\venv\Scripts\activate
    ```
3.  **Run the tests** using Python's `unittest` module:
    ```bash
    python -m unittest discover backend/tests
    ```
    Or, to run a specific test file (e.g., `test_auth.py`):
    ```bash
    python -m unittest backend.tests.test_auth
    ```

### Test Environment
- Tests are configured to run against an **in-memory SQLite database** (`sqlite:///:memory:`), as defined in `backend/tests/test_config.py`. This ensures that tests do not interfere with your development database and run in a clean, isolated environment.
- External OAuth API calls are mocked using `unittest.mock` to provide consistent and predictable behavior during tests without actual network requests.

### Manual End-to-End Testing
These tests require the backend server to be running and the frontend to be accessible in a browser (preferably served via a simple HTTP server as described in "Frontend Setup").

**1. Email/Password Authentication:**
   - **Sign Up:**
     - Navigate to the Sign Up page (`frontend/signup.html`).
     - Attempt to sign up with an empty email/password (expect client-side validation errors).
     - Attempt to sign up with an invalid email format (e.g., "test@test") (expect validation errors).
     - Attempt to sign up with a short password (e.g., less than 8 characters) (expect validation errors).
     - Successfully sign up with a new valid email (e.g., `testuser1@example.com`) and password (e.g., `password123`). Verify redirection to the Sign In page or a success message.
     - Attempt to sign up again with the *same* email (e.g., `testuser1@example.com`) (expect an error message like "Email already registered").
   - **Sign In:**
     - Navigate to the Sign In page (`frontend/signin.html`).
     - Attempt to sign in with a non-existent email (e.g., `nosuchuser@example.com`) (expect an error message like "Invalid email or password").
     - Attempt to sign in with an existing email (e.g., `testuser1@example.com`) but the wrong password (expect an error message like "Invalid email or password").
     - Successfully sign in with the newly created user (`testuser1@example.com` and `password123`).
     - Verify redirection to the dashboard (`frontend/dashboard.html`).
     - Verify that user information (e.g., email, user ID) is displayed on the dashboard (if implemented) or that the access token is stored in `localStorage`.
   - **Logout:**
     - From the dashboard, click the "Logout" button.
     - Verify redirection to the Sign In page.
     - Verify that the access token is cleared from `localStorage`.
     - Attempt to navigate directly to `dashboard.html` (expect redirection back to Sign In).

**2. Google OAuth 2.0:**
   - *Prerequisite: Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correctly configured in `backend/config.py` with valid credentials from Google Cloud Platform, and the redirect URI is correctly set up.*
   - On the Sign In page, click the "Sign in with Google" button.
   - You should be redirected to Google's authentication page.
   - Authenticate with a valid Google account.
   - Grant access if prompted by Google.
   - Verify successful login/registration and redirection to the application's dashboard (`frontend/dashboard.html`).
   - (Optional) Check your database to see if a new user has been created with a `google_id` and the email from your Google account, or if an existing user with that email has been linked.
   - Logout from the application.
   - (Optional) Attempt to sign in with a *different* Google account to test multiple social logins.

**3. GitHub OAuth 2.0:**
   - *Prerequisite: Ensure `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are correctly configured in `backend/config.py` with valid credentials from a GitHub OAuth App, and the redirect URI is correctly set up.*
   - On the Sign In page, click the "Sign in with GitHub" button.
   - You should be redirected to GitHub's authentication page.
   - Authenticate with a valid GitHub account.
   - Authorize the application if prompted by GitHub.
   - Verify successful login/registration and redirection to the application's dashboard (`frontend/dashboard.html`).
   - (Optional) Check your database to see if a new user has been created with a `github_id` and the email from your GitHub account (if public, or primary verified email), or if an existing user has been linked.
   - Logout from the application.

**4. Error Handling (Backend Down):**
   - Stop the backend Flask server.
   - Attempt to sign up or sign in from the frontend.
   - Verify that user-friendly error messages (e.g., "Network error, please try again", "Could not connect to server") are displayed on the frontend, rather than the browser's default connection error page.

## Configuration

### Obtaining OAuth Credentials
To use Google and GitHub social logins, you need to obtain API keys (Client ID and Client Secret) from their respective developer platforms and configure them in `backend/config.py`.

**1. Google OAuth 2.0 Credentials:**
   - Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).
   - **Create a new project** or select an existing one.
   - Navigate to **"APIs & Services" -> "Credentials"** from the left-hand menu.
   - Click **"+ CREATE CREDENTIALS"** and select **"OAuth 2.0 Client ID."**
   - If prompted, configure the "OAuth consent screen" first:
     - User Type: External (or Internal if applicable).
     - Provide an App name, User support email, and Developer contact information.
     - Scopes: Add `email`, `profile`, `openid`.
     - Add test users if your app is in testing mode.
   - For "Application type," select **"Web application."**
   - **Authorized JavaScript origins:**
     - Add your frontend's origin. For local development, this is typically `http://localhost:5000` (if you serve the frontend on port 5000).
   - **Authorized redirect URIs:**
     - This is where Google sends the response back to your backend. Add `http://localhost:5001/api/auth/google/callback` (assuming your backend runs on port 5001).
   - Click **"CREATE."**
   - Copy the **"Client ID"** and **"Client Secret"** and paste them into the `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` fields in `backend/config.py`. Also, ensure `GOOGLE_REDIRECT_URI` in `config.py` matches the one you registered.

**2. GitHub OAuth 2.0 Credentials:**
   - Go to your [GitHub Developer settings](https://github.com/settings/developers).
   - Click on **"OAuth Apps"** on the left, then click **"New OAuth App."**
   - **Application name:** Choose a name (e.g., "My Auth Test App").
   - **Homepage URL:** Your application's main URL. For local development, use `http://localhost:5000` (or your frontend's URL).
   - **Authorization callback URL:** This is where GitHub sends the response back to your backend. Use `http://localhost:5001/api/auth/github/callback` (assuming your backend runs on port 5001).
   - Click **"Register application."**
   - On the next page, you will see the **"Client ID."**
   - Click **"Generate a new client secret"** to get your client secret.
   - Copy the **"Client ID"** and the newly generated **"Client Secret"** and paste them into the `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` fields in `backend/config.py`. Ensure `GITHUB_REDIRECT_URI` in `config.py` matches the callback URL.

**Important:**
- Keep your Client Secrets confidential. Do not commit them directly to public repositories if this were a production project (use environment variables or a secret management system).
- The OAuth flows will not work correctly without valid credentials and matching redirect URIs configured both in `backend/config.py` and on the respective OAuth provider platforms.
