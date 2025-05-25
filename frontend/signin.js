document.addEventListener('DOMContentLoaded', () => {
    const signInForm = document.getElementById('signInForm');
    const googleSignInBtn = document.getElementById('googleSignInBtn');
    const githubSignInBtn = document.getElementById('githubSignInBtn');
    const messageElement = document.getElementById('message');
    const submitButton = signInForm ? signInForm.querySelector('button[type="submit"]') : null;

    const displayMessage = (message, type) => {
        if (!messageElement) return;
        messageElement.textContent = message || '';
        messageElement.classList.remove('message-success', 'message-error', 'message-loading', 'message-active');

        if (message && type) {
            messageElement.classList.add(`message-${type}`);
            messageElement.classList.add('message-active');
        }
    };

    const setLoadingState = (isLoading, buttonText = 'Sign In') => {
        if (!submitButton) return;
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'Signing In...'; // Or use a spinner
            displayMessage('Processing your sign-in...', 'loading');
        } else {
            submitButton.disabled = false;
            submitButton.textContent = buttonText;
            // Loading message is cleared by the subsequent success/error message
        }
    };

    // Email/Password Sign-In
    if (signInForm && submitButton) {
        signInForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            displayMessage(null); // Clear previous messages

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                displayMessage('Email and password are required.', 'error');
                return;
            }

            setLoadingState(true);

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json(); // Attempt to parse JSON for all responses

                if (response.ok) {
                    localStorage.setItem('accessToken', data.access_token);
                    displayMessage('Sign-in successful! Redirecting...', 'success');
                    setTimeout(() => { // Give time for message to be seen
                        window.location.href = 'dashboard.html';
                    }, 1500);
                } else {
                    displayMessage(data.message || `Sign-in failed: ${response.statusText || response.status}`, 'error');
                }
            } catch (error) {
                console.error('Sign-in error:', error);
                displayMessage('An error occurred during sign-in. This could be a network issue or the server might be down. Please try again.', 'error');
            } finally {
                setLoadingState(false);
            }
        });
    } else {
        if (!signInForm) console.error("Sign In form not found on the page.");
        if (!submitButton) console.error("Submit button not found on the Sign In form.");
    }

    // Google Sign-In
    if (googleSignInBtn) {
        googleSignInBtn.addEventListener('click', () => {
            displayMessage('Redirecting to Google for sign-in...', 'loading');
            // The backend /api/auth/google will redirect to Google's OAuth page
            window.location.href = '/api/auth/google';
        });
    }

    // GitHub Sign-In
    if (githubSignInBtn) {
        githubSignInBtn.addEventListener('click', () => {
            displayMessage('Redirecting to GitHub for sign-in...', 'loading');
            // The backend /api/auth/github will redirect to GitHub's OAuth page
            window.location.href = '/api/auth/github';
        });
    }

    // Check for error messages from handle_token.js or backend OAuth callback error redirects
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');
    const success = urlParams.get('success'); // For potential success messages via redirect

    if (error) {
        let decodedError = '';
        try {
            // Attempt to decode if it's base64url encoded (as done in backend for errors)
            // Replace base64url specific chars then decode
            decodedError = atob(error.replace(/-/g, '+').replace(/_/g, '/'));
        } catch (e) {
            // If not base64, assume it's plain text (or URI encoded)
            decodedError = decodeURIComponent(error);
        }
        displayMessage(decodedError, 'error');
        // Clean the URL: remove error query parameter
        if (window.history.replaceState) {
            const cleanURL = new URL(window.location.href);
            cleanURL.searchParams.delete('error');
            if (success) cleanURL.searchParams.delete('success'); // Also remove success if present
            window.history.replaceState({ path: cleanURL.href }, '', cleanURL.href);
        }
    } else if (success) {
        displayMessage(decodeURIComponent(success), 'success');
        // Clean the URL: remove success query parameter
        if (window.history.replaceState) {
            const cleanURL = new URL(window.location.href);
            cleanURL.searchParams.delete('success');
            window.history.replaceState({ path: cleanURL.href }, '', cleanURL.href);
        }
    }
});
