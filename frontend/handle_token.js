document.addEventListener('DOMContentLoaded', () => {
    const messageElement = document.getElementById('message'); // Assuming your handle_token.html has a message div

    const displayErrorOnSignInPage = (message) => {
        // Redirect to signin.html with error message as a query parameter
        window.location.href = `signin.html?error=${encodeURIComponent(message)}`;
    };

    const processToken = () => {
        let token = null;
        let error = null;

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
                error = urlParams.get('error');
            }
        }

        if (error) {
            console.error('OAuth Error:', error);
            if (messageElement) messageElement.textContent = decodeURIComponent(error);
            // Delay redirect to allow user to see message, or redirect immediately to signin with error
            setTimeout(() => displayErrorOnSignInPage(decodeURIComponent(error)), 2000);
            return;
        }

        if (token) {
            localStorage.setItem('accessToken', token);
            // Clean the URL (remove token from address bar) and redirect
            if (window.history.replaceState) {
                // For hash: remove the hash
                // For query param: construct URL without query params or just redirect
                const cleanURL = window.location.protocol + "//" + window.location.host + window.location.pathname.replace('handle_token.html', 'dashboard.html');
                window.history.replaceState({ path: cleanURL }, '', cleanURL.replace('dashboard.html', 'handle_token.html')); // temporary clean
                window.location.href = 'dashboard.html';
            } else {
                // Fallback for older browsers
                window.location.href = 'dashboard.html';
            }
        } else {
            console.error('Token not found in URL.');
            if (messageElement) messageElement.textContent = 'Authentication token not found. Redirecting to sign in.';
            setTimeout(() => displayErrorOnSignInPage('Authentication token not found after OAuth process.'), 2000);
        }
    };

    processToken();
});
