// ===== TALENTSCOPE - AUTHENTICATION JAVASCRIPT =====

// Gestionnaire d'authentification
const AuthManager = {
    // Configuration
    config: {
        sessionKey: 'talentScope_session',
        apiBaseUrl: '',
        redirectDelay: 1000
    },

    // Initialisation
    init: () => {
        Utils.log('Initialisation du gestionnaire d\'authentification');
        
        // Vérifier si l'utilisateur est déjà connecté
        if (AuthManager.isLoggedIn()) {
            Utils.log('Utilisateur déjà connecté, redirection...');
            AuthManager.redirectToDashboard();
            return;
        }

        // Initialiser les formulaires
        AuthManager.initForms();
        
        // Initialiser les interactions
        AuthManager.initInteractions();
    },

    // Initialiser les formulaires
    initForms: () => {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (loginForm) {
            loginForm.addEventListener('submit', AuthManager.handleLogin);
        }

        if (registerForm) {
            registerForm.addEventListener('submit', AuthManager.handleRegister);
        }
    },

    // Initialiser les interactions
    initInteractions: () => {
        // Toggle password visibility
        window.togglePassword = (inputId = 'password') => {
            const input = document.getElementById(inputId);
            const button = input.nextElementSibling;
            const icon = button.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                input.type = 'password';
                icon.className = 'fas fa-eye';
            }
        };

        // Show register form
        window.showRegister = () => {
            const loginCard = document.querySelector('.auth-card');
            const registerCard = document.getElementById('registerCard');
            
            if (loginCard && registerCard) {
                loginCard.style.display = 'none';
                registerCard.style.display = 'block';
            }
        };

        // Show login form
        window.showLogin = () => {
            const loginCard = document.querySelector('.auth-card');
            const registerCard = document.getElementById('registerCard');
            
            if (loginCard && registerCard) {
                registerCard.style.display = 'none';
                loginCard.style.display = 'block';
            }
        };

        // Social login
        window.socialLogin = () => {
            Notifications.info('Connexion Microsoft en cours...');
            // Simulation de connexion sociale
            setTimeout(() => {
                AuthManager.simulateLogin({
                    name: 'Utilisateur Microsoft',
                    role: 'user'
                });
            }, 2000);
        };
    },

    // Gérer la connexion
    handleLogin: async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const email = formData.get('email');
        const password = formData.get('password');
        const remember = formData.get('remember');

        // Validation
        if (!AuthManager.validateLoginForm(email, password)) {
            return;
        }

        // Afficher le loader
        const loader = Loading.show();

        try {
            // Simulation d'API (remplacer par vraie API)
            const response = await AuthManager.simulateLoginRequest(email, password);
            
            if (response.success) {
                // Sauvegarder la session
                AuthManager.saveSession(response.session_id, response.user, remember);
                
                // Notification de succès
                Notifications.success('Connexion réussie !');
                
                // Redirection
                setTimeout(() => {
                    AuthManager.redirectToDashboard();
                }, AuthManager.config.redirectDelay);
            } else {
                Notifications.error(response.message || 'Erreur de connexion');
            }
        } catch (error) {
            Utils.log('Erreur de connexion', error);
            Notifications.error('Erreur de connexion. Veuillez réessayer.');
        } finally {
            Loading.hide(loader);
        }
    },

    // Gérer l'inscription
    handleRegister: async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const name = formData.get('name');
        const email = formData.get('email');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');

        // Validation
        if (!AuthManager.validateRegisterForm(name, email, password, confirmPassword)) {
            return;
        }

        // Afficher le loader
        const loader = Loading.show();

        try {
            // Simulation d'API (remplacer par vraie API)
            const response = await AuthManager.simulateRegisterRequest(name, email, password);
            
            if (response.success) {
                Notifications.success('Compte créé avec succès !');
                
                // Basculer vers le formulaire de connexion
                setTimeout(() => {
                    showLogin();
                }, 1000);
            } else {
                Notifications.error(response.message || 'Erreur lors de la création du compte');
            }
        } catch (error) {
            Utils.log('Erreur d\'inscription', error);
            Notifications.error('Erreur lors de la création du compte. Veuillez réessayer.');
        } finally {
            Loading.hide(loader);
        }
    },

    // Valider le formulaire de connexion
    validateLoginForm: (email, password) => {
        if (!email || !password) {
            Notifications.error('Veuillez remplir tous les champs');
            return false;
        }

        if (!Utils.isValidEmail(email)) {
            Notifications.error('Veuillez saisir une adresse email valide');
            return false;
        }

        if (password.length < 6) {
            Notifications.error('Le mot de passe doit contenir au moins 6 caractères');
            return false;
        }

        return true;
    },

    // Valider le formulaire d'inscription
    validateRegisterForm: (name, email, password, confirmPassword) => {
        if (!name || !email || !password || !confirmPassword) {
            Notifications.error('Veuillez remplir tous les champs');
            return false;
        }

        if (name.length < 2) {
            Notifications.error('Le nom doit contenir au moins 2 caractères');
            return false;
        }

        if (!Utils.isValidEmail(email)) {
            Notifications.error('Veuillez saisir une adresse email valide');
            return false;
        }

        if (password.length < 6) {
            Notifications.error('Le mot de passe doit contenir au moins 6 caractères');
            return false;
        }

        if (password !== confirmPassword) {
            Notifications.error('Les mots de passe ne correspondent pas');
            return false;
        }

        return true;
    },

    // Simuler une requête de connexion
    simulateLoginRequest: async (email, password) => {
        // Simulation d'un délai réseau
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Comptes de test
        const testAccounts = {
            'admin@ministere.gov.ma': { password: 'admin123', name: 'Administrateur', role: 'admin' },
            'user@ministere.gov.ma': { password: 'user123', name: 'Utilisateur', role: 'user' }
        };

        if (testAccounts[email] && testAccounts[email].password === password) {
            return {
                success: true,
                session_id: `session_${Date.now()}`,
                user: {
                    name: testAccounts[email].name,
                    role: testAccounts[email].role
                }
            };
        } else {
            return {
                success: false,
                message: 'Email ou mot de passe incorrect'
            };
        }
    },

    // Simuler une requête d'inscription
    simulateRegisterRequest: async (name, email, password) => {
        // Simulation d'un délai réseau
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Vérifier si l'email existe déjà
        const existingEmails = ['admin@ministere.gov.ma', 'user@ministere.gov.ma'];
        if (existingEmails.includes(email)) {
            return {
                success: false,
                message: 'Cette adresse email est déjà utilisée'
            };
        }

        return {
            success: true,
            message: 'Compte créé avec succès'
        };
    },

    // Simuler une connexion (pour les tests)
    simulateLogin: (user) => {
        const sessionId = `session_${Date.now()}`;
        AuthManager.saveSession(sessionId, user, true);
        Notifications.success('Connexion réussie !');
        setTimeout(() => {
            AuthManager.redirectToDashboard();
        }, AuthManager.config.redirectDelay);
    },

    // Sauvegarder la session
    saveSession: (sessionId, user, remember = false) => {
        const sessionData = {
            session_id: sessionId,
            user: user,
            timestamp: Date.now()
        };

        if (remember) {
            localStorage.setItem(AuthManager.config.sessionKey, JSON.stringify(sessionData));
        } else {
            sessionStorage.setItem(AuthManager.config.sessionKey, JSON.stringify(sessionData));
        }

        Utils.log('Session sauvegardée', sessionData);
    },

    // Vérifier si l'utilisateur est connecté
    isLoggedIn: () => {
        const sessionData = AuthManager.getSessionData();
        return sessionData !== null;
    },

    // Obtenir les données de session
    getSessionData: () => {
        try {
            const data = localStorage.getItem(AuthManager.config.sessionKey) || 
                        sessionStorage.getItem(AuthManager.config.sessionKey);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            Utils.log('Erreur lors de la lecture de la session', error);
            return null;
        }
    },

    // Déconnexion
    logout: () => {
        localStorage.removeItem(AuthManager.config.sessionKey);
        sessionStorage.removeItem(AuthManager.config.sessionKey);
        Notifications.info('Déconnexion réussie');
        
        // Redirection vers la page de connexion
        setTimeout(() => {
            window.location.href = '/auth';
        }, 1000);
    },

    // Redirection vers le tableau de bord
    redirectToDashboard: () => {
        const sessionData = AuthManager.getSessionData();
        if (sessionData) {
            window.location.href = `/dashboard?session_id=${sessionData.session_id}`;
        } else {
            window.location.href = '/auth';
        }
    },

    // Obtenir l'utilisateur actuel
    getCurrentUser: () => {
        const sessionData = AuthManager.getSessionData();
        return sessionData ? sessionData.user : null;
    },

    // Obtenir l'ID de session
    getSessionId: () => {
        const sessionData = AuthManager.getSessionData();
        return sessionData ? sessionData.session_id : null;
    }
};

// Fonctions globales pour les boutons
window.logout = AuthManager.logout;
window.togglePassword = (inputId = 'password') => {
    const input = document.getElementById(inputId);
    const button = input.nextElementSibling;
    const icon = button.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fas fa-eye';
    }
};

window.showRegister = () => {
    const loginCard = document.querySelector('.auth-card');
    const registerCard = document.getElementById('registerCard');
    
    if (loginCard && registerCard) {
        loginCard.style.display = 'none';
        registerCard.style.display = 'block';
    }
};

window.showLogin = () => {
    const loginCard = document.querySelector('.auth-card');
    const registerCard = document.getElementById('registerCard');
    
    if (loginCard && registerCard) {
        registerCard.style.display = 'none';
        loginCard.style.display = 'block';
    }
};

window.socialLogin = () => {
    Notifications.info('Connexion Microsoft en cours...');
    setTimeout(() => {
        AuthManager.simulateLogin({
            name: 'Utilisateur Microsoft',
            role: 'user'
        });
    }, 2000);
};

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    Utils.log('Initialisation de la page d\'authentification');
    AuthManager.init();
});

// Export pour utilisation globale
window.AuthManager = AuthManager;
