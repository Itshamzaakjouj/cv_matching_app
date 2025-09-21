const TRANSLATIONS = {
    fr: {
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

        // Titres
        "TalentScope": "TalentScope",
        "Ministère de l'Économie et des Finances": "Ministère de l'Économie et des Finances",
        "Plateforme de gestion des talents": "Plateforme de gestion des talents",
        "Paramètres de l'application": "Paramètres de l'application",

        // Page Paramètres
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
    },
    en: {
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

        // Titles
        "TalentScope": "TalentScope",
        "Ministère de l'Économie et des Finances": "Ministry of Economy and Finance",
        "Plateforme de gestion des talents": "Talent Management Platform",
        "Paramètres de l'application": "Application Settings",

        // Settings Page
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
    }
};

class I18nManager {
    constructor() {
        this.currentLang = localStorage.getItem('app_language') || 'fr';
        this.translations = TRANSLATIONS;
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupLanguageSelector();
            this.translatePage();
        });
    }

    setupLanguageSelector() {
        const langSelect = document.querySelector('select[name="langue"]');
        if (langSelect) {
            langSelect.value = this.currentLang;
            langSelect.addEventListener('change', (e) => this.changeLanguage(e.target.value));
        }
    }

    changeLanguage(newLang) {
        if (this.translations[newLang]) {
            this.currentLang = newLang;
            localStorage.setItem('app_language', newLang);
            this.translateWithAnimation();
        }
    }

    translateWithAnimation() {
        const mainContent = document.querySelector('.main-content');
        const sidebar = document.querySelector('.sidebar');

        // Animation de sortie
        [mainContent, sidebar].forEach(el => {
            if (el) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(-10px)';
            }
        });

        // Traduire après un court délai
        setTimeout(() => {
            this.translatePage();

            // Animation d'entrée
            [mainContent, sidebar].forEach(el => {
                if (el) {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }
            });
        }, 200);
    }

    translatePage() {
        // Mettre à jour l'attribut lang de la page
        document.documentElement.lang = this.currentLang;

        // Traduire tous les textes visibles
        this.translateTextNodes(document.body);
        
        // Traduire les attributs spécifiques
        this.translateAttributes();
        
        // Traduire les options des sélecteurs
        this.translateSelects();
    }

    translateTextNodes(element) {
        const walker = document.createTreeWalker(
            element,
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
    }

    translateAttributes() {
        // Traduire les placeholders
        document.querySelectorAll('[placeholder]').forEach(el => {
            const text = el.getAttribute('placeholder');
            if (this.translations[this.currentLang][text]) {
                el.setAttribute('placeholder', this.translations[this.currentLang][text]);
            }
        });

        // Traduire les titles
        document.querySelectorAll('[title]').forEach(el => {
            const text = el.getAttribute('title');
            if (this.translations[this.currentLang][text]) {
                el.setAttribute('title', this.translations[this.currentLang][text]);
            }
        });
    }

    translateSelects() {
        document.querySelectorAll('select').forEach(select => {
            Array.from(select.options).forEach(option => {
                const text = option.text;
                if (this.translations[this.currentLang][text]) {
                    option.text = this.translations[this.currentLang][text];
                }
            });
        });
    }

    getTranslation(key) {
        return this.translations[this.currentLang][key] || key;
    }
}

// Créer et exporter l'instance
window.i18n = new I18nManager();
