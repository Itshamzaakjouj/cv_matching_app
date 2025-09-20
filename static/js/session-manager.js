// Gestionnaire de session
class SessionManager {
    constructor() {
        this.sessionKey = 'talentscope_session';
        this.checkSession();
    }

    checkSession() {
        const session = this.getSession();
        const currentPath = window.location.pathname;

        // Routes qui ne nécessitent pas d'authentification
        const publicRoutes = ['/auth', '/login', '/register'];
        
        if (!session && !publicRoutes.includes(currentPath)) {
            // Rediriger vers la page d'authentification
            this.redirectToAuth();
            return false;
        } else if (session && publicRoutes.includes(currentPath)) {
            // Rediriger vers le dashboard si déjà connecté
            this.redirectToDashboard();
            return false;
        }

        if (session) {
            this.updateUserInterface(session.user);
        }

        return true;
    }

    createSession(userData) {
        const session = {
            user: userData,
            timestamp: Date.now(),
            expiresAt: Date.now() + (24 * 60 * 60 * 1000) // 24 heures
        };

        localStorage.setItem(this.sessionKey, JSON.stringify(session));
        this.updateUserInterface(userData);
    }

    getSession() {
        const sessionData = localStorage.getItem(this.sessionKey);
        if (!sessionData) return null;

        const session = JSON.parse(sessionData);
        
        // Vérifier si la session a expiré
        if (Date.now() > session.expiresAt) {
            this.destroySession();
            return null;
        }

        return session;
    }

    destroySession() {
        localStorage.removeItem(this.sessionKey);
        this.redirectToAuth();
    }

    updateUserInterface(user) {
        // Mettre à jour les éléments de l'interface utilisateur
        const userElements = {
            name: document.getElementById('user-name'),
            role: document.getElementById('user-role'),
            avatar: document.getElementById('user-avatar')
        };

        if (userElements.name) {
            userElements.name.textContent = user.name;
        }

        if (userElements.role) {
            userElements.role.textContent = user.department;
        }

        if (userElements.avatar) {
            userElements.avatar.setAttribute('alt', `Photo de ${user.name}`);
        }
    }

    redirectToAuth() {
        window.location.href = '/auth';
    }

    redirectToDashboard() {
        window.location.href = '/dashboard';
    }

    // Méthodes utilitaires
    isAuthenticated() {
        return this.getSession() !== null;
    }

    getCurrentUser() {
        const session = this.getSession();
        return session ? session.user : null;
    }

    hasRole(role) {
        const user = this.getCurrentUser();
        return user && user.role === role;
    }

    refreshSession() {
        const session = this.getSession();
        if (session) {
            session.timestamp = Date.now();
            session.expiresAt = Date.now() + (24 * 60 * 60 * 1000);
            localStorage.setItem(this.sessionKey, JSON.stringify(session));
        }
    }
}

// Initialiser le gestionnaire de session
document.addEventListener('DOMContentLoaded', () => {
    window.sessionManager = new SessionManager();

    // Gestionnaire de déconnexion
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            window.sessionManager.destroySession();
        });
    }
});

