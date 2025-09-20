/**
 * Base de données utilisateurs pour TalentScope
 * Gestion multi-utilisateurs avec localStorage
 */

class UserDatabase {
    constructor() {
        this.storageKey = 'talentScope_users';
        this.currentUserKey = 'talentScope_current_user';
        this.initializeDatabase();
    }

    /**
     * Initialise la base de données si elle n'existe pas
     */
    initializeDatabase() {
        if (!localStorage.getItem(this.storageKey)) {
            localStorage.setItem(this.storageKey, JSON.stringify({}));
            console.log('Base de données utilisateurs initialisée');
        }
    }

    /**
     * Récupère tous les utilisateurs
     */
    getAllUsers() {
        try {
            const users = localStorage.getItem(this.storageKey);
            return users ? JSON.parse(users) : {};
        } catch (e) {
            console.error('Erreur lors de la récupération des utilisateurs:', e);
            return {};
        }
    }

    /**
     * Sauvegarde tous les utilisateurs
     */
    saveAllUsers(users) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(users));
            return true;
        } catch (e) {
            console.error('Erreur lors de la sauvegarde des utilisateurs:', e);
            return false;
        }
    }

    /**
     * Crée un nouvel utilisateur
     */
    createUser(email, password, fullName, department = 'Ministère des Finances', position = 'Utilisateur', phone = '') {
        const users = this.getAllUsers();
        const userId = this.generateUserId();
        
        const newUser = {
            id: userId,
            email: email,
            fullName: fullName,
            department: department,
            position: position,
            phone: phone,
            password: password, // En production, il faudrait hasher le mot de passe
            createdAt: new Date().toISOString(),
            lastLogin: new Date().toISOString(),
            isActive: true
        };

        users[userId] = newUser;
        
        if (this.saveAllUsers(users)) {
            console.log('Utilisateur créé:', newUser.fullName);
            return newUser;
        } else {
            console.error('Erreur lors de la création de l\'utilisateur');
            return null;
        }
    }

    /**
     * Trouve un utilisateur par email
     */
    findUserByEmail(email) {
        const users = this.getAllUsers();
        for (const userId in users) {
            if (users[userId].email === email) {
                return users[userId];
            }
        }
        return null;
    }

    /**
     * Trouve un utilisateur par ID
     */
    findUserById(userId) {
        const users = this.getAllUsers();
        return users[userId] || null;
    }

    /**
     * Met à jour un utilisateur
     */
    updateUser(userId, updateData) {
        const users = this.getAllUsers();
        if (users[userId]) {
            users[userId] = { ...users[userId], ...updateData };
            if (this.saveAllUsers(users)) {
                console.log('Utilisateur mis à jour:', users[userId].fullName);
                return users[userId];
            }
        }
        return null;
    }

    /**
     * Authentifie un utilisateur
     */
    authenticateUser(email, password) {
        const user = this.findUserByEmail(email);
        if (user && user.password === password && user.isActive) {
            // Mettre à jour la dernière connexion
            user.lastLogin = new Date().toISOString();
            this.updateUser(user.id, { lastLogin: user.lastLogin });
            
            // Définir comme utilisateur actuel
            this.setCurrentUser(user);
            
            console.log('Utilisateur authentifié:', user.fullName);
            return user;
        }
        return null;
    }

    /**
     * Définit l'utilisateur actuel
     */
    setCurrentUser(user) {
        try {
            localStorage.setItem(this.currentUserKey, JSON.stringify(user));
            console.log('Utilisateur actuel défini:', user.fullName);
            return true;
        } catch (e) {
            console.error('Erreur lors de la définition de l\'utilisateur actuel:', e);
            return false;
        }
    }

    /**
     * Récupère l'utilisateur actuel
     */
    getCurrentUser() {
        try {
            const currentUser = localStorage.getItem(this.currentUserKey);
            return currentUser ? JSON.parse(currentUser) : null;
        } catch (e) {
            console.error('Erreur lors de la récupération de l\'utilisateur actuel:', e);
            return null;
        }
    }

    /**
     * Déconnecte l'utilisateur actuel
     */
    logout() {
        localStorage.removeItem(this.currentUserKey);
        console.log('Utilisateur déconnecté');
    }

    /**
     * Génère un ID unique pour un utilisateur
     */
    generateUserId() {
        return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Vérifie si un email existe déjà
     */
    emailExists(email) {
        return this.findUserByEmail(email) !== null;
    }

    /**
     * Obtient les statistiques des utilisateurs
     */
    getUserStats() {
        const users = this.getAllUsers();
        const totalUsers = Object.keys(users).length;
        const activeUsers = Object.values(users).filter(user => user.isActive).length;
        
        return {
            totalUsers,
            activeUsers,
            inactiveUsers: totalUsers - activeUsers
        };
    }

    /**
     * Liste tous les utilisateurs (pour l'administration)
     */
    listUsers() {
        const users = this.getAllUsers();
        return Object.values(users).map(user => ({
            id: user.id,
            fullName: user.fullName,
            email: user.email,
            department: user.department,
            position: user.position,
            createdAt: user.createdAt,
            lastLogin: user.lastLogin,
            isActive: user.isActive
        }));
    }
}

// Instance globale de la base de données
window.userDatabase = new UserDatabase();

// Fonctions utilitaires globales
window.getCurrentUser = function() {
    return window.userDatabase.getCurrentUser();
};

window.setCurrentUser = function(user) {
    return window.userDatabase.setCurrentUser(user);
};

window.logoutUser = function() {
    return window.userDatabase.logout();
};

console.log('Base de données utilisateurs chargée');


