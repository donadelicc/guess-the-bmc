document.addEventListener('DOMContentLoaded', function () {

    // Håndter brukerinnlogging
    document.getElementById('login-user-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = '/start_game';  // Send brukeren til spillet
        } else {
            alert(result.message);  // Viser feilmelding fra backend
        }
    });

    // Håndter gjestelogging
    document.getElementById('guest-user-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        
        const guestUsername = document.getElementById('guest-username').value;

        const response = await fetch('/guest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: guestUsername
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            window.location.href = '/start_game';  // Send gjesten til spillet
        } else {
            alert(result.message);  // Viser feilmelding fra backend
        }
    });

    // Håndter brukerregistrering
    document.getElementById('register-user-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        
        const newUsername = document.getElementById('new-username').value;
        const newPassword = document.getElementById('new-password').value;

        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: newUsername,
                password: newPassword
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert('Registrering vellykket! Du kan nå logge inn.');
        } else {
            alert(result.message);  // Viser feilmelding fra backend
        }
    });
});
