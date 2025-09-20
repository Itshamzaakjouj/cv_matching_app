/**
 * Système de traduction forcé et simple
 */
class ForceTranslationManager {
    constructor() {
        this.translations = {
            fr: {
                "nav.home": "Accueil",
                "nav.dashboard": "Tableau de Bord",
                "nav.analysis": "Nouvelle Analyse",
                "nav.history": "CVs Traités",
                "nav.config": "Configuration",
                "nav.home_subtitle": "Page principale",
                "nav.dashboard_subtitle": "Vue d'ensemble",
                "nav.analysis_subtitle": "Analyser des CVs",
                "nav.history_subtitle": "Historique des analyses",
                "nav.config_subtitle": "Paramètres",
                "dashboard.title": "Tableau de Bord",
                "dashboard.subtitle": "Vue d'ensemble de vos analyses et statistiques",
                "dashboard.total_cvs": "Total CVs Analysés",
                "dashboard.avg_score": "Score Moyen des CVs",
                "dashboard.pending_analysis": "Analyses en Attente",
                "dashboard.new_analysis": "Nouvelle Analyse",
                "dashboard.view_history": "Voir l'Historique",
                "dashboard.quick_actions": "Actions Rapides",
                "dashboard.recent_analysis": "Analyses Récentes",
                "dashboard.no_recent_analysis": "Aucune analyse récente.",
                "config.title": "Configuration",
                "config.subtitle": "Paramètres de l'application et préférences utilisateur",
                "config.theme": "Thème",
                "config.language": "Langue",
                "config.language_description": "Sélectionnez la langue de l'interface",
                "config.notifications": "Notifications",
                "config.notifications_description": "Configurez vos préférences de notification",
                "config.email_notifications": "Notifications par email",
                "config.push_notifications": "Notifications push",
                "config.danger_zone": "Zone de danger",
                "config.delete_history": "Supprimer l'historique",
                "config.reset_site": "Réinitialiser le site",
                "lang.fr": "Français",
                "lang.en": "English"
            },
            en: {
                "nav.home": "Home",
                "nav.dashboard": "Dashboard",
                "nav.analysis": "New Analysis",
                "nav.history": "Processed CVs",
                "nav.config": "Configuration",
                "nav.home_subtitle": "Main page",
                "nav.dashboard_subtitle": "Overview",
                "nav.analysis_subtitle": "Analyze CVs",
                "nav.history_subtitle": "Analysis history",
                "nav.config_subtitle": "Settings",
                "dashboard.title": "Dashboard",
                "dashboard.subtitle": "Overview of your analyses and statistics",
                "dashboard.total_cvs": "Total CVs Analyzed",
                "dashboard.avg_score": "Average CV Score",
                "dashboard.pending_analysis": "Pending Analyses",
                "dashboard.new_analysis": "New Analysis",
                "dashboard.view_history": "View History",
                "dashboard.quick_actions": "Quick Actions",
                "dashboard.recent_analysis": "Recent Analyses",
                "dashboard.no_recent_analysis": "No recent analyses.",
                "config.title": "Configuration",
                "config.subtitle": "Application settings and user preferences",
                "config.theme": "Theme",
                "config.language": "Language",
                "config.language_description": "Select the interface language",
                "config.notifications": "Notifications",
                "config.notifications_description": "Configure your notification preferences",
                "config.email_notifications": "Email notifications",
                "config.push_notifications": "Push notifications",
                "config.danger_zone": "Danger zone",
                "config.delete_history": "Delete history",
                "config.reset_site": "Reset site",
                "lang.fr": "Français",
                "lang.en": "English"
            }
        };
        
        this.currentLanguage = localStorage.getItem('language') || 'fr';
        this.init();
    }

    init() {
        console.log('ForceTranslationManager initializing with language:', this.currentLanguage);
        
        // Attendre que le DOM soit chargé
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.applyLanguage(this.currentLanguage);
            });
        } else {
            this.applyLanguage(this.currentLanguage);
        }
    }

    getTranslation(key) {
        const keys = key.split('.');
        let result = this.translations[this.currentLanguage];
        
        for (const k of keys) {
            if (result && result[k] !== undefined) {
                result = result[k];
            } else {
                console.warn(`Translation key "${key}" not found for language "${this.currentLanguage}"`);
                return key;
            }
        }
        return result;
    }

    applyLanguage(language) {
        console.log(`Force applying language: ${language}`);
        
        if (!this.translations[language]) {
            console.warn(`Language ${language} not found in translations`);
            return;
        }

        this.currentLanguage = language;
        localStorage.setItem('language', language);
        document.documentElement.lang = language;

        // Forcer la traduction de tous les éléments
        this.forceTranslateAll();
        
        // Mettre à jour les sélecteurs
        this.updateLanguageSelectors(language);
        
        console.log(`Language ${language} applied successfully`);
    }

    forceTranslateAll() {
        // Traduire tous les éléments avec data-translate
        const elements = document.querySelectorAll('[data-translate]');
        console.log(`Force translating ${elements.length} elements`);
        
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            
            if (translation && translation !== key) {
                element.textContent = translation;
                console.log(`Force translated ${key} to ${translation}`);
            }
        });

        // Traduire les placeholders
        const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            const translation = this.getTranslation(key);
            
            if (translation && translation !== key) {
                element.placeholder = translation;
            }
        });

        // Traduire les titres
        const titleElements = document.querySelectorAll('[data-translate-title]');
        titleElements.forEach(element => {
            const key = element.getAttribute('data-translate-title');
            const translation = this.getTranslation(key);
            
            if (translation && translation !== key) {
                element.title = translation;
            }
        });

        // Traduire les valeurs des options
        const optionElements = document.querySelectorAll('[data-translate-value]');
        optionElements.forEach(element => {
            const key = element.getAttribute('data-translate-value');
            const translation = this.getTranslation(key);
            
            if (translation && translation !== key) {
                element.value = translation;
            }
        });
    }

    updateLanguageSelectors(language) {
        const languageSelects = document.querySelectorAll('#language-select, #config-language-select');
        languageSelects.forEach(select => {
            if (select) {
                select.value = language;
            }
        });
    }

    changeLanguage(language) {
        console.log(`Force changing language to: ${language}`);
        this.applyLanguage(language);
    }
}

// Initialiser le gestionnaire de traduction
const forceTranslationManager = new ForceTranslationManager();

// Fonction globale pour le changement de langue
window.handleLanguageChange = function(selectElement) {
    const language = selectElement.value;
    console.log('handleLanguageChange called with:', language);
    
    // Sauvegarder la langue
    localStorage.setItem('language', language);
    
    // Notification
    const message = language === 'fr' ? 'Changement vers le français...' : 'Switching to English...';
    alert(message);
    
    // Recharger la page
    setTimeout(() => {
        location.reload();
    }, 1000);
};

// Fonction globale pour le changement de thème
window.handleThemeChange = function(selectElement) {
    const theme = selectElement.value;
    console.log('handleThemeChange called with:', theme);
    
    // Appliquer le thème
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Mettre à jour le bouton de thème
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
};

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, force translation manager ready');
});

