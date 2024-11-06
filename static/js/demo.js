// Event listener for form submission
document.querySelector('.formauth').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent page reload

    const phoneNumber = document.getElementById('phone').value;
    const messageDiv = document.getElementById('message');  // Select message div

    // Clear previous messages
    messageDiv.textContent = '';

    const phonePattern = /^\+?[0-9]{1,3}[0-9]{9,14}$/;  // Allow 1 to 3 digits for country code followed by 9 to 14 digits

    if (!phonePattern.test(phoneNumber)) {
        messageDiv.textContent = 'Veuillez entrer un numéro de téléphone valide.';
        messageDiv.className = 'message error';
        return;  // Stop the function if validation fails
    }

    // Display loading message before API call
    messageDiv.textContent = 'Loading...';  // You can customize this message
    messageDiv.className = 'message loading';  // Optional loading class

    // Make the API request to trigger the call via your backend
    fetch('/submit-number', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phoneNumber: phoneNumber }),
    })
    .then(response => {
        // Check if response is OK (status 200)
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Une erreur est survenue.');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Debugging log
        messageDiv.textContent = 'Appel et SMS en cours d\'envoi...';
        messageDiv.className = 'message success';  // Add success class
    })
    .catch(error => {
        console.error('Erreur :', error);
        messageDiv.textContent = error.message;  // Display the error message from the response
        messageDiv.className = 'message error';  // Add error class
    });
});

