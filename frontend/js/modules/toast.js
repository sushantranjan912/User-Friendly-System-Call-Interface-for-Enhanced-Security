// Toast Notification System

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer') || createToastContainer();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    document.body.appendChild(container);

    // Add toast styles if not already present
    if (!document.getElementById('toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            .toast {
                padding: 1rem 1.5rem;
                border-radius: 12px;
                color: white;
                font-weight: 500;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
                opacity: 0;
                transform: translateX(100px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                min-width: 250px;
                max-width: 400px;
            }
            
            .toast.show {
                opacity: 1;
                transform: translateX(0);
            }
            
            .toast-success {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            }
            
            .toast-error {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            }
            
            .toast-warning {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            }
            
            .toast-info {
                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            }
        `;
        document.head.appendChild(style);
    }

    return container;
}
