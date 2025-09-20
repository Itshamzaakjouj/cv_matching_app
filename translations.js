// Système de traduction pour TalentScope
class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('talentscope_language') || 'fr';
        this.translations = {
            fr: {
                // Navigation
                'nav.home': 'Accueil',
                'nav.dashboard': 'Tableau de Bord',
                'nav.new_analysis': 'Nouvelle Analyse',
                'nav.processed_cvs': 'CVs Traités',
                'nav.configuration': 'Configuration',
                'nav.home_subtitle': 'Page principale',
                'nav.dashboard_subtitle': 'Vue d\'ensemble',
                'nav.analysis_subtitle': 'Analyser des CVs',
                'nav.cvs_subtitle': 'Historique des analyses',
                'nav.config_subtitle': 'Paramètres',

                // Authentication
                'auth.title': 'Connexion',
                'auth.subtitle': 'Accédez à votre espace d\'analyse',
                'auth.email': 'Email',
                'auth.password': 'Mot de passe',
                'auth.remember': 'Se souvenir de moi',
                'auth.login': 'Se connecter',
                'auth.register': 'S\'inscrire',
                'auth.forgot_password': 'Mot de passe oublié ?',
                'auth.or': 'ou',
                'auth.google': 'Continuer avec Google',
                'auth.microsoft': 'Continuer avec Microsoft',
                'auth.register_title': 'Créer un compte',
                'auth.register_subtitle': 'Rejoignez TalentScope',
                'auth.fullname': 'Nom complet',
                'auth.confirm_password': 'Confirmer le mot de passe',
                'auth.already_account': 'Déjà un compte ?',
                'auth.no_account': 'Pas encore de compte ?',

                // Dashboard
                'dashboard.welcome': 'Bienvenue dans TalentScope',
                'dashboard.subtitle': 'Votre plateforme d\'analyse de CVs alimentée par l\'IA',
                'dashboard.total_cvs': 'CVs Analysés',
                'dashboard.avg_score': 'Score Moyen',
                'dashboard.best_match': 'Meilleur Candidat',
                'dashboard.active_jobs': 'Postes Actifs',
                'dashboard.new_analysis': 'Nouvelle Analyse',
                'dashboard.view_history': 'Voir l\'Historique',
                'dashboard.export_data': 'Exporter les Données',
                'dashboard.recent_analysis': 'Analyses Récentes',
                'dashboard.candidate': 'Candidat',
                'dashboard.score': 'Score',
                'dashboard.status': 'Statut',
                'dashboard.date': 'Date',
                'dashboard.view_details': 'Voir Détails',
                'dashboard.usage_guide': 'Guide d\'Utilisation',
                'dashboard.ministry_info': 'À Propos du Ministère',
                'dashboard.clear_history': 'Supprimer l\'Historique',

                // Analysis
                'analysis.title': 'Nouvelle Analyse',
                'analysis.subtitle': 'Analyser des CVs avec l\'IA en 4 étapes simples',
                'analysis.step1': 'Offre d\'emploi',
                'analysis.step2': 'Importation CVs',
                'analysis.step3': 'Vérification',
                'analysis.step4': 'Résultats',
                'analysis.job_title': 'Titre du poste',
                'analysis.job_description': 'Description du poste',
                'analysis.job_skills': 'Compétences clés',
                'analysis.job_experience': 'Niveau d\'expérience',
                'analysis.job_title_placeholder': 'Ex: Data Scientist Senior',
                'analysis.job_description_placeholder': 'Décrivez les missions, responsabilités, compétences requises, expérience souhaitée...',
                'analysis.job_skills_placeholder': 'Ex: Python, Machine Learning, SQL, TensorFlow (séparées par des virgules)',
                'analysis.upload_cvs': 'Importation des CVs',
                'analysis.drag_drop': 'Glissez-déposez vos fichiers CV ici',
                'analysis.or_click': 'ou cliquez pour sélectionner',
                'analysis.supported_formats': 'Formats supportés: PDF, DOC, DOCX',
                'analysis.next': 'Suivant',
                'analysis.previous': 'Précédent',
                'analysis.start_analysis': 'Démarrer l\'Analyse',
                'analysis.results_title': 'Résultats de l\'analyse',
                'analysis.results_subtitle': 'Voici les résultats de l\'analyse de vos CVs. Les candidats sont classés par score de compatibilité.',
                'analysis.view_cv': 'Voir le CV',
                'analysis.details': 'Détails',
                'analysis.export_results': 'Exporter les résultats',
                'analysis.new_analysis': 'Nouvelle analyse',

                // Configuration
                'config.title': 'Paramètres',
                'config.theme': 'Thème',
                'config.theme_description': 'Choisissez le thème de l\'interface',
                'config.language': 'Langue',
                'config.language_description': 'Sélectionnez la langue de l\'interface',
                'config.notifications': 'Notifications',
                'config.notifications_description': 'Configurez vos préférences de notification',
                'config.email_notifications': 'Notifications par email',
                'config.push_notifications': 'Notifications push',
                'config.danger_zone': 'Zone de danger',
                'config.danger_description': 'Actions irréversibles - Procédez avec prudence',
                'config.clear_history': 'Supprimer l\'Historique',
                'config.reset_site': 'Réinitialiser le site',

                // Common
                'common.save': 'Enregistrer',
                'common.cancel': 'Annuler',
                'common.delete': 'Supprimer',
                'common.edit': 'Modifier',
                'common.view': 'Voir',
                'common.download': 'Télécharger',
                'common.upload': 'Importer',
                'common.search': 'Rechercher',
                'common.filter': 'Filtrer',
                'common.sort': 'Trier',
                'common.loading': 'Chargement...',
                'common.error': 'Erreur',
                'common.success': 'Succès',
                'common.warning': 'Attention',
                'common.info': 'Information',

                // Status
                'status.excellent': 'Excellent',
                'status.very_good': 'Très bon',
                'status.good': 'Bon',
                'status.to_improve': 'À améliorer',

                // Experience levels
                'exp.junior': 'Junior (0-2 ans)',
                'exp.intermediate': 'Intermédiaire (2-5 ans)',
                'exp.senior': 'Senior (5-10 ans)',
                'exp.expert': 'Expert (10+ ans)',

                // Profile
                'profile.administrator': 'Administrateur',
                'profile.ministry': 'Ministère des Finances',
                'profile.edit': 'Modifier le profil',
                'profile.change_password': 'Changer le mot de passe',
                'profile.settings': 'Paramètres',
                'profile.logout': 'Déconnexion',
                'profile.personal_info': 'Informations Personnelles',
                'profile.security': 'Sécurité',
                'profile.fullname': 'Nom complet',
                'profile.department': 'Département',
                'profile.position': 'Poste',
                'profile.phone': 'Téléphone',
                'profile.two_factor': 'Authentification à deux facteurs',
                'profile.sessions': 'Sessions actives',
                'profile.enable': 'Activer',
                'profile.manage': 'Gérer',
                'profile.delete_account': 'Supprimer le compte',

                // Themes
                'theme.light': 'Clair',
                'theme.dark': 'Sombre',
                'theme.auto': 'Automatique',

                // Languages
                'lang.fr': 'Français',
                'lang.en': 'English'
            },
            en: {
                // Navigation
                'nav.home': 'Home',
                'nav.dashboard': 'Dashboard',
                'nav.new_analysis': 'New Analysis',
                'nav.processed_cvs': 'Processed CVs',
                'nav.configuration': 'Configuration',
                'nav.home_subtitle': 'Main page',
                'nav.dashboard_subtitle': 'Overview',
                'nav.analysis_subtitle': 'Analyze CVs',
                'nav.cvs_subtitle': 'Analysis history',
                'nav.config_subtitle': 'Settings',

                // Authentication
                'auth.title': 'Login',
                'auth.subtitle': 'Access your analysis workspace',
                'auth.email': 'Email',
                'auth.password': 'Password',
                'auth.remember': 'Remember me',
                'auth.login': 'Login',
                'auth.register': 'Register',
                'auth.forgot_password': 'Forgot password?',
                'auth.or': 'or',
                'auth.google': 'Continue with Google',
                'auth.microsoft': 'Continue with Microsoft',
                'auth.register_title': 'Create Account',
                'auth.register_subtitle': 'Join TalentScope',
                'auth.fullname': 'Full name',
                'auth.confirm_password': 'Confirm password',
                'auth.already_account': 'Already have an account?',
                'auth.no_account': 'Don\'t have an account?',

                // Dashboard
                'dashboard.welcome': 'Welcome to TalentScope',
                'dashboard.subtitle': 'Your AI-powered CV analysis platform',
                'dashboard.total_cvs': 'CVs Analyzed',
                'dashboard.avg_score': 'Average Score',
                'dashboard.best_match': 'Best Candidate',
                'dashboard.active_jobs': 'Active Jobs',
                'dashboard.new_analysis': 'New Analysis',
                'dashboard.view_history': 'View History',
                'dashboard.export_data': 'Export Data',
                'dashboard.recent_analysis': 'Recent Analysis',
                'dashboard.candidate': 'Candidate',
                'dashboard.score': 'Score',
                'dashboard.status': 'Status',
                'dashboard.date': 'Date',
                'dashboard.view_details': 'View Details',
                'dashboard.usage_guide': 'Usage Guide',
                'dashboard.ministry_info': 'About the Ministry',
                'dashboard.clear_history': 'Clear History',

                // Analysis
                'analysis.title': 'New Analysis',
                'analysis.subtitle': 'Analyze CVs with AI in 4 simple steps',
                'analysis.step1': 'Job Offer',
                'analysis.step2': 'CV Import',
                'analysis.step3': 'Verification',
                'analysis.step4': 'Results',
                'analysis.job_title': 'Job title',
                'analysis.job_description': 'Job description',
                'analysis.job_skills': 'Key skills',
                'analysis.job_experience': 'Experience level',
                'analysis.job_title_placeholder': 'Ex: Senior Data Scientist',
                'analysis.job_description_placeholder': 'Describe missions, responsibilities, required skills, desired experience...',
                'analysis.job_skills_placeholder': 'Ex: Python, Machine Learning, SQL, TensorFlow (comma separated)',
                'analysis.upload_cvs': 'CV Upload',
                'analysis.drag_drop': 'Drag and drop your CV files here',
                'analysis.or_click': 'or click to select',
                'analysis.supported_formats': 'Supported formats: PDF, DOC, DOCX',
                'analysis.next': 'Next',
                'analysis.previous': 'Previous',
                'analysis.start_analysis': 'Start Analysis',
                'analysis.results_title': 'Analysis Results',
                'analysis.results_subtitle': 'Here are the results of your CV analysis. Candidates are ranked by compatibility score.',
                'analysis.view_cv': 'View CV',
                'analysis.details': 'Details',
                'analysis.export_results': 'Export results',
                'analysis.new_analysis': 'New analysis',

                // Configuration
                'config.title': 'Settings',
                'config.theme': 'Theme',
                'config.theme_description': 'Choose the interface theme',
                'config.language': 'Language',
                'config.language_description': 'Select the interface language',
                'config.notifications': 'Notifications',
                'config.notifications_description': 'Configure your notification preferences',
                'config.email_notifications': 'Email notifications',
                'config.push_notifications': 'Push notifications',
                'config.danger_zone': 'Danger Zone',
                'config.danger_description': 'Irreversible actions - Proceed with caution',
                'config.clear_history': 'Clear History',
                'config.reset_site': 'Reset Site',

                // Common
                'common.save': 'Save',
                'common.cancel': 'Cancel',
                'common.delete': 'Delete',
                'common.edit': 'Edit',
                'common.view': 'View',
                'common.download': 'Download',
                'common.upload': 'Upload',
                'common.search': 'Search',
                'common.filter': 'Filter',
                'common.sort': 'Sort',
                'common.loading': 'Loading...',
                'common.error': 'Error',
                'common.success': 'Success',
                'common.warning': 'Warning',
                'common.info': 'Information',

                // Status
                'status.excellent': 'Excellent',
                'status.very_good': 'Very Good',
                'status.good': 'Good',
                'status.to_improve': 'To Improve',

                // Experience levels
                'exp.junior': 'Junior (0-2 years)',
                'exp.intermediate': 'Intermediate (2-5 years)',
                'exp.senior': 'Senior (5-10 years)',
                'exp.expert': 'Expert (10+ years)',

                // Profile
                'profile.administrator': 'Administrator',
                'profile.ministry': 'Ministry of Finance',
                'profile.edit': 'Edit profile',
                'profile.change_password': 'Change password',
                'profile.settings': 'Settings',
                'profile.logout': 'Logout',
                'profile.personal_info': 'Personal Information',
                'profile.security': 'Security',
                'profile.fullname': 'Full name',
                'profile.department': 'Department',
                'profile.position': 'Position',
                'profile.phone': 'Phone',
                'profile.two_factor': 'Two-factor authentication',
                'profile.sessions': 'Active sessions',
                'profile.enable': 'Enable',
                'profile.manage': 'Manage',
                'profile.delete_account': 'Delete account',

                // Themes
                'theme.light': 'Light',
                'theme.dark': 'Dark',
                'theme.auto': 'Auto',

                // Languages
                'lang.fr': 'Français',
                'lang.en': 'English'
            }
        };
    }

    // Obtenir une traduction
    t(key, defaultValue = key) {
        const translation = this.translations[this.currentLanguage]?.[key];
        return translation || defaultValue;
    }

    // Changer la langue
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            localStorage.setItem('talentscope_language', lang);
            this.updatePageTranslations();
        }
    }

    // Obtenir la langue actuelle
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Mettre à jour toutes les traductions sur la page
    updatePageTranslations() {
        // Mettre à jour tous les éléments avec data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.type === 'submit' || element.type === 'button') {
                    element.value = translation;
                } else {
                    element.placeholder = translation;
                }
            } else {
                element.textContent = translation;
            }
        });

        // Mettre à jour les attributs title et aria-label
        document.querySelectorAll('[data-translate-title]').forEach(element => {
            const key = element.getAttribute('data-translate-title');
            element.title = this.t(key);
        });

        document.querySelectorAll('[data-translate-aria]').forEach(element => {
            const key = element.getAttribute('data-translate-aria');
            element.setAttribute('aria-label', this.t(key));
        });

        // Déclencher un événement personnalisé pour informer les autres composants
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: this.currentLanguage }
        }));
    }

    // Initialiser les traductions au chargement de la page
    init() {
        this.updatePageTranslations();
        
        // Écouter les changements de langue
        document.addEventListener('change', (e) => {
            if (e.target.id === 'language-select') {
                this.setLanguage(e.target.value);
            }
        });
    }
}

// Gestionnaire de thèmes
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('talentscope_theme') || 'light';
        this.init();
    }

    // Appliquer un thème
    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('talentscope_theme', theme);
        this.applyTheme();
    }

    // Obtenir le thème actuel
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Appliquer le thème à la page
    applyTheme() {
        document.body.setAttribute('data-theme', this.currentTheme);
        
        // Mettre à jour l'icône du bouton de thème
        const themeButton = document.getElementById('theme-toggle');
        if (themeButton) {
            themeButton.innerHTML = this.currentTheme === 'dark' ? '☀️' : '🌙';
        }

        // Déclencher un événement personnalisé
        window.dispatchEvent(new CustomEvent('themeChanged', {
            detail: { theme: this.currentTheme }
        }));
    }

    // Basculer entre les thèmes
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    // Initialiser le gestionnaire de thèmes
    init() {
        this.applyTheme();
        
        // Écouter les changements de thème
        document.addEventListener('change', (e) => {
            if (e.target.id === 'theme-select') {
                this.setTheme(e.target.value);
            }
        });

        document.addEventListener('click', (e) => {
            if (e.target.id === 'theme-toggle') {
                this.toggleTheme();
            }
        });
    }
}

// Instances globales
window.translationManager = new TranslationManager();
window.themeManager = new ThemeManager();

// Initialiser au chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
    if (window.translationManager) {
        window.translationManager.init();
    }
    if (window.themeManager) {
        window.themeManager.init();
    }
});

// S'assurer que les classes sont disponibles globalement
if (typeof window !== 'undefined') {
    window.TranslationManager = TranslationManager;
    window.ThemeManager = ThemeManager;
}
