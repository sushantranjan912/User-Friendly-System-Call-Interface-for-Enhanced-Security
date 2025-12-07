// Authentication Module

// Check if user is authenticated
function isAuthenticated() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    return !!(token && user);
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Login function
async function login(username, password) {
    try {
        const response = await authAPI.login(username, password);

        if (response.success) {
            // Store token and user info
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));

            showToast('Login successful!', 'success');

            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/pages/dashboard.html';
            }, 1000);
        }
    } catch (error) {
        showToast(error.message || 'Login failed', 'error');
        throw error;
    }
}

// Register function
async function register(username, email, password, role) {
    try {
        const response = await authAPI.register(username, email, password, role);

        if (response.success) {
            showToast('Registration successful! Please login.', 'success');

            // Close register modal and open login modal
            setTimeout(() => {
                const registerModal = document.getElementById('registerModal');
                const loginModal = document.getElementById('loginModal');
                if (registerModal) registerModal.classList.remove('active');
                if (loginModal) loginModal.classList.add('active');
            }, 1500);
        }
    } catch (error) {
        showToast(error.message || 'Registration failed', 'error');
        throw error;
    }
}

// Logout function
async function logout() {
    try {
        await authAPI.logout();
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear local storage
        localStorage.removeItem('token');
        localStorage.removeItem('user');

        showToast('Logged out successfully', 'info');

        // Redirect to home
        setTimeout(() => {
            window.location.href = '/';
        }, 1000);
    }
}

// Load user info in navbar
function loadUserInfo() {
    const user = getCurrentUser();
    if (user) {
        const userNameEl = document.getElementById('userName');
        const userAvatarEl = document.getElementById('userAvatar');

        if (userNameEl) userNameEl.textContent = user.username;
        if (userAvatarEl) userAvatarEl.textContent = user.username.charAt(0).toUpperCase();
    }
}

// Setup logout button
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
});
