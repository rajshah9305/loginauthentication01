document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logoutButton');
    const userInfoDiv = document.getElementById('userInfo');
    const userIdSpan = document.getElementById('userId');
    const userEmailSpan = document.getElementById('userEmail');
    // A message element can be added to dashboard.html if specific messages are needed here
    // const messageElement = document.getElementById('dashboardMessage');

    const redirectToSignIn = (message) => {
        let url = 'signin.html';
        if (message) {
            url += `?message=${encodeURIComponent(message)}`; // Or use 'error' if it's always an error
        }
        window.location.href = url;
    };

    // Check for token on page load
    const token = localStorage.getItem('accessToken');

    if (!token) {
        redirectToSignIn('Your session has expired or you are not logged in. Please sign in.');
        return; // Stop further execution
    }

    // Attempt to parse the token (assuming it's a JWT)
    try {
        const payloadBase64 = token.split('.')[1];
        if (!payloadBase64) {
            throw new Error("Invalid token format: Missing payload.");
        }
        const decodedPayload = JSON.parse(atob(payloadBase64));

        if (decodedPayload && decodedPayload.exp && decodedPayload.exp * 1000 < Date.now()) {
            localStorage.removeItem('accessToken');
            redirectToSignIn('Your session has expired. Please sign in again.');
            return;
        }

        // Display user info if available in token
        if (userInfoDiv && userIdSpan && userEmailSpan) {
            if (decodedPayload.user_id && decodedPayload.email) {
                userIdSpan.textContent = decodedPayload.user_id;
                userEmailSpan.textContent = decodedPayload.email;
                userInfoDiv.style.display = 'block';
            } else {
                console.warn("User ID or Email not found in token payload.");
                userInfoDiv.style.display = 'none';
            }
        }
    } catch (error) {
        console.error("Error decoding token or token is invalid:", error);
        localStorage.removeItem('accessToken');
        redirectToSignIn('Invalid session token. Please sign in again.');
        return;
    }

    // Logout Button Handler
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            // Optionally, display a "Logged out" message on the sign-in page
            // For now, just redirect. signin.js can check for a 'message' query param.
            redirectToSignIn('You have been logged out successfully.');
        });
    } else {
        console.warn("Logout button not found on the page.");
    }
});
