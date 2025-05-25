# User Authentication System

A complete user authentication template with email/password registration and social login integration (Google & GitHub).

## 🚀 Features

- **Email/Password Authentication** - Standard registration and login
- **Social Login** - Google OAuth 2.0 and GitHub OAuth 2.0 integration
- **JWT Authentication** - Secure API access with JSON Web Tokens
- **Modern Frontend** - Clean HTML, CSS, and JavaScript interface
- **Flask Backend** - Python-based REST API
- **Database Ready** - User management with SQL schema

## 📁 Project Structure

```
/
├── frontend/                 # User interface (HTML, CSS, JS)
│   ├── signin.html          # Login page
│   ├── signup.html          # Registration page
│   ├── dashboard.html       # User dashboard
│   └── ...
├── backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── tests/              # Unit tests
├── database/               # Database schema
│   └── schema.sql         # User table structure
└── README.md
```

## 🛠️ Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
python -m http.server 5000
```
Open your browser to `http://localhost:5000`

### 3. Configuration
- Update `backend/config.py` with your database connection
- Add your Google and GitHub OAuth credentials
- Set a secure JWT secret key

## 🔧 API Endpoints

- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/auth/google` - Google OAuth flow
- `GET /api/auth/github` - GitHub OAuth flow

## 🧪 Testing

Run the test suite:
```bash
python -m unittest discover backend/tests
```

## 📋 Requirements

- Python 3.7+
- Flask and dependencies (see requirements.txt)
- PostgreSQL or SQLite database
- Google Cloud Platform account (for Google OAuth)
- GitHub Developer account (for GitHub OAuth)

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- OAuth 2.0 social login integration
- Input validation and sanitization
- CORS protection

## 📄 License

This project is licensed under the MIT License - see the details below:

```
MIT License

Copyright (c) 2025 User Authentication System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Note:** This is a development template. For production use, ensure proper environment variable management, HTTPS configuration, and additional security measures.
