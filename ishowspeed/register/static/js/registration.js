document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const inputs = document.querySelectorAll('.form-input');
    const sendCodeBtn = document.getElementById('sendCodeBtn');

    function validatePassword(password, username) {
        // Check if password contains username or parts of it
        if (username && password.toLowerCase().includes(username.toLowerCase())) {
            return { valid: false, message: "Password cannot contain your username" };
        }
        
        // Check minimum length
        if (password.length < 9) {
            return { valid: false, message: "Password must be at least 9 characters" };
        }
        
        // Check character types
        const hasUpper = /[A-Z]/.test(password);
        const hasLower = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
        
        const typeCount = [hasUpper, hasLower, hasNumber, hasSpecial].filter(Boolean).length;
        
        if (typeCount < 3) {
            return { 
                valid: false, 
                message: "Password must include at least 3 of: uppercase, lowercase, numbers, or special characters" 
            };
        }
        
        return { valid: true, message: "" };
    }

    function validateForm() {
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm-password');

        const usernameValid = username.value.length >= 7;
        const emailValid = email.value.includes('@') && email.value.includes('.');
        const passwordValidation = validatePassword(password.value, username.value);
        const passwordValid = passwordValidation.valid;
        const passwordsMatch = password.value === confirmPassword.value && passwordValid;

        sendCodeBtn.disabled = !(usernameValid && emailValid && passwordValid && passwordsMatch);
    }

    inputs.forEach(input => {
        input.addEventListener('input', () => {
            const errorElement = input.nextElementSibling.nextElementSibling;
            
            if (input.value.length > 0) {
                if (input.id === 'username') {
                    const isValid = input.value.length >= 7;
                    input.classList.toggle('valid', isValid);
                    input.classList.toggle('invalid', !isValid);
                    errorElement.textContent = isValid ? '' : 'Username must be at least 7 characters';
                } else if (input.id === 'email') {
                    const isValid = input.value.includes('@') && input.value.includes('.');
                    input.classList.toggle('valid', isValid);
                    input.classList.toggle('invalid', !isValid);
                    errorElement.textContent = isValid ? '' : 'Please enter a valid email address';
                } else if (input.id === 'password') {
                    const username = document.getElementById('username').value;
                    const validation = validatePassword(input.value, username);
                    const isValid = validation.valid;
                    
                    input.classList.toggle('valid', isValid);
                    input.classList.toggle('invalid', !isValid);
                    errorElement.textContent = validation.message;
                    
                    // Also validate confirm password when password changes
                    const confirmPassword = document.getElementById('confirm-password');
                    if (confirmPassword.value.length > 0) {
                        const confirmValid = confirmPassword.value === input.value && isValid;
                        confirmPassword.classList.toggle('valid', confirmValid);
                        confirmPassword.classList.toggle('invalid', !confirmValid);
                        confirmPassword.nextElementSibling.nextElementSibling.textContent = confirmValid ? '' : 'Passwords do not match';
                    }
                } else if (input.id === 'confirm-password') {
                    const password = document.getElementById('password');
                    const passwordValidation = validatePassword(password.value, document.getElementById('username').value);
                    const isValid = input.value === password.value && passwordValidation.valid;
                    
                    input.classList.toggle('valid', isValid);
                    input.classList.toggle('invalid', !isValid);
                    errorElement.textContent = isValid ? '' : 'Passwords do not match';
                }
            } else {
                input.classList.remove('valid', 'invalid');
                errorElement.textContent = '';
            }
            
            validateForm();
        });
    });

    sendCodeBtn.addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Final validation check
        const passwordValidation = validatePassword(password, username);
        if (!passwordValidation.valid) {
            alert(passwordValidation.message);
            return;
        }

        // Check if passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        sendCodeBtn.disabled = true;
        sendCodeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        fetch('/send-verification-code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ 
                email: email,
                username: username,
                password: password 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Store form data in sessionStorage
                sessionStorage.setItem('registrationData', JSON.stringify({
                    username: username,
                    email: email,
                    password1: password,
                    password2: confirmPassword
                }));
                
                // Redirect to verification page
                window.location.href = '/verify/';
            } else {
                alert(data.message || 'Failed to send code.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        })
        .finally(() => {
            sendCodeBtn.disabled = false;
            sendCodeBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Verification Code';
        });
    });

    // Initial form validation
    validateForm();
});