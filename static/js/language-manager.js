// Définition des traductions
const APP_TRANSLATIONS = {
    fr: {
        // Navigation
        'nav.home': 'Accueil',
        'nav.home.subtitle': 'Page principale',
        'nav.dashboard': 'Tableau de Bord',
        'nav.dashboard.subtitle': 'Vue d\'ensemble',
        'nav.new_analysis': 'Nouvelle Analyse',
        'nav.new_analysis.subtitle': 'Analyser des CVs',
        'nav.treated_cvs': 'CVs Traités',
        'nav.treated_cvs.subtitle': 'Historique des analyses',
        'nav.settings': 'Configuration',
        'nav.settings.subtitle': 'Paramètres',
        'nav.title': 'NAVIGATION',

        // Titres et sous-titres
        'app.name': 'TalentScope',
        'app.ministry': 'Ministère de l\'Économie et des Finances',
        'app.subtitle': 'Plateforme de gestion des talents',

        // Page Paramètres
        'settings.title': 'Configuration',
        'settings.subtitle': 'Paramètres de l\'application',
        'settings.parameters': 'Paramètres',
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
    },
    en: {
        // Navigation
        'nav.home': 'Home',
        'nav.home.subtitle': 'Main page',
        'nav.dashboard': 'Dashboard',
        'nav.dashboard.subtitle': 'Overview',
        'nav.new_analysis': 'New Analysis',
        'nav.new_analysis.subtitle': 'Analyze CVs',
        'nav.treated_cvs': 'Processed CVs',
        'nav.treated_cvs.subtitle': 'Analysis history',
        'nav.settings': 'Settings',
        'nav.settings.subtitle': 'Parameters',
        'nav.title': 'NAVIGATION',

        // Titles and subtitles
        'app.name': 'TalentScope',
        'app.ministry': 'Ministry of Economy and Finance',
        'app.subtitle': 'Talent Management Platform',

        // Settings Page
        'settings.title': 'Settings',
        'settings.subtitle': 'Application Settings',
        'settings.parameters': 'Parameters',
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
    }
};

class LanguageManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('app_language') || 'fr';
        this.translations = APP_TRANSLATIONS;
        this.init();
    }

    init() {
        // Appliquer la langue initiale
        this.applyLanguage(this.currentLanguage);
        
        // Configurer les écouteurs d'événements
        document.addEventListener('DOMContentLoaded', () => {
            this.setupLanguageSelector();
            this.translatePage();
        });
    }

    setupLanguageSelector() {
        const languageSelect = document.querySelector('select[name="langue"]');
        if (languageSelect) {
            // Définir la valeur initiale
            languageSelect.value = this.currentLanguage;
            
            // Ajouter l'écouteur d'événements
            languageSelect.addEventListener('change', (e) => {
                this.applyLanguage(e.target.value);
            });
        }
    }

    applyLanguage(lang) {
        if (this.translations[lang]) {
            // Sauvegarder la langue
            this.currentLanguage = lang;
            localStorage.setItem('app_language', lang);
            
            // Appliquer les traductions avec animation
            this.animateTransition(() => {
                this.translatePage();
                this.updateMetadata();
            });
        }
    }

    translatePage() {
        // Traduire tous les éléments avec data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        });

        // Traduire les éléments spécifiques
        this.translateSpecificElements();
    }

    translateSpecificElements() {
        // Navigation
        document.querySelector('.nav-title')?.textContent = this.getTranslation('nav.title');
        
        // En-tête de l'application
        document.querySelector('.app-name')?.textContent = this.getTranslation('app.name');
        document.querySelector('.ministry-name')?.textContent = this.getTranslation('app.ministry');
        document.querySelector('.platform-subtitle')?.textContent = this.getTranslation('app.subtitle');

        // Page des paramètres
        if (window.location.pathname.includes('settings')) {
            this.translateSettingsPage();
        }
    }

    translateSettingsPage() {
        // Titres
        document.querySelector('.settings-title')?.textContent = this.getTranslation('settings.title');
        document.querySelector('.settings-subtitle')?.textContent = this.getTranslation('settings.subtitle');

        // Options de thème
        const themeSelect = document.querySelector('select[name="theme"]');
        if (themeSelect) {
            themeSelect.options[0].textContent = this.getTranslation('settings.theme.light');
            themeSelect.options[1].textContent = this.getTranslation('settings.theme.dark');
        }

        // Descriptions
        document.querySelectorAll('.setting-description').forEach(desc => {
            const key = desc.getAttribute('data-setting-key');
            if (key) {
                desc.textContent = this.getTranslation(key);
            }
        });
    }

    getTranslation(key) {
        return this.translations[this.currentLanguage]?.[key] || key;
    }

    updateMetadata() {
        // Mettre à jour l'attribut lang de la page
        document.documentElement.lang = this.currentLanguage;
    }

    animateTransition(callback) {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            // Animation de sortie
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(-10px)';

            setTimeout(() => {
                // Exécuter les changements
                callback();

                // Animation d'entrée
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 200);
        } else {
            callback();
        }
    }
}

// Créer et exporter l'instance
window.languageManager = new LanguageManager();
