const appTranslations = {
    fr: {
        // Navigation
        'navigation.title': 'NAVIGATION',
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

        // En-têtes
        'header.app_name': 'TalentScope',
        'header.ministry': 'Ministère de l\'Économie et des Finances',
        'header.platform': 'Plateforme de gestion des talents',

        // Page Paramètres
        'settings.title': 'Paramètres',
        'settings.app_settings': 'Paramètres de l\'application',
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
        'settings.danger_zone': 'Zone de danger',
        'settings.danger_zone.warning': 'Actions irréversibles - Procédez avec prudence',

        // Messages communs
        'common.loading': 'Chargement...',
        'common.save': 'Enregistrer',
        'common.cancel': 'Annuler',
        'common.delete': 'Supprimer',
        'common.edit': 'Modifier',
        'common.success': 'Opération réussie',
        'common.error': 'Une erreur est survenue',
    },
    en: {
        // Navigation
        'navigation.title': 'NAVIGATION',
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

        // Headers
        'header.app_name': 'TalentScope',
        'header.ministry': 'Ministry of Economy and Finance',
        'header.platform': 'Talent Management Platform',

        // Settings Page
        'settings.title': 'Settings',
        'settings.app_settings': 'Application Settings',
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
        'settings.danger_zone': 'Danger Zone',
        'settings.danger_zone.warning': 'Irreversible actions - Proceed with caution',

        // Common messages
        'common.loading': 'Loading...',
        'common.save': 'Save',
        'common.cancel': 'Cancel',
        'common.delete': 'Delete',
        'common.edit': 'Edit',
        'common.success': 'Operation successful',
        'common.error': 'An error occurred',
    }
};

class TranslationManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('app_language') || 'fr';
        this.translations = appTranslations;
        this.observers = [];
    }

    init() {
        // Appliquer la traduction initiale
        this.translatePage();
        
        // Configurer les écouteurs d'événements
        this.setupEventListeners();
        
        // Mettre à jour l'interface
        this.updateUI();
    }

    setupEventListeners() {
        // Écouter les changements de langue
        document.addEventListener('DOMContentLoaded', () => {
            const languageSelectors = document.querySelectorAll('select[data-language-selector]');
            languageSelectors.forEach(selector => {
                selector.value = this.currentLanguage;
                selector.addEventListener('change', (e) => {
                    this.setLanguage(e.target.value);
                });
            });
        });
    }

    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            localStorage.setItem('app_language', lang);
            
            // Animer la transition
            this.animateTransition(() => {
                this.translatePage();
                this.updateUI();
                this.notifyObservers();
            });
        }
    }

    translatePage() {
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            if (this.translations[this.currentLanguage]?.[key]) {
                element.textContent = this.translations[this.currentLanguage][key];
            }
        });
    }

    updateUI() {
        // Mettre à jour les sélecteurs de langue
        document.querySelectorAll('select[data-language-selector]').forEach(selector => {
            selector.value = this.currentLanguage;
        });

        // Mettre à jour l'attribut lang de la page
        document.documentElement.lang = this.currentLanguage;
    }

    animateTransition(callback) {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            // Animation de sortie
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                // Exécuter le callback (traduction)
                callback();

                // Animation d'entrée
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }, 300);
        } else {
            callback();
        }

        // Animer le sélecteur de langue
        const languageSelectors = document.querySelectorAll('select[data-language-selector]');
        languageSelectors.forEach(selector => {
            selector.classList.add('language-change');
            setTimeout(() => {
                selector.classList.remove('language-change');
            }, 500);
        });
    }

    // Observer Pattern pour les mises à jour externes
    addObserver(callback) {
        this.observers.push(callback);
    }

    notifyObservers() {
        this.observers.forEach(callback => callback(this.currentLanguage));
    }

    // Méthode utilitaire pour obtenir une traduction
    translate(key) {
        return this.translations[this.currentLanguage]?.[key] || key;
    }
}

// Créer et exporter l'instance globale
window.translationManager = new TranslationManager();

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.translationManager.init();
});
