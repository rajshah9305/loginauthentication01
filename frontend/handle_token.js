document.addEventListener('DOMContentLoaded', () => {
    const messageElement = document.getElementById('message'); // From handle_token.html
    const processingMessageElement = document.querySelector('.processing-container p'); // The "Processing..." text

    const displayStatusMessage = (message, type) => {
        if (!messageElement) return;
        messageElement.textContent = message || '';
        messageElement.classList.remove('message-success', 'message-error', 'message-loading', 'message-active');

        if (message && type) {
            messageElement.classList.add(`message-${type}`);
            messageElement.classList.add('message-active'); // Make it visible
            messageElement.style.display = 'flex'; // Ensure it's displayed if hidden by default
        } else {
            messageElement.style.display = 'none'; // Hide if no message
        }
        // Hide the initial "Processing..." message when we show a specific status
        if (processingMessageElement && message) {
            processingMessageElement.style.display = 'none';
        }
    };

    const redirectToSignInWithError = (errorMessage) => {
        // Redirect to signin.html with error message as a query parameter
        // The error message will be picked up by signin.js
        window.location.href = `signin.html?error=${encodeURIComponent(errorMessage)}`;
    };

    const processToken = () => {
        displayStatusMessage('Processing your authentication...', 'loading'); // Initial loading message

        let token = null;
        let error = null;
        let errorMessageForSignIn = 'An unknown authentication error occurred.'; // Default error

        // Try to get token from URL hash (#token=...)
        if (window.location.hash && window.location.hash.startsWith('#token=')) {
            token = window.location.hash.substring(7); // Length of '#token='
        }
        // If not in hash, try to get from URL query parameter (?token=...)
        else {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('token')) {
                token = urlParams.get('token');
            } else if (urlParams.has('error')) { // Check if backend redirected with an error
                error = urlParams.get('error'); // This error is already URL encoded by backend
            }
        }

        if (error) {
            console.error('OAuth Error from URL:', error);
            let decodedError = '';
            try {
                // Attempt to decode if it's base64url encoded (as done in backend for errors)
                decodedError = atob(error.replace(/-/g, '+').replace(/_/g, '/'));
            } catch (e) {
                // If not base64, assume it's plain text (or URI encoded)
                decodedError = decodeURIComponent(error);
            }
            errorMessageForSignIn = `Authentication failed: ${decodedError}`;
            displayStatusMessage(errorMessageForSignIn, 'error');
            setTimeout(() => redirectToSignInWithError(errorMessageForSignIn), 3000); // Give time to see message
            return;
        }

        if (token) {
            // Basic validation: JWTs have three parts separated by dots.
            if (token.split('.').length === 3) {
                localStorage.setItem('accessToken', token);
                displayStatusMessage('Authentication successful! Redirecting to your dashboard...', 'success');

                // Clean the URL (remove token from address bar) and redirect
                if (window.history.replaceState) {
                    const cleanURLBase = window.location.protocol + "//" + window.location.host + window.location.pathname.replace('handle_token.html', '');
                    window.history.replaceState({ path: cleanURLBase + 'dashboard.html' }, '', cleanURLBase + 'handle_token.html'); // Clean URL first
                    window.location.href = 'dashboard.html'; // Then redirect
                } else {
                    // Fallback for older browsers
                    window.location.href = 'dashboard.html';
                }
            } else {
                console.error('Invalid token format received.');
                errorMessageForSignIn = 'Received an invalid authentication token. Please try signing in again.';
                displayStatusMessage(errorMessageForSignIn, 'error');
                setTimeout(() => redirectToSignInWithError(errorMessageForSignIn), 3000);
            }
        } else {
            console.error('Token not found in URL after OAuth process.');
            errorMessageForSignIn = 'Authentication token not found after the sign-in process. Please try again.';
            displayStatusMessage(errorMessageForSignIn, 'error');
            setTimeout(() => redirectToSignInWithError(errorMessageForSignIn), 3000);
        }
    };

    // Give a brief moment for the page to render before processing,
    // so user might see "Processing..."
    setTimeout(processToken, 100);
});
