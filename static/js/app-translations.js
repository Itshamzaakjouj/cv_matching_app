// Définition des traductions
const translations = {
    fr: {
        // Titres principaux
        "Configuration": "Configuration",
        "Paramètres de l'application": "Paramètres de l'application",
        "Paramètres": "Paramètres",
        
        // Navigation
        "NAVIGATION": "NAVIGATION",
        "Accueil": "Accueil",
        "Page principale": "Page principale",
        "Tableau de Bord": "Tableau de Bord",
        "Vue d'ensemble": "Vue d'ensemble",
        "Nouvelle Analyse": "Nouvelle Analyse",
        "Analyser des CVs": "Analyser des CVs",
        "CVs Traités": "CVs Traités",
        "Historique des analyses": "Historique des analyses",
        "Configuration": "Configuration",
        "Paramètres": "Paramètres",

        // Paramètres
        "Thème": "Thème",
        "Choisissez le thème de l'interface": "Choisissez le thème de l'interface",
        "Clair": "Clair",
        "Sombre": "Sombre",
        "Langue": "Langue",
        "Sélectionnez la langue de l'interface": "Sélectionnez la langue de l'interface",
        "Notifications": "Notifications",
        "Configurez vos préférences de notification": "Configurez vos préférences de notification",
        "Notifications par email": "Notifications par email",
        "Notifications push": "Notifications push",

        // En-tête
        "TalentScope": "TalentScope",
        "Ministère de l'Économie et des Finances": "Ministère de l'Économie et des Finances",
        "Plateforme de gestion des talents": "Plateforme de gestion des talents",
    },
    en: {
        // Main titles
        "Configuration": "Settings",
        "Paramètres de l'application": "Application Settings",
        "Paramètres": "Parameters",
        
        // Navigation
        "NAVIGATION": "NAVIGATION",
        "Accueil": "Home",
        "Page principale": "Main Page",
        "Tableau de Bord": "Dashboard",
        "Vue d'ensemble": "Overview",
        "Nouvelle Analyse": "New Analysis",
        "Analyser des CVs": "Analyze CVs",
        "CVs Traités": "Processed CVs",
        "Historique des analyses": "Analysis History",
        "Configuration": "Settings",
        "Paramètres": "Parameters",

        // Settings
        "Thème": "Theme",
        "Choisissez le thème de l'interface": "Choose interface theme",
        "Clair": "Light",
        "Sombre": "Dark",
        "Langue": "Language",
        "Sélectionnez la langue de l'interface": "Select interface language",
        "Notifications": "Notifications",
        "Configurez vos préférences de notification": "Configure your notification preferences",
        "Notifications par email": "Email notifications",
        "Notifications push": "Push notifications",

        // Header
        "TalentScope": "TalentScope",
        "Ministère de l'Économie et des Finances": "Ministry of Economy and Finance",
        "Plateforme de gestion des talents": "Talent Management Platform",
    }
};

class AppTranslator {
    constructor() {
        this.currentLang = localStorage.getItem('app_language') || 'fr';
        this.translations = translations;
        this.init();
    }

    init() {
        // Initialiser la langue au chargement
        this.updatePageLanguage();
        
        // Configurer les écouteurs d'événements
        document.addEventListener('DOMContentLoaded', () => {
            const langSelect = document.querySelector('select[name="langue"]');
            if (langSelect) {
                langSelect.value = this.currentLang;
                langSelect.addEventListener('change', (e) => this.changeLanguage(e.target.value));
            }
        });
    }

    changeLanguage(newLang) {
        if (this.translations[newLang]) {
            this.currentLang = newLang;
            localStorage.setItem('app_language', newLang);
            this.updatePageLanguage();
        }
    }

    updatePageLanguage() {
        // Mettre à jour l'attribut lang de la page
        document.documentElement.lang = this.currentLang;

        // Animation de transition
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(-10px)';
        }

        // Traduire tous les éléments de texte
        this.translateTextContent();

        // Animation de retour
        setTimeout(() => {
            if (mainContent) {
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';
            }
        }, 300);
    }

    translateTextContent() {
        // Traduire le texte visible
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        let node;
        while (node = walker.nextNode()) {
            const text = node.textContent.trim();
            if (text && this.translations[this.currentLang][text]) {
                node.textContent = node.textContent.replace(
                    text,
                    this.translations[this.currentLang][text]
                );
            }
        }

        // Traduire les attributs (placeholder, title, etc.)
        document.querySelectorAll('[placeholder], [title]').forEach(element => {
            if (element.hasAttribute('placeholder')) {
                const text = element.getAttribute('placeholder');
                if (this.translations[this.currentLang][text]) {
                    element.setAttribute('placeholder', this.translations[this.currentLang][text]);
                }
            }
            if (element.hasAttribute('title')) {
                const text = element.getAttribute('title');
                if (this.translations[this.currentLang][text]) {
                    element.setAttribute('title', this.translations[this.currentLang][text]);
                }
            }
        });
    }
}

// Créer l'instance du traducteur
const appTranslator = new AppTranslator();

// Exporter pour utilisation externe
window.appTranslator = appTranslator;
