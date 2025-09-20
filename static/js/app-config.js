// Configuration de l'application
const AppConfig = {
    // Configuration du serveur
    server: {
        host: 'localhost',
        port: 8083,
        baseUrl: 'http://localhost:8083'
    },

    // Configuration de l'authentification
    auth: {
        sessionDuration: 24 * 60 * 60 * 1000, // 24 heures
        allowedDomains: ['finances.gov.ma', 'mef.gov.ma'],
        defaultRedirect: '/dashboard'
    },

    // Configuration de l'interface
    ui: {
        theme: {
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#10B981',
            warning: '#F59E0B',
            danger: '#EF4444',
            info: '#3B82F6'
        },
        animations: {
            duration: 300,
            easing: 'ease-in-out'
        },
        notifications: {
            position: 'top-right',
            duration: 5000,
            maxVisible: 5
        }
    },

    // Configuration de l'analyse des CVs
    cvAnalysis: {
        maxFileSize: 10 * 1024 * 1024, // 10 MB
        allowedTypes: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        maxFiles: 10,
        analysisTimeout: 30000 // 30 secondes
    },

    // Configuration des graphiques
    charts: {
        colors: {
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#10B981',
            warning: '#F59E0B',
            danger: '#EF4444'
        },
        defaults: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    },

    // Configuration des routes
    routes: {
        auth: '/auth',
        dashboard: '/dashboard',
        analysis: '/analysis',
        profile: '/profile',
        settings: '/settings'
    },

    // Configuration des API endpoints
    api: {
        login: '/api/login',
        logout: '/api/logout',
        analyze: '/api/analyze',
        results: '/api/results',
        profile: '/api/profile'
    }
};

// Exporter la configuration
window.AppConfig = AppConfig;

