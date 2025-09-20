// Base de données utilisateur simplifiée
window.userDatabase = {
    users: [
        {
            email: "akjouj17@gmail.com",
            password: "Hamza12345",
            fullName: "Akjouj Hamza",
            department: "Ministère des Finances",
            position: "Administrateur"
        },
        {
            email: "elhafsaghazouani@gmail.com",
            password: "Hafsa2003",
            fullName: "Hafsa El Ghazouani",
            department: "Ministère des Finances",
            position: "Utilisateur"
        }
    ],

    authenticateUser: function(email, password) {
        const user = this.users.find(u => u.email === email && u.password === password);
        if (user) {
            // Stocker l'utilisateur dans localStorage
            localStorage.setItem('currentUser', JSON.stringify(user));
            // Rediriger vers le dashboard moderne
            window.location.href = 'http://localhost:8087/dashboard';
            return true;
        }
        return false;
    },

    getCurrentUser: function() {
        const userJson = localStorage.getItem('currentUser');
        return userJson ? JSON.parse(userJson) : null;
    },

    setCurrentUser: function(user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        return true;
    },

    emailExists: function(email) {
        return this.users.some(u => u.email === email);
    },

    findUserByEmail: function(email) {
        return this.users.find(u => u.email === email) || null;
    },

    createUser: function(email, password, fullName, department, position) {
        if (this.emailExists(email)) {
            return false;
        }

        const newUser = {
            email,
            password,
            fullName,
            department,
            position
        };

        this.users.push(newUser);
        return newUser;
    }
};

