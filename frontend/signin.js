document.addEventListener('DOMContentLoaded', () => {
    const signInForm = document.getElementById('signInForm');
    const googleSignInBtn = document.getElementById('googleSignInBtn');
    const githubSignInBtn = document.getElementById('githubSignInBtn');
    const messageElement = document.getElementById('message');

    const displayMessage = (message, type) => {
        if (messageElement) {
            messageElement.textContent = message;
            messageElement.className = `message-placeholder message-${type}`; // e.g., message-success or message-error
        } else {
            console.warn("Message element not found for:", message);
        }
    };

    // Email/Password Sign-In
    if (signInForm) {
        signInForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                displayMessage('Email and password are required.', 'error');
                return;
            }

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('accessToken', data.access_token);
                    displayMessage('Sign-in successful! Redirecting...', 'success');
                    window.location.href = 'dashboard.html';
                } else {
                    displayMessage(data.message || `Sign-in failed: ${response.status}`, 'error');
                }
            } catch (error) {
                console.error('Sign-in error:', error);
                displayMessage('An error occurred during sign-in. Please try again.', 'error');
            }
        });
    }

    // Google Sign-In
    if (googleSignInBtn) {
        googleSignInBtn.addEventListener('click', () => {
            // The backend /api/auth/google will redirect to Google's OAuth page
            window.location.href = '/api/auth/google';
        });
    }

    // GitHub Sign-In
    if (githubSignInBtn) {
        githubSignInBtn.addEventListener('click', () => {
            // The backend /api/auth/github will redirect to GitHub's OAuth page
            window.location.href = '/api/auth/github';
        });
    }

    // Check for error messages from handle_token.js if redirected
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    if (error) {
        displayMessage(decodeURIComponent(error), 'error');
        // Clean the URL
        if (window.history.replaceState) {
            const cleanURL = window.location.pathname;
            window.history.replaceState({ path: cleanURL }, '', cleanURL);
        }
    }
});
