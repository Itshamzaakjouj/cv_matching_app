// Système de traduction complet avec animations
const TranslationSystem = {
    // Dictionnaire des traductions
    translations: {
        fr: {
            // Page d'authentification
            'app-title': 'TalentScope',
            'ministry-name': 'Ministère de l\'Économie et des Finances',
            'platform-description': 'Plateforme de gestion des talents',
            'email-label': 'Adresse mail',
            'email-placeholder': 'Entrez votre adresse e-mail',
            'password-label': 'Mot de passe',
            'password-placeholder': 'Entrez votre mot de passe',
            'login-button': 'Se connecter',
            'forgot-password': 'Mot de passe oublié ?',
            'register-tab': 'Inscription',
            'login-tab': 'Connexion',
            'register-button': 'S\'inscrire',
            'access-request-button': 'Demander l\'accès',
            'ministry-sso': 'Ministère',
            'name-label': 'Nom complet',
            'name-placeholder': 'Entrez votre nom complet',
            'confirm-password-label': 'Confirmer le mot de passe',
            'confirm-password-placeholder': 'Confirmez votre mot de passe',
            'department-label': 'Département',
            'department-placeholder': 'Sélectionnez votre département',
            'position-label': 'Poste',
            'position-placeholder': 'Entrez votre poste',
            
            // Dashboard
            'dashboard-title': 'Tableau de bord',
            'welcome-message': 'Bienvenue sur TalentScope',
            'analytics-section': 'Analyses',
            'cv-management': 'Gestion des CV',
            'profile-settings': 'Paramètres du profil',
            'logout': 'Déconnexion',
            'total-cvs': 'Total des CV',
            'pending-reviews': 'Examens en attente',
            'matches-found': 'Correspondances trouvées',
            'success-rate': 'Taux de réussite',
            
            // Analyse
            'analysis-title': 'Analyse des CV',
            'upload-cv': 'Télécharger un CV',
            'job-description': 'Description du poste',
            'analyze-button': 'Analyser',
            'results-section': 'Résultats de l\'analyse',
            'compatibility-score': 'Score de compatibilité',
            'skills-match': 'Correspondance des compétences',
            'experience-match': 'Correspondance de l\'expérience',
            'recommendations': 'Recommandations',
            
            // Navigation
            'home': 'Accueil',
            'analysis': 'Analyse',
            'comparison': 'Comparaison',
            'settings': 'Paramètres',
            
            // Messages système
            'loading': 'Chargement...',
            'error': 'Erreur',
            'success': 'Succès',
            'processing': 'Traitement en cours...',
            
            // Langue
            'language': 'Langue',
            'french': 'Français',
            'english': 'English'
        },
        en: {
            // Authentication page
            'app-title': 'TalentScope',
            'ministry-name': 'Ministry of Economy and Finance',
            'platform-description': 'Talent Management Platform',
            'email-label': 'Email Address',
            'email-placeholder': 'Enter your email address',
            'password-label': 'Password',
            'password-placeholder': 'Enter your password',
            'login-button': 'Sign In',
            'forgot-password': 'Forgot password?',
            'register-tab': 'Register',
            'login-tab': 'Login',
            'register-button': 'Register',
            'access-request-button': 'Request Access',
            'ministry-sso': 'Ministry',
            'name-label': 'Full Name',
            'name-placeholder': 'Enter your full name',
            'confirm-password-label': 'Confirm Password',
            'confirm-password-placeholder': 'Confirm your password',
            'department-label': 'Department',
            'department-placeholder': 'Select your department',
            'position-label': 'Position',
            'position-placeholder': 'Enter your position',
            
            // Dashboard
            'dashboard-title': 'Dashboard',
            'welcome-message': 'Welcome to TalentScope',
            'analytics-section': 'Analytics',
            'cv-management': 'CV Management',
            'profile-settings': 'Profile Settings',
            'logout': 'Logout',
            'total-cvs': 'Total CVs',
            'pending-reviews': 'Pending Reviews',
            'matches-found': 'Matches Found',
            'success-rate': 'Success Rate',
            
            // Analysis
            'analysis-title': 'CV Analysis',
            'upload-cv': 'Upload CV',
            'job-description': 'Job Description',
            'analyze-button': 'Analyze',
            'results-section': 'Analysis Results',
            'compatibility-score': 'Compatibility Score',
            'skills-match': 'Skills Match',
            'experience-match': 'Experience Match',
            'recommendations': 'Recommendations',
            
            // Navigation
            'home': 'Home',
            'analysis': 'Analysis',
            'comparison': 'Comparison',
            'settings': 'Settings',
            
            // System messages
            'loading': 'Loading...',
            'error': 'Error',
            'success': 'Success',
            'processing': 'Processing...',
            
            // Language
            'language': 'Language',
            'french': 'Français',
            'english': 'English'
        }
    },

    currentLang: 'fr',
    isTransitioning: false,

    // Initialisation
    init() {
        this.currentLang = localStorage.getItem('selectedLanguage') || 'fr';
        this.setupLanguageSelector();
        this.translatePage();
        this.addTransitionStyles();
    },

    // Ajouter les styles CSS pour les transitions
    addTransitionStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .translation-fade {
                opacity: 0;
                transition: opacity 0.3s ease-in-out;
            }
            
            .translation-fade.active {
                opacity: 1;
            }
            
            .language-switching {
                pointer-events: none;
            }
            
            .translate-element {
                transition: opacity 0.2s ease-in-out;
            }
            
            .translate-element.fading {
                opacity: 0.3;
            }
            
            @keyframes languageSwitch {
                0% { transform: scale(1); opacity: 1; }
                50% { transform: scale(0.95); opacity: 0.7; }
                100% { transform: scale(1); opacity: 1; }
            }
            
            .language-animation {
                animation: languageSwitch 0.5s ease-in-out;
            }
        `;
        document.head.appendChild(style);
    },

    // Configuration du sélecteur de langue
    setupLanguageSelector() {
        const languageSelectors = document.querySelectorAll('#languageSelector, .language-selector select');
        
        languageSelectors.forEach(selector => {
            if (selector) {
                selector.value = this.currentLang;
                selector.addEventListener('change', (e) => {
                    this.changeLanguage(e.target.value);
                });
            }
        });
    },

    // Changement de langue avec animation
    async changeLanguage(newLang) {
        if (this.isTransitioning || newLang === this.currentLang) return;
        
        this.isTransitioning = true;
        const body = document.body;
        
        // Ajouter classe d'animation
        body.classList.add('language-switching');
        
        // Faire disparaître les éléments en fondu
        const elementsToTranslate = document.querySelectorAll('[data-translate], [data-translate-placeholder], [data-translate-title]');
        elementsToTranslate.forEach(el => {
            el.classList.add('translate-element', 'fading');
        });
        
        // Attendre la fin de l'animation de fondu
        await this.delay(200);
        
        // Changer la langue
        this.currentLang = newLang;
        localStorage.setItem('selectedLanguage', newLang);
        
        // Appliquer les traductions
        this.translatePage();
        
        // Faire réapparaître les éléments
        elementsToTranslate.forEach(el => {
            el.classList.remove('fading');
        });
        
        // Animation globale de la page
        body.classList.add('language-animation');
        
        // Attendre la fin des animations
        await this.delay(500);
        
        // Nettoyer les classes
        body.classList.remove('language-switching', 'language-animation');
        elementsToTranslate.forEach(el => {
            el.classList.remove('translate-element');
        });
        
        this.isTransitioning = false;
        
        // Mettre à jour les sélecteurs de langue
        this.updateLanguageSelectors();
        
        console.log(`Language changed to: ${newLang}`);
    },

    // Traduire toute la page
    translatePage() {
        const translations = this.translations[this.currentLang];
        if (!translations) return;

        // Traduire les éléments avec data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (translations[key]) {
                element.textContent = translations[key];
            }
        });

        // Traduire les placeholders
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            if (translations[key]) {
                element.placeholder = translations[key];
            }
        });

        // Traduire les titres
        document.querySelectorAll('[data-translate-title]').forEach(element => {
            const key = element.getAttribute('data-translate-title');
            if (translations[key]) {
                element.title = translations[key];
            }
        });

        // Traduire les options de sélect
        document.querySelectorAll('select[data-translate-options] option').forEach(option => {
            const key = option.getAttribute('data-translate');
            if (key && translations[key]) {
                option.textContent = translations[key];
            }
        });

        // Mettre à jour le titre de la page
        if (translations['app-title']) {
            document.title = translations['app-title'];
        }
    },

    // Mettre à jour tous les sélecteurs de langue
    updateLanguageSelectors() {
        const selectors = document.querySelectorAll('#languageSelector, .language-selector select');
        selectors.forEach(selector => {
            if (selector && selector.value !== this.currentLang) {
                selector.value = this.currentLang;
            }
        });
    },

    // Utilitaire pour les délais
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    // Obtenir la langue actuelle
    getCurrentLanguage() {
        return this.currentLang;
    },

    // Obtenir une traduction spécifique
    getTranslation(key) {
        return this.translations[this.currentLang][key] || key;
    }
};

// Initialisation automatique quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    TranslationSystem.init();
});

// Export pour utilisation dans d'autres scripts
window.TranslationSystem = TranslationSystem;
