// Particle Animation
class ParticleAnimation {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 50;
        this.init();
    }

    init() {
        const container = document.getElementById('particles');
        if (!container) return;

        container.appendChild(this.canvas);
        this.resize();
        this.createParticles();
        this.animate();

        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 3 + 1,
                speedX: Math.random() * 0.5 - 0.25,
                speedY: Math.random() * 0.5 - 0.25,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            // Wrap around screen
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;

            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(16, 185, 129, ${particle.opacity})`;
            this.ctx.fill();
        });

        requestAnimationFrame(() => this.animate());
    }
}

// Login functionality
class LoginManager {
    constructor() {
        this.currentTab = 'login';
        this.init();
    }

    init() {
        this.bindEvents();
        new ParticleAnimation();
    }

    bindEvents() {
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const tabName = e.currentTarget.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });

        // Password toggle
        document.querySelectorAll('.toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const inputId = e.target.closest('.password-toggle').querySelector('input').id;
                this.togglePassword(inputId);
            });
        });

        // Form submissions
        document.getElementById('login-form').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('register-form').addEventListener('submit', (e) => this.handleRegister(e));

        // Input validation
        this.setupValidation();
    }

    switchTab(tab) {
        this.currentTab = tab;

        // Update tabs
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.form-container').forEach(f => f.classList.remove('active'));

        if (tab === 'login') {
            document.querySelectorAll('.tab')[0].classList.add('active');
            document.getElementById('login-form').classList.add('active');
        } else {
            document.querySelectorAll('.tab')[1].classList.add('active');
            document.getElementById('register-form').classList.add('active');
        }

        this.hideAlert();
        this.clearForms();
    }

    togglePassword(inputId) {
        const input = document.getElementById(inputId);
        const toggleBtn = input.parentNode.querySelector('.toggle-btn');
        const icon = toggleBtn.querySelector('i');

        if (input.type === 'password') {
            input.type = 'text';
            icon.setAttribute('data-lucide', 'eye-off');
        } else {
            input.type = 'password';
            icon.setAttribute('data-lucide', 'eye');
        }
        
        // Reinitialize Lucide icons
        lucide.createIcons();
    }

    showAlert(message, type) {
        const alert = document.getElementById('alert');
        alert.textContent = message;
        alert.className = `alert alert-${type} show`;

        // Auto-hide success messages after 3 seconds
        if (type === 'success') {
            setTimeout(() => this.hideAlert(), 3000);
        }
    }

    hideAlert() {
        const alert = document.getElementById('alert');
        alert.classList.remove('show');
    }

    clearForms() {
        // Clear only the non-active form
        const forms = document.querySelectorAll('.form-container');
        forms.forEach(form => {
            if (!form.classList.contains('active')) {
                form.querySelector('form').reset();
            }
        });
    }

    setupValidation() {
        // Real-time password confirmation validation
        const confirmPassword = document.getElementById('register-confirm');
        if (confirmPassword) {
            confirmPassword.addEventListener('input', () => {
                const password = document.getElementById('register-password').value;
                const confirm = confirmPassword.value;

                if (confirm && password !== confirm) {
                    confirmPassword.style.borderColor = 'var(--danger)';
                } else {
                    confirmPassword.style.borderColor = '';
                }
            });
        }

        // Username availability check (could be enhanced with backend API)
        const usernameInput = document.getElementById('register-username');
        if (usernameInput) {
            usernameInput.addEventListener('blur', () => {
                this.checkUsernameAvailability(usernameInput.value);
            });
        }
    }

    async checkUsernameAvailability(username) {
        if (username.length < 3) return;

        // This would typically call a backend API to check username availability
        // For now, we'll just simulate a check
        console.log(`Checking availability for username: ${username}`);
    }

    async handleLogin(e) {
        e.preventDefault();

        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const submitBtn = e.target.querySelector('.btn');

        // Show loading state
        this.setLoadingState(submitBtn, true);

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (data.success) {
                this.showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                this.showAlert(data.message || 'Invalid credentials', 'error');
            }
        } catch (error) {
            this.showAlert('Connection error. Please try again.', 'error');
            console.error('Login error:', error);
        } finally {
            this.setLoadingState(submitBtn, false);
        }
    }

    async handleRegister(e) {
        e.preventDefault();

        const fullName = document.getElementById('register-fullname').value;
        const username = document.getElementById('register-username').value;
        const currency = document.getElementById('register-currency').value;
        const password = document.getElementById('register-password').value;
        const confirm = document.getElementById('register-confirm').value;
        const submitBtn = e.target.querySelector('.btn');

        // Validation
        if (password !== confirm) {
            this.showAlert('Passwords do not match', 'error');
            return;
        }

        if (!this.validatePassword(password)) {
            this.showAlert(
                'Password must be at least 8 characters with uppercase, lowercase, number and special character',
                'error'
            );
            return;
        }

        // Show loading state
        this.setLoadingState(submitBtn, true);

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    full_name: fullName,
                    username,
                    currency,
                    password,
                }),
            });

            const data = await response.json();

            if (data.success) {
                this.showAlert('Registration successful! Please login.', 'success');
                setTimeout(() => this.switchTab('login'), 1500);
            } else {
                this.showAlert(data.message || 'Registration failed', 'error');
            }
        } catch (error) {
            this.showAlert('Connection error. Please try again.', 'error');
            console.error('Registration error:', error);
        } finally {
            this.setLoadingState(submitBtn, false);
        }
    }

    validatePassword(password) {
        const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
        return pattern.test(password);
    }

    setLoadingState(button, isLoading) {
        if (isLoading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }
}

// Initialize login manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});