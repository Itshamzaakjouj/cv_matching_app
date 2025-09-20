/**
 * Gestionnaire de traductions utilisant un fichier JSON
 */
class TranslationManager {
    constructor() {
        this.translations = null;
        this.currentLanguage = localStorage.getItem('selectedLanguage') || 'fr';
        this.init();
    }

    async init() {
        try {
            // Charger les traductions depuis le fichier JSON
            const response = await fetch('translations.json');
            this.translations = await response.json();
            
            // Appliquer la langue actuelle
            this.applyLanguage(this.currentLanguage);
            
            console.log('TranslationManager initialized with language:', this.currentLanguage);
        } catch (error) {
            console.error('Error loading translations:', error);
            // Fallback vers les traductions intégrées
            this.loadFallbackTranslations();
        }
    }

    loadFallbackTranslations() {
        // Traductions de fallback intégrées
        this.translations = {
            fr: {
                nav: {
                    home: "Accueil",
                    home_subtitle: "Page principale",
                    dashboard: "Tableau de Bord",
                    dashboard_subtitle: "Vue d'ensemble",
                    new_analysis: "Nouvelle Analyse",
                    analysis_subtitle: "Analyser des CVs",
                    processed_cvs: "CVs Traités",
                    cvs_subtitle: "Historique des analyses",
                    configuration: "Configuration",
                    config_subtitle: "Paramètres"
                },
                auth: {
                    login: "Connexion",
                    register: "S'inscrire",
                    email: "Email",
                    password: "Mot de passe",
                    confirm_password: "Confirmer le mot de passe",
                    forgot_password: "Mot de passe oublié ?",
                    remember_me: "Se souvenir de moi",
                    login_button: "Se connecter",
                    register_button: "Créer un compte",
                    social_login: "Ou continuer avec",
                    no_account: "Pas de compte ?",
                    has_account: "Déjà un compte ?",
                    sign_up: "S'inscrire",
                    sign_in: "Se connecter"
                },
                dashboard: {
                    title: "Tableau de Bord",
                    subtitle: "Vue d'ensemble de vos analyses et statistiques",
                    analyses_performed: "Analyses Effectuées",
                    processed_cvs: "CVs Traités",
                    average_score: "Score Moyen",
                    success_rate: "Taux de Réussite",
                    this_week: "cette semaine",
                    analysis_trend: "Tendance des Analyses",
                    score_distribution: "Distribution des Scores",
                    quick_actions: "Actions Rapides",
                    new_analysis: "Nouvelle Analyse",
                    view_history: "Voir l'historique",
                    export_data: "Exporter les données",
                    recent_analyses: "Analyses Récentes",
                    no_analyses: "Aucune analyse récente",
                    view_all: "Voir tout"
                },
                profile: {
                    administrator: "Administrateur",
                    ministry: "Ministère des Finances",
                    edit: "Modifier le profil",
                    change_password: "Changer le mot de passe",
                    settings: "Paramètres",
                    logout: "Déconnexion",
                    personal_info: "Informations Personnelles",
                    security: "Sécurité",
                    fullname: "Nom complet",
                    department: "Département",
                    position: "Poste",
                    phone: "Téléphone",
                    two_factor: "Authentification à deux facteurs",
                    sessions: "Sessions actives",
                    enable: "Activer",
                    manage: "Gérer",
                    delete_account: "Supprimer le compte"
                },
                common: {
                    save: "Enregistrer",
                    cancel: "Annuler",
                    delete: "Supprimer",
                    edit: "Modifier",
                    close: "Fermer",
                    confirm: "Confirmer",
                    loading: "Chargement...",
                    error: "Erreur",
                    success: "Succès",
                    warning: "Attention",
                    info: "Information"
                },
                themes: {
                    light: "Clair",
                    dark: "Sombre",
                    auto: "Automatique"
                }
            },
            en: {
                nav: {
                    home: "Home",
                    home_subtitle: "Main page",
                    dashboard: "Dashboard",
                    dashboard_subtitle: "Overview",
                    new_analysis: "New Analysis",
                    analysis_subtitle: "Analyze CVs",
                    processed_cvs: "Processed CVs",
                    cvs_subtitle: "Analysis history",
                    configuration: "Configuration",
                    config_subtitle: "Settings"
                },
                auth: {
                    login: "Login",
                    register: "Register",
                    email: "Email",
                    password: "Password",
                    confirm_password: "Confirm password",
                    forgot_password: "Forgot password?",
                    remember_me: "Remember me",
                    login_button: "Sign in",
                    register_button: "Create account",
                    social_login: "Or continue with",
                    no_account: "No account?",
                    has_account: "Already have an account?",
                    sign_up: "Sign up",
                    sign_in: "Sign in"
                },
                dashboard: {
                    title: "Dashboard",
                    subtitle: "Overview of your analyses and statistics",
                    analyses_performed: "Analyses Performed",
                    processed_cvs: "Processed CVs",
                    average_score: "Average Score",
                    success_rate: "Success Rate",
                    this_week: "this week",
                    analysis_trend: "Analysis Trend",
                    score_distribution: "Score Distribution",
                    quick_actions: "Quick Actions",
                    new_analysis: "New Analysis",
                    view_history: "View history",
                    export_data: "Export data",
                    recent_analyses: "Recent Analyses",
                    no_analyses: "No recent analyses",
                    view_all: "View all"
                },
                profile: {
                    administrator: "Administrator",
                    ministry: "Ministry of Finance",
                    edit: "Edit profile",
                    change_password: "Change password",
                    settings: "Settings",
                    logout: "Logout",
                    personal_info: "Personal Information",
                    security: "Security",
                    fullname: "Full name",
                    department: "Department",
                    position: "Position",
                    phone: "Phone",
                    two_factor: "Two-factor authentication",
                    sessions: "Active sessions",
                    enable: "Enable",
                    manage: "Manage",
                    delete_account: "Delete account"
                },
                common: {
                    save: "Save",
                    cancel: "Cancel",
                    delete: "Delete",
                    edit: "Edit",
                    close: "Close",
                    confirm: "Confirm",
                    loading: "Loading...",
                    error: "Error",
                    success: "Success",
                    warning: "Warning",
                    info: "Information"
                },
                themes: {
                    light: "Light",
                    dark: "Dark",
                    auto: "Auto"
                }
            }
        };
        
        this.applyLanguage(this.currentLanguage);
    }

    /**
     * Obtenir une traduction
     * @param {string} key - Clé de traduction (ex: "nav.home")
     * @param {string} language - Langue (optionnel, utilise la langue actuelle par défaut)
     * @returns {string} - Texte traduit
     */
    translate(key, language = null) {
        const lang = language || this.currentLanguage;
        
        if (!this.translations || !this.translations[lang]) {
            console.warn(`Language ${lang} not found`);
            return key;
        }

        const keys = key.split('.');
        let translation = this.translations[lang];
        
        for (const k of keys) {
            if (translation && translation[k]) {
                translation = translation[k];
            } else {
                console.warn(`Translation key ${key} not found for language ${lang}`);
                return key;
            }
        }
        
        return translation;
    }

    /**
     * Changer la langue
     * @param {string} language - Code de langue (fr, en)
     */
    changeLanguage(language) {
        console.log(`Attempting to change language to: ${language}`);
        
        if (!this.translations) {
            console.error('Translations not loaded yet');
            return;
        }
        
        if (!this.translations[language]) {
            console.error(`Language ${language} not available`);
            return;
        }

        this.currentLanguage = language;
        localStorage.setItem('selectedLanguage', language);
        
        // Appliquer la langue immédiatement
        this.applyLanguage(language);
        
        console.log(`Language changed to: ${language}`);
    }

    /**
     * Appliquer la langue à tous les éléments avec data-translate
     * @param {string} language - Code de langue
     */
    applyLanguage(language) {
        if (!this.translations || !this.translations[language]) {
            console.warn(`Language ${language} not found in translations`);
            return;
        }

        console.log(`Applying language: ${language}`);

        // Mettre à jour tous les éléments avec data-translate
        const elements = document.querySelectorAll('[data-translate]');
        console.log(`Found ${elements.length} elements with data-translate`);
        
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.translate(key, language);
            
            if (translation && translation !== key) {
                element.textContent = translation;
                console.log(`Translated ${key} to ${translation}`);
            }
        });

        // Mettre à jour les placeholders
        const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            const translation = this.translate(key, language);
            
            if (translation && translation !== key) {
                element.placeholder = translation;
            }
        });

        // Mettre à jour les titres
        const titleElements = document.querySelectorAll('[data-translate-title]');
        titleElements.forEach(element => {
            const key = element.getAttribute('data-translate-title');
            const translation = this.translate(key, language);
            
            if (translation && translation !== key) {
                element.title = translation;
            }
        });

        // Mettre à jour les valeurs des options
        const optionElements = document.querySelectorAll('[data-translate-value]');
        optionElements.forEach(element => {
            const key = element.getAttribute('data-translate-value');
            const translation = this.translate(key, language);
            
            if (translation && translation !== key) {
                element.value = translation;
            }
        });

        // Mettre à jour les sélecteurs de langue
        this.updateLanguageSelectors(language);
        
        // Mettre à jour l'attribut lang du document
        document.documentElement.lang = language;
    }

    /**
     * Mettre à jour les sélecteurs de langue
     * @param {string} language - Code de langue
     */
    updateLanguageSelectors(language) {
        const languageSelects = document.querySelectorAll('#language-select, .language-selector select');
        languageSelects.forEach(select => {
            select.value = language;
        });
    }

    /**
     * Obtenir la langue actuelle
     * @returns {string} - Code de langue actuel
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    /**
     * Obtenir la liste des langues disponibles
     * @returns {string[]} - Liste des codes de langue
     */
    getAvailableLanguages() {
        return this.translations ? Object.keys(this.translations) : [];
    }
}

// Gestionnaire de thème (inchangé)
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('selectedTheme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
    }

    changeTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('selectedTheme', theme);
        this.applyTheme(theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        // Mettre à jour les sélecteurs de thème
        const themeSelects = document.querySelectorAll('#theme-select, .theme-selector select');
        themeSelects.forEach(select => {
            select.value = theme;
        });

        // Mettre à jour l'icône du toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
                this.changeTheme(newTheme);
            });
        }
    }

    getCurrentTheme() {
        return this.currentTheme;
    }
}

// Initialisation globale
let translationManager;
let themeManager;

document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les gestionnaires
    translationManager = new TranslationManager();
    themeManager = new ThemeManager();
    
    // Rendre les gestionnaires disponibles globalement
    window.translationManager = translationManager;
    window.themeManager = themeManager;
    
    // Fonctions de compatibilité
    window.handleLanguageChange = function(selectElement) {
        const language = selectElement.value;
        console.log('handleLanguageChange called with:', language);
        
        if (translationManager) {
            translationManager.changeLanguage(language);
        } else {
            console.error('TranslationManager not available');
        }
    };
    
    window.handleThemeChange = function(selectElement) {
        const theme = selectElement.value;
        if (themeManager) {
            themeManager.changeTheme(theme);
        }
    };
});
