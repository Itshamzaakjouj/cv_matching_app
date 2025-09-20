// ===== TALENTSCOPE - MAIN JAVASCRIPT =====

// Configuration
const CONFIG = {
    API_BASE_URL: '',
    VERSION: '2.0.0',
    DEBUG: true
};

// Utilitaires
const Utils = {
    // Logging
    log: (message, data = null) => {
        if (CONFIG.DEBUG) {
            console.log(`[TalentScope] ${message}`, data || '');
        }
    },

    // Animation d'apparition
    fadeIn: (element, duration = 300) => {
        element.style.opacity = '0';
        element.style.display = 'block';
        
        let start = performance.now();
        
        function animate(currentTime) {
            let elapsed = currentTime - start;
            let progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    },

    // Animation de disparition
    fadeOut: (element, duration = 300) => {
        let start = performance.now();
        
        function animate(currentTime) {
            let elapsed = currentTime - start;
            let progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = 1 - progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.display = 'none';
            }
        }
        
        requestAnimationFrame(animate);
    },

    // Formatage des dates
    formatDate: (date) => {
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Formatage des nombres
    formatNumber: (number) => {
        return new Intl.NumberFormat('fr-FR').format(number);
    },

    // Validation email
    isValidEmail: (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Debounce
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Throttle
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Gestionnaire d'événements
const EventHandler = {
    // Initialisation
    init: () => {
        Utils.log('Initialisation des événements');
        
        // Navigation
        EventHandler.initNavigation();
        
        // Animations
        EventHandler.initAnimations();
        
        // Formulaires
        EventHandler.initForms();
    },

    // Navigation
    initNavigation: () => {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                if (href && href !== '#') {
                    window.location.href = href;
                }
            });
        });
    },

    // Animations
    initAnimations: () => {
        // Animation des cartes au scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        const animatedElements = document.querySelectorAll('.feature-card, .stat-card, .chart-card');
        animatedElements.forEach(el => observer.observe(el));
    },

    // Formulaires
    initForms: () => {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                Utils.log('Soumission de formulaire', form.id);
            });
        });
    }
};

// API Client
const API = {
    // Requête générique
    request: async (url, options = {}) => {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            Utils.log(`Requête API: ${url}`, config);
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            Utils.log('Réponse API reçue', data);
            return data;
        } catch (error) {
            Utils.log('Erreur API', error);
            throw error;
        }
    },

    // GET
    get: (url) => API.request(url, { method: 'GET' }),

    // POST
    post: (url, data) => API.request(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }),

    // PUT
    put: (url, data) => API.request(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    }),

    // DELETE
    delete: (url) => API.request(url, { method: 'DELETE' })
};

// Gestionnaire de notifications
const Notifications = {
    // Afficher une notification
    show: (message, type = 'info', duration = 5000) => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${Notifications.getIcon(type)}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="Notifications.hide(this.parentElement.parentElement)">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            min-width: 300px;
            max-width: 500px;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        // Auto-hide
        if (duration > 0) {
            setTimeout(() => Notifications.hide(notification), duration);
        }

        return notification;
    },

    // Masquer une notification
    hide: (notification) => {
        if (notification && notification.parentNode) {
            notification.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    },

    // Obtenir l'icône selon le type
    getIcon: (type) => {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    // Méthodes de convenance
    success: (message, duration) => Notifications.show(message, 'success', duration),
    error: (message, duration) => Notifications.show(message, 'error', duration),
    warning: (message, duration) => Notifications.show(message, 'warning', duration),
    info: (message, duration) => Notifications.show(message, 'info', duration)
};

// Gestionnaire de chargement
const Loading = {
    // Afficher le loader
    show: (element = document.body) => {
        const loader = document.createElement('div');
        loader.className = 'loading-overlay';
        loader.innerHTML = `
            <div class="loading-content">
                <div class="spinner"></div>
                <p>Chargement...</p>
            </div>
        `;

        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            backdrop-filter: blur(4px);
        `;

        element.appendChild(loader);
        return loader;
    },

    // Masquer le loader
    hide: (loader) => {
        if (loader && loader.parentNode) {
            loader.parentNode.removeChild(loader);
        }
    }
};

// Gestionnaire de modales
const Modal = {
    // Afficher une modale
    show: (title, content, options = {}) => {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close" onclick="Modal.hide(this.closest('.modal-overlay'))">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                <div class="modal-footer">
                    ${options.buttons || '<button class="btn btn-primary" onclick="Modal.hide(this.closest(\'.modal-overlay\'))">Fermer</button>'}
                </div>
            </div>
        `;

        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease-out;
        `;

        document.body.appendChild(modal);
        return modal;
    },

    // Masquer une modale
    hide: (modal) => {
        if (modal && modal.parentNode) {
            modal.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => {
                if (modal.parentNode) {
                    modal.parentNode.removeChild(modal);
                }
            }, 300);
        }
    }
};

// Initialisation de l'application
document.addEventListener('DOMContentLoaded', () => {
    Utils.log('Application TalentScope initialisée');
    
    // Initialiser les gestionnaires d'événements
    EventHandler.init();
    
    // Afficher un message de bienvenue
    if (CONFIG.DEBUG) {
        Notifications.info('Application TalentScope chargée avec succès !');
    }
});

// Export pour utilisation globale
window.TalentScope = {
    Utils,
    API,
    Notifications,
    Loading,
    Modal,
    CONFIG
};
