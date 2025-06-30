document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const inputs = document.querySelectorAll('.form-input');
    const sendCodeBtn = document.getElementById('sendCodeBtn');

    // Function to get CSRF token
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }

    const csrfToken = getCSRFToken();

    // Enhanced similarity check with configurable thresholds
    const SIMILARITY_THRESHOLD = 50; // Percentage
    const MIN_SEQUENCE_LENGTH = 4;   // Minimum similar sequence length

    function getSimilarityScore(str1, str2) {
        const s1 = str1.toLowerCase();
        const s2 = str2.toLowerCase();

        // Direct inclusion check
        if (s2.includes(s1)) return 100;
        if (s1.includes(s2)) return 100;

        // Common sequence check
        for (let i = 0; i <= s1.length - MIN_SEQUENCE_LENGTH; i++) {
            const sequence = s1.substr(i, MIN_SEQUENCE_LENGTH);
            if (s2.includes(sequence)) return 100;
        }

        // Character similarity percentage
        const set1 = new Set(s1);
        const set2 = new Set(s2);
        const intersection = new Set([...set1].filter(c => set2.has(c)));
        return (intersection.size / (set1.size + set2.size - intersection.size)) * 100;
    }

function validatePassword(password, username) {
    const MIN_LENGTH = 9;
    const SIMILARITY_THRESHOLD = 0.7;
    const MIN_SEQUENCE_LENGTH = 3;

    if (password.length < MIN_LENGTH) {
        return { valid: false, message: "Password must be at least 9 characters" };
    }

    const requirements = [
        { test: /[0-9]/, message: "a number (0-9)", priority: 1 },
        { test: /[A-Z]/, message: "an uppercase letter (A-Z)", priority: 2 },
        { test: /[a-z]/, message: "a lowercase letter (a-z)", priority: 3 },
        { test: /[^A-Za-z0-9]/, message: "a special character (!@#$% etc.)", priority: 4 }
    ];

    const met = requirements.filter(req => req.test.test(password));
    const missing = requirements.filter(req => !req.test.test(password)).sort((a, b) => a.priority - b.priority);

    if (met.length < 3) {
        const neededCount = 3 - met.length;
        const toShow = missing.slice(0, neededCount).map(r => r.message);
        const formatted = formatList(toShow);
        return {
            valid: false,
            message: `Password needs ${formatted}`
        };
    }

    if (username && username.length > 0) {
        const similarity = getSimilarityScore(username, password);
        if (similarity >= SIMILARITY_THRESHOLD) {
            return { valid: false, message: "Password is too similar to username" };
        }

        const usernameParts = username.toLowerCase().match(new RegExp(`.{${MIN_SEQUENCE_LENGTH},}`, 'g')) || [];
        if (usernameParts.some(part => password.toLowerCase().includes(part))) {
            return { valid: false, message: "Password contains username fragments" };
        }
    }

    return { valid: true, message: "" };
}

// Helper: "a, b, or c"
function formatList(items) {
    if (items.length === 1) return items[0];
    if (items.length === 2) return `${items[0]} or ${items[1]}`;
    return `${items.slice(0, -1).join(', ')}, or ${items[items.length - 1]}`;
}

    function updateValidationStatus(input, isValid, message = '') {
        const errorElement = input.nextElementSibling.nextElementSibling;
        input.classList.toggle('valid', isValid);
        input.classList.toggle('invalid', !isValid && input.value.length > 0);
        errorElement.textContent = message;
    }

    function validateForm() {
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        const isUsernameValid = username.length >= 7;
        const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        const passwordValidation = validatePassword(password, username);
        const passwordsMatch = password === confirmPassword && passwordValidation.valid;

        sendCodeBtn.disabled = !(isUsernameValid && isEmailValid && passwordValidation.valid && passwordsMatch);
    }

    function handleInputValidation(input) {
        const value = input.value.trim();

        if (value.length === 0) {
            updateValidationStatus(input, true);
            return;
        }

        switch(input.id) {
            case 'username':
                updateValidationStatus(
                    input,
                    value.length >= 7,
                    'Username must be at least 7 characters'
                );
                break;

            case 'email':
                updateValidationStatus(
                    input,
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
                    'Please enter a valid email'
                );
                break;

            case 'password':
                const username = document.getElementById('username').value;
                const validation = validatePassword(value, username);
                updateValidationStatus(input, validation.valid, validation.message);
                break;

            case 'confirm-password':
                const password = document.getElementById('password').value;
                const passwordValidation = validatePassword(password, document.getElementById('username').value);
                const isValid = value === password && passwordValidation.valid;
                updateValidationStatus(
                    input,
                    isValid,
                    isValid ? '' : 'Passwords do not match'
                );
                break;
        }
    }

    // Event listeners
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            handleInputValidation(input);
            validateForm();

            // Special case: validate confirm password when password changes
            if (input.id === 'password') {
                const confirmPassword = document.getElementById('confirm-password');
                if (confirmPassword.value.length > 0) {
                    handleInputValidation(confirmPassword);
                }
            }
        });

        // Validate on blur as well
        input.addEventListener('blur', () => handleInputValidation(input));
    });

   sendCodeBtn.addEventListener('click', async () => {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    const passwordValidation = validatePassword(password, username);
    if (!passwordValidation.valid) {
        alert(passwordValidation.message);
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    try {
        sendCodeBtn.disabled = true;
        sendCodeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        const response = await fetch('/send-verification-code/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                email,
                username,
                password
            })
        });

        const data = await response.json();

        if (data.success) {
            sessionStorage.setItem('registrationData', JSON.stringify({
                username,
                email,
                password1: password,
                password2: confirmPassword
            }));
            window.location.href = '/verify/';
        } else {
            alert(data.message || 'Failed to send code.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        sendCodeBtn.disabled = false;
        sendCodeBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Verification Code';
    }
});


    // Initial form validation
    validateForm();
});