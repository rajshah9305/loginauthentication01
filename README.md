# User Authentication System

## Overview
This project's primary purpose is to provide a robust and easy-to-integrate system for user authentication in web applications. It offers a foundational template that includes email/password registration and login, along with social login capabilities via Google and GitHub. Its key benefit is helping developers kickstart their projects with essential authentication features already built-in, saving time and effort.

This project provides a template for user authentication with sign-in, sign-up, and social login options (Google & GitHub).

It includes a Python Flask backend and a simple HTML, CSS, and JavaScript frontend.

## Prerequisites
Before you begin, ensure you have the following installed or set up:

*   **Python:** Version 3.7 or higher. `pip` (Python package installer) and `venv` (for creating virtual environments) are typically included with Python installations.
*   **Database (Optional but Recommended):**
    *   The application can create and use a local SQLite database by default upon startup (`backend/app.py` contains logic for this), which is convenient for quick testing.
    *   For more robust development or a production-like environment, setting up a dedicated database server like PostgreSQL is recommended. The file `database/schema.sql` is provided to help initialize the schema for a PostgreSQL database.
*   **OAuth Credentials:**
    *   To enable the Google and GitHub social login functionalities, you will need to create your own OAuth 2.0 applications on the Google Cloud Platform and GitHub Developer settings, respectively.
    *   Detailed instructions on how to obtain these credentials can be found in the "[Configuration](#configuration)" section under "[Obtaining OAuth Credentials](#obtaining-oauth-credentials)".
*   **Git (Optional):**
    *   While not strictly necessary to run the project if you've downloaded the code as a ZIP file, Git is highly recommended for version control, managing changes, and collaborating.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Running the Project](#running-the-project)
  - [1. Backend Setup](#1-backend-setup)
  - [2. Frontend Setup](#2-frontend-setup)
- [API Endpoints (Backend)](#api-endpoints-backend)
- [Testing](#testing)
  - [Backend Unit Tests](#backend-unit-tests)
  - [Manual End-to-End Testing](#manual-end-to-end-testing)
- [Configuration](#configuration)
  - [Obtaining OAuth Credentials](#obtaining-oauth-credentials)

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
│   ├── `handle_token.html`     # Processes OAuth tokens
│   ├── `style.css`
│   ├── `signin.js`
│   ├── `signup.js`
│   ├── `dashboard.js`
│   └── `handle_token.js`
├── backend/                  # Flask application for API and authentication logic
│   ├── `app.py`                # Main Flask application
│   ├── `config.py`             # Configuration (DB URI, OAuth keys)
│   ├── `requirements.txt`      # Python dependencies
│   └── ... (other potential modules)
├── database/                 # Database related files
│   └── `schema.sql`            # SQL schema for the users table
└── `README.md`                 # This file
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
  Make sure your virtual environment is activated before running this command.
  ```bash
  pip install -r requirements.txt
  ```
- **Configure `backend/config.py`**:
    - Open `backend/config.py`.
    - **`SQLALCHEMY_DATABASE_URI`**: This is critical. For quick local development, you can use SQLite. For example: `SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/dev.db'`. This will create a `dev.db` file inside an `instance` folder at the root of the project (you might need to create the `instance` folder manually if it doesn't exist). For other databases like PostgreSQL, use the appropriate connection string (e.g., `postgresql://user:password@host:port/database_name`).
    - **OAuth Credentials**: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`, and `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `GITHUB_REDIRECT_URI` are essential for social logins. Replace placeholder values with your actual credentials. Ensure the `*_REDIRECT_URI` values match your OAuth provider settings and point to your backend's callback paths (e.g., `http://localhost:5001/api/auth/google/callback`).
    - **`SECRET_KEY`**: Set a strong, unique secret key for session security and JWT token encryption.
    - **`FRONTEND_BASE_URL`**: The `backend/app.py` uses this configuration value to redirect users back to the frontend after OAuth authentication. Ensure it matches the URL where your frontend is served. The default is `'http://localhost:5000'`. If your frontend runs on a different port or domain, update this in `config.py` or by setting it as an environment variable. For example, before running the backend:
      ```bash
      export FRONTEND_BASE_URL='http://localhost:3000' # For Linux/macOS
      # set FRONTEND_BASE_URL=http://localhost:3000    # For Windows
      python app.py
      ```
- **Initialize the Database**:
    - **Automatic Setup (Recommended for Development):** If `SQLALCHEMY_DATABASE_URI` in `backend/config.py` is set (e.g., to a SQLite path like `sqlite:///../instance/dev.db`), the Flask application (`backend/app.py`) will automatically create the database file (if it doesn't exist) and the necessary tables when you first run `python app.py`. This is due to the `db.create_all()` command within the application context.
    - **Manual Setup (e.g., for PostgreSQL):** The `database/schema.sql` file contains the SQL commands to create the `users` table. This is primarily useful if you want to set up a specific database system like PostgreSQL manually or if you are not using SQLAlchemy's `db.create_all()` feature. You would typically execute this script against your configured database using a database management tool.
- **Run the Flask development server**:
  ```bash
  python app.py
  ```
  The backend will typically run on `http://localhost:5001`.

### 2. Frontend Setup
- No build step is required for this simple HTML, CSS, and JavaScript setup.
- **Serving the Frontend (Crucial for API Calls & OAuth):**
    - While you can open `.html` files directly in the browser (`File -> Open File...`), this method **will not work** for features that rely on API calls to the backend (like registration, login) or for OAuth redirects.
    - For the frontend to correctly communicate with the backend API and for OAuth redirects to function seamlessly, you **must serve the `frontend` directory using a simple HTTP server.**
    - Ensure the backend server is running and accessible (typically at `http://localhost:5001`).
    - The JavaScript files in `frontend/` (e.g., `signin.js`, `signup.js`) make API calls to relative paths like `/api/register`. A local HTTP server ensures these requests are correctly routed to your backend.
    - **Example using Python's built-in HTTP server:**
      Navigate to the `frontend` directory:
      ```bash
      cd frontend
      ```
      Then start the server (e.g., on port 5000):
      ```bash
      python -m http.server 5000
      ```
      Access your frontend at `http://localhost:5000/signin.html` or `http://localhost:5000/signup.html`.
    - **Port Configuration:** If you serve the frontend on a port different from the default `5000` (e.g., `3000`), make sure to update the `FRONTEND_BASE_URL` in your backend configuration accordingly. As detailed in the "[1. Backend Setup](#1-backend-setup)" section, you can set this as an environment variable before running the backend:
      ```bash
      export FRONTEND_BASE_URL='http://localhost:3000' # For Linux/macOS
      # set FRONTEND_BASE_URL=http://localhost:3000    # For Windows
      # Then run your backend: python backend/app.py
      ```
- **OAuth Redirect URL (`handle_token.html`):**
    - After a successful OAuth authentication (e.g., with Google or GitHub), the backend needs to redirect the user back to a frontend page. This page is `frontend/handle_token.html`.
    - The backend constructs this redirect URL using the `FRONTEND_BASE_URL` variable from its configuration (see `backend/config.py` and "[1. Backend Setup](#1-backend-setup)"). The full redirect URL will be `FRONTEND_BASE_URL/frontend/handle_token.html`.
    - By default, `FRONTEND_BASE_URL` is `http://localhost:5000`, so the backend redirects to `http://localhost:5000/frontend/handle_token.html`.
    - If you serve your frontend on a different URL (e.g., `http://localhost:3000`), you must set the `FRONTEND_BASE_URL` environment variable for the backend to match, as explained above and in the backend setup instructions. This ensures the OAuth flow completes correctly by redirecting the user to the correct frontend page.

## API Endpoints (Backend)
- **POST `/api/register`**: User registration.
- **POST `/api/login`**: User login, returns JWT.
- **GET `/api/auth/google`**: Initiates Google OAuth flow.
- **GET `/api/auth/google/callback`**: Handles Google OAuth callback.
- **GET `/api/auth/github`**: Initiates GitHub OAuth flow.
- **GET `/api/auth/github/callback`**: Handles GitHub OAuth callback.

(Further details on request/response formats can be added here if needed.)

## Testing

The project includes backend unit tests and guidelines for manual end-to-end testing.

### Backend Unit Tests

These tests cover individual components of the backend application to ensure functionality and catch regressions.

#### Running Unit Tests
1.  **Navigate to the root directory of the project.**
2.  **Activate the backend virtual environment** (as described in "[1. Backend Setup](#1-backend-setup)"):
    ```bash
    # Example for macOS/Linux (from project root):
    # source backend/venv/bin/activate
    # Example for Windows (from project root):
    # backend\venv\Scripts\activate
    ```
3.  **Run all unit tests** using Python's `unittest` module from the project root directory:
    ```bash
    python -m unittest discover backend/tests
    ```
    This command discovers and runs all test files located in the `backend/tests` directory.
    To run a specific test file (e.g., `test_auth.py`):
    ```bash
    python -m unittest backend.tests.test_auth
    ```

#### Test Environment for Unit Tests
- Unit tests are configured to use an **in-memory SQLite database** (`sqlite:///:memory:`), as specified in `backend/tests/test_config.py`.
- This setup ensures that tests run in a clean, isolated environment and **do not interfere with your development database** or require any external database setup for testing.
- External OAuth API calls are mocked using `unittest.mock` to provide consistent and predictable behavior during tests, avoiding actual network requests to Google or GitHub.

### Manual End-to-End Testing

Manual End-to-End (E2E) tests involve testing the complete application flow, from the user interface to the backend and database.

**Prerequisites for Manual E2E Testing:**
-   The **backend server must be running** (see "[1. Backend Setup](#1-backend-setup)").
-   The **frontend must be served via an HTTP server** and accessible in your browser (see "[2. Frontend Setup](#2-frontend-setup)").

These tests simulate real user scenarios:

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
