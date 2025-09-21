// Système de traduction global
const translations = {
    fr: {
        // Navigation
        'nav.home': 'Accueil',
        'nav.dashboard': 'Tableau de Bord',
        'nav.new_analysis': 'Nouvelle Analyse',
        'nav.treated_cvs': 'CVs Traités',
        'nav.settings': 'Configuration',
        'nav.home.subtitle': 'Page principale',
        'nav.dashboard.subtitle': 'Vue d\'ensemble',
        'nav.new_analysis.subtitle': 'Analyser des CVs',
        'nav.treated_cvs.subtitle': 'Historique des analyses',
        'nav.settings.subtitle': 'Paramètres',

        // Paramètres
        'settings.title': 'Paramètres',
        'settings.app_settings': 'Paramètres de l\'application',
        'settings.theme': 'Thème',
        'settings.theme.description': 'Choisissez le thème de l\'interface',
        'settings.theme.light': 'Clair',
        'settings.theme.dark': 'Sombre',
        'settings.language': 'Langue',
        'settings.language.description': 'Sélectionnez la langue de l\'interface',
        'settings.notifications': 'Notifications',
        'settings.notifications.description': 'Configurez vos préférences de notification',
        'settings.notifications.email': 'Notifications par email',
        'settings.notifications.push': 'Notifications push',
        'settings.danger_zone': 'Zone de danger',
        'settings.danger_zone.warning': 'Actions irréversibles - Procédez avec prudence',

        // Titres principaux
        'app.title': 'TalentScope',
        'app.subtitle': 'Ministère de l\'Économie et des Finances',
        'app.platform': 'Plateforme de gestion des talents',

        // Messages généraux
        'general.loading': 'Chargement...',
        'general.error': 'Une erreur est survenue',
        'general.success': 'Opération réussie',
        'general.save': 'Enregistrer',
        'general.cancel': 'Annuler',
        'general.delete': 'Supprimer',
        'general.edit': 'Modifier',
        'general.search': 'Rechercher',
    },
    en: {
        // Navigation
        'nav.home': 'Home',
        'nav.dashboard': 'Dashboard',
        'nav.new_analysis': 'New Analysis',
        'nav.treated_cvs': 'Processed CVs',
        'nav.settings': 'Settings',
        'nav.home.subtitle': 'Main page',
        'nav.dashboard.subtitle': 'Overview',
        'nav.new_analysis.subtitle': 'Analyze CVs',
        'nav.treated_cvs.subtitle': 'Analysis history',
        'nav.settings.subtitle': 'Settings',

        // Settings
        'settings.title': 'Settings',
        'settings.app_settings': 'Application Settings',
        'settings.theme': 'Theme',
        'settings.theme.description': 'Choose interface theme',
        'settings.theme.light': 'Light',
        'settings.theme.dark': 'Dark',
        'settings.language': 'Language',
        'settings.language.description': 'Select interface language',
        'settings.notifications': 'Notifications',
        'settings.notifications.description': 'Configure your notification preferences',
        'settings.notifications.email': 'Email notifications',
        'settings.notifications.push': 'Push notifications',
        'settings.danger_zone': 'Danger Zone',
        'settings.danger_zone.warning': 'Irreversible actions - Proceed with caution',

        // Main titles
        'app.title': 'TalentScope',
        'app.subtitle': 'Ministry of Economy and Finance',
        'app.platform': 'Talent Management Platform',

        // General messages
        'general.loading': 'Loading...',
        'general.error': 'An error occurred',
        'general.success': 'Operation successful',
        'general.save': 'Save',
        'general.cancel': 'Cancel',
        'general.delete': 'Delete',
        'general.edit': 'Edit',
        'general.search': 'Search',
    }
};

// Gestionnaire de traduction global
class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('language') || 'fr';
        this.translations = translations;
    }

    // Initialiser la traduction
    init() {
        this.updateLanguageSelector();
        this.translatePage();
        this.setupLanguageChangeListener();
    }

    // Mettre à jour le sélecteur de langue
    updateLanguageSelector() {
        const languageSelect = document.querySelector('select[data-translation-select]');
        if (languageSelect) {
            languageSelect.value = this.currentLanguage;
        }
    }

    // Configurer l'écouteur de changement de langue
    setupLanguageChangeListener() {
        const languageSelect = document.querySelector('select[data-translation-select]');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.setLanguage(e.target.value);
            });
        }
    }

    // Définir la langue
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            localStorage.setItem('language', lang);
            this.translatePage();
            this.animateTransition();
        }
    }

    // Traduire la page
    translatePage() {
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (this.translations[this.currentLanguage] && this.translations[this.currentLanguage][key]) {
                element.textContent = this.translations[this.currentLanguage][key];
            }
        });
    }

    // Obtenir une traduction
    translate(key) {
        return this.translations[this.currentLanguage]?.[key] || key;
    }

    // Animation de transition
    animateTransition() {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 300);
        }

        // Effet sur le sélecteur de langue
        const languageSelector = document.querySelector('.language-selector');
        if (languageSelector) {
            languageSelector.classList.add('language-change');
            setTimeout(() => {
                languageSelector.classList.remove('language-change');
            }, 500);
        }
    }
}

// Créer et exporter l'instance du gestionnaire de traduction
window.translationManager = new TranslationManager();

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.translationManager.init();
});