// Authentication Module

function isAuthenticated() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    return !!(token && user);
}

function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function validateEmail(value) {
    const email = String(value || '').trim();
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}

function validateUsername(value) {
    const username = String(value || '').trim();
    return username.length >= 3 && username.length <= 20 && /^[a-zA-Z0-9_]+$/.test(username);
}

function validatePassword(value) {
    const password = String(value || '');
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    return password.length >= 8 && hasLetter && hasNumber;
}

function getPasswordStrength(password) {
    const length = String(password || '').length;
    const score = [/[a-z]/, /[A-Z]/, /[0-9]/, /[^a-zA-Z0-9]/].reduce((count, regex) => count + (regex.test(password) ? 1 : 0), 0);
    if (length >= 12 && score >= 3) return 'Strong password';
    if (length >= 10 && score >= 2) return 'Moderate password';
    return 'Weak password';
}

function getLoginValidationErrors(email, password) {
    const errors = {};
    if (!String(email || '').trim()) {
        errors.email = 'Email is required.';
    } else if (!validateEmail(email)) {
        errors.email = 'Please enter a valid email address.';
    }

    if (!String(password || '').trim()) {
        errors.password = 'Password is required.';
    } else if (String(password).length < 8) {
        errors.password = 'Password must be at least 8 characters.';
    }

    return errors;
}

function getRegisterValidationErrors(username, email, password, confirmPassword) {
    const errors = {};
    if (!String(username || '').trim()) {
        errors.username = 'Username is required.';
    } else if (!validateUsername(username)) {
        errors.username = 'Username must be 3-20 letters, numbers, or underscore.';
    }

    if (!String(email || '').trim()) {
        errors.email = 'Email is required.';
    } else if (!validateEmail(email)) {
        errors.email = 'Please enter a valid email address.';
    }

    if (!String(password || '').trim()) {
        errors.password = 'Password is required.';
    } else if (!validatePassword(password)) {
        errors.password = 'Password must be at least 8 characters and include letters and numbers.';
    }

    if (!String(confirmPassword || '').trim()) {
        errors.confirmPassword = 'Please confirm your password.';
    } else if (password !== confirmPassword) {
        errors.confirmPassword = 'Passwords do not match.';
    }

    return errors;
}

async function loginUser(email, password) {
    const trimmedEmail = String(email || '').trim();
    const trimmedPassword = String(password || '');
    const validationErrors = getLoginValidationErrors(trimmedEmail, trimmedPassword);

    if (Object.keys(validationErrors).length > 0) {
        const error = new Error('Validation failed.');
        error.validation = validationErrors;
        throw error;
    }

    const response = await authAPI.login(trimmedEmail, trimmedPassword);

    if (response && response.success) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        return response;
    }

    throw new Error('Login failed. Please try again.');
}

async function registerUser(username, email, password, confirmPassword, role = 'user') {
    const trimmedUsername = String(username || '').trim();
    const trimmedEmail = String(email || '').trim();
    const trimmedPassword = String(password || '');
    const trimmedConfirmPassword = String(confirmPassword || '');

    const validationErrors = getRegisterValidationErrors(trimmedUsername, trimmedEmail, trimmedPassword, trimmedConfirmPassword);

    if (Object.keys(validationErrors).length > 0) {
        const error = new Error('Validation failed.');
        error.validation = validationErrors;
        throw error;
    }

    const response = await authAPI.register(trimmedUsername, trimmedEmail, trimmedPassword, role);

    if (response && response.success) {
        return response;
    }

    throw new Error('Registration failed. Please try again.');
}

async function logoutUser() {
    try {
        await authAPI.logout();
    } finally {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }
}

window.authService = {
    isAuthenticated,
    getCurrentUser,
    validateEmail,
    validateUsername,
    validatePassword,
    getPasswordStrength,
    getLoginValidationErrors,
    getRegisterValidationErrors,
    loginUser,
    registerUser,
    logoutUser
};
