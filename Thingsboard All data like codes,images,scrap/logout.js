// logout.js

let inactivityTimeout;

function startInactivityTimer() {
    inactivityTimeout = setTimeout(logout, 5 * 60 * 1000); // 5 minutes in milliseconds
}

function resetInactivityTimer() {
    clearTimeout(inactivityTimeout);
    startInactivityTimer();
}

function logout() {
    // Perform any existing logout or cleanup actions
    // ...

    // Call the ThingsBoard logout API endpoint
    // Adjust the URL and headers based on ThingsBoard API documentation
    $.ajax({
        url: 'https://app.controlytics.ai:443/api/auth/login', // Adjust the URL
        type: 'POST',
        headers: {
            'X-Authorization': 'Bearer ' + authToken // Include your authentication token
        },
        success: function (response) {
            console.log('ThingsBoard Logout Successful:', response);
            // Redirect to the login page or perform other actions as needed
            window.location.href = 'login.html'; // Adjust the URL as needed
        },
        error: function (error) {
            console.error('ThingsBoard Logout Failed:', error);
            // Redirect to the login page or perform other actions as needed
            window.location.href = 'login.html'; // Adjust the URL as needed
        }
    });
}

// Event listeners for user activity
document.addEventListener('mousemove', resetInactivityTimer);
document.addEventListener('keydown', resetInactivityTimer);

// Start the inactivity timer when the page loads
startInactivityTimer();
