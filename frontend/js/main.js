// Main Application Entry Point

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 System Call Interface Initialized');

    // Setup Login Modal
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeLogin = document.getElementById('closeLogin');

    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal('loginModal');
        });
    }

    if (closeLogin) {
        closeLogin.addEventListener('click', () => {
            closeModal('loginModal');
        });
    }

    // Setup Register Modal
    const registerBtn = document.getElementById('registerBtn');
    const heroGetStarted = document.getElementById('heroGetStarted');
    const registerModal = document.getElementById('registerModal');
    const closeRegister = document.getElementById('closeRegister');

    if (registerBtn) {
        registerBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal('registerModal');
        });
    }

    if (heroGetStarted) {
        heroGetStarted.addEventListener('click', () => {
            openModal('registerModal');
        });
    }

    if (closeRegister) {
        closeRegister.addEventListener('click', () => {
            closeModal('registerModal');
        });
    }

    // Login Form Submit
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            const errorEl = document.getElementById('loginError');

            if (errorEl) errorEl.classList.add('hidden');

            try {
                await login(username, password);
            } catch (error) {
                if (errorEl) {
                    errorEl.textContent = error.message || 'Login failed';
                    errorEl.classList.remove('hidden');
                }
            }
        });
    }

    // Register Form Submit
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const role = document.getElementById('registerRole').value;
            const errorEl = document.getElementById('registerError');

            if (errorEl) errorEl.classList.add('hidden');

            try {
                await register(username, email, password, role);
            } catch (error) {
                if (errorEl) {
                    errorEl.textContent = error.message || 'Registration failed';
                    errorEl.classList.remove('hidden');
                }
            }
        });
    }

    // Hero Learn More Button
    const heroLearnMore = document.getElementById('heroLearnMore');
    if (heroLearnMore) {
        heroLearnMore.addEventListener('click', () => {
            document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Add fade-in animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});
