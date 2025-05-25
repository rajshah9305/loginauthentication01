document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const messageElement = document.getElementById('message');
    const submitButton = signupForm ? signupForm.querySelector('button[type="submit"]') : null;

    const displayMessage = (message, type) => {
        if (!messageElement) return;
        messageElement.textContent = message || ''; // Clear message if null or empty
        // Base class is message-placeholder. Add specific type class for styling.
        // Remove old type classes before adding new one.
        messageElement.classList.remove('message-success', 'message-error', 'message-loading', 'message-active');

        if (message && type) {
            messageElement.classList.add(`message-${type}`);
            messageElement.classList.add('message-active'); // To trigger visibility/animation
        }
        // If no message or type, it remains hidden or clears.
    };

    const setLoadingState = (isLoading) => {
        if (!submitButton) return;
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'Signing Up...'; // Or add a spinner icon
            displayMessage('Processing your registration...', 'loading');
        } else {
            submitButton.disabled = false;
            submitButton.textContent = 'Sign Up';
            // displayMessage(null); // Clear loading message - handled by next success/error message
        }
    };

    if (signupForm && submitButton) {
        signupForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            displayMessage(null); // Clear previous messages

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

            setLoadingState(true);

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

                const data = await response.json(); // Attempt to parse JSON regardless of response.ok

                if (response.ok) { // Status 200-299
                    displayMessage(data.message || 'Registration successful! Redirecting to sign in...', 'success');
                    setTimeout(() => {
                        window.location.href = 'signin.html';
                    }, 2000);
                } else {
                    // Display error message from backend, or a generic one
                    displayMessage(data.message || `Registration failed: ${response.statusText || response.status}`, 'error');
                }
            } catch (error) {
                console.error('Registration error:', error);
                displayMessage('An error occurred during registration. This could be a network issue or the server might be down. Please try again.', 'error');
            } finally {
                setLoadingState(false);
            }
        });
    } else {
        if (!signupForm) console.error("Signup form not found on the page.");
        if (!submitButton) console.error("Submit button not found on the signup form.");
    }
});
