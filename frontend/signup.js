document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const messageElement = document.getElementById('message');

    const displayMessage = (message, type) => {
        messageElement.textContent = message;
        messageElement.className = `message-${type}`; // e.g., message-success or message-error
    };

    if (signupForm) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            // --- Client-side Validation ---
            if (!email) {
                displayMessage('Email is required.', 'error');
                return;
            }
            // Basic email format validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                displayMessage('Please enter a valid email address.', 'error');
                return;
            }

            if (!password) {
                displayMessage('Password is required.', 'error');
                return;
            }
            if (password.length < 8) {
                displayMessage('Password must be at least 8 characters long.', 'error');
                return;
            }
            if (password !== confirmPassword) {
                displayMessage('Passwords do not match.', 'error');
                return;
            }

            const payload = {
                email: email,
                password: password
            };
            if (username) {
                payload.username = username;
            }

            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                if (response.ok) { // Status 200-299
                    displayMessage(data.message || 'Registration successful! Redirecting to sign in...', 'success');
                    // Optionally, redirect to sign-in page after a delay
                    setTimeout(() => {
                        window.location.href = 'signin.html';
                    }, 2000);
                } else {
                    // Display error message from backend
                    displayMessage(data.message || `Registration failed with status: ${response.status}`, 'error');
                }
            } catch (error) {
                console.error('Registration error:', error);
                displayMessage('An error occurred during registration. Please check your network connection and try again.', 'error');
            }
        });
    } else {
        console.error("Signup form not found on the page.");
    }
});
