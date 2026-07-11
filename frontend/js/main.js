// Main Application Entry Point

function initUI() {
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

    function clearFormErrors(formElement) {
        formElement.querySelectorAll('.form-error, .form-success').forEach(el => {
            el.textContent = '';
            el.classList.add('hidden');
            el.classList.remove('visible');
        });
        formElement.querySelectorAll('.form-input').forEach(input => {
            input.classList.remove('invalid');
            input.classList.remove('valid');
        });
    }

    function setFormError(inputId, message) {
        const errorEl = document.getElementById(inputId);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.classList.remove('hidden');
            errorEl.classList.add('visible');
        }
        const input = errorEl ? errorEl.closest('.form-group')?.querySelector('.form-input') : null;
        if (input) {
            input.classList.add('invalid');
        }
    }

    function setSuccessMessage(inputId, message) {
        const successEl = document.getElementById(inputId);
        if (successEl) {
            successEl.textContent = message;
            successEl.classList.remove('hidden');
            successEl.classList.add('visible');
        }
    }

    function setButtonLoading(button, isLoading) {
        if (!button) return;
        button.disabled = isLoading;
        button.classList.toggle('btn-loading', isLoading);
    }

    // Login Form Submit
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearFormErrors(loginForm);

            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const submitButton = document.getElementById('loginSubmitButton');
            const errorEl = document.getElementById('loginError');

            setButtonLoading(submitButton, true);

            try {
                await authService.loginUser(email, password);
                showToast('Login successful!', 'success');
                setTimeout(() => {
                    window.location.href = 'pages/dashboard.html';
                }, 600);
            } catch (error) {
                if (error.validation) {
                    if (error.validation.email) setFormError('loginEmailError', error.validation.email);
                    if (error.validation.password) setFormError('loginPasswordError', error.validation.password);
                    const firstInvalid = loginForm.querySelector('.form-input.invalid');
                    if (firstInvalid) firstInvalid.focus();
                } else if (errorEl) {
                    errorEl.textContent = error.message || 'Login failed. Please try again.';
                    errorEl.classList.remove('hidden');
                    submitButton?.focus();
                }
            } finally {
                setButtonLoading(submitButton, false);
            }
        });
    }

    // Register Form Submit
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        const passwordInput = document.getElementById('registerPassword');
        const strengthEl = document.getElementById('registerPasswordStrength');

        passwordInput?.addEventListener('input', () => {
            if (strengthEl && passwordInput.value) {
                setSuccessMessage('registerPasswordStrength', authService.getPasswordStrength(passwordInput.value));
            } else if (strengthEl) {
                strengthEl.textContent = '';
                strengthEl.classList.add('hidden');
            }
        });

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearFormErrors(registerForm);

            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('registerConfirmPassword').value;
            const role = document.getElementById('registerRole').value;
            const submitButton = document.getElementById('registerSubmitButton');
            const errorEl = document.getElementById('registerError');

            setButtonLoading(submitButton, true);

            try {
                await authService.registerUser(username, email, password, confirmPassword, role);
                showToast('Registration successful! Please login.', 'success');
                setTimeout(() => {
                    const registerModal = document.getElementById('registerModal');
                    const loginModal = document.getElementById('loginModal');
                    if (registerModal) registerModal.classList.remove('active');
                    if (loginModal) loginModal.classList.add('active');
                }, 800);
            } catch (error) {
                if (error.validation) {
                    if (error.validation.username) setFormError('registerUsernameError', error.validation.username);
                    if (error.validation.email) setFormError('registerEmailError', error.validation.email);
                    if (error.validation.password) setFormError('registerPasswordError', error.validation.password);
                    if (error.validation.confirmPassword) setFormError('registerConfirmPasswordError', error.validation.confirmPassword);
                    const firstInvalid = registerForm.querySelector('.form-input.invalid');
                    if (firstInvalid) firstInvalid.focus();
                } else if (errorEl) {
                    errorEl.textContent = error.message || 'Registration failed. Please try again.';
                    errorEl.classList.remove('hidden');
                    submitButton?.focus();
                }
            } finally {
                setButtonLoading(submitButton, false);
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

    }

    // Ensure handlers run even if DOMContentLoaded already fired
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUI);
    } else {
        initUI();
    }
