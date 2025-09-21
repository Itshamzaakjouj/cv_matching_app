/**
 * Système de Traduction Global pour TalentScope
 * Gère la traduction de toutes les pages de l'application
 */

class TranslationSystem {
    constructor() {
        this.currentLanguage = localStorage.getItem('talentScope_language') || 'fr';
        this.translations = {
            fr: {
                // Navigation
                'nav.home': 'Accueil',
                'nav.home.subtitle': 'Page principale',
                'nav.dashboard': 'Tableau de Bord',
                'nav.dashboard.subtitle': 'Vue d\'ensemble',
                'nav.new-analysis': 'Nouvelle Analyse',
                'nav.new-analysis.subtitle': 'Analyser des CVs',
                'nav.history': 'Historique',
                'nav.history.subtitle': 'Analyses précédentes',
                'nav.translator': 'Traducteur',
                'nav.translator.subtitle': 'Traduction multilingue',
                'nav.configuration': 'Configuration',
                'nav.configuration.subtitle': 'Gestion du compte',
                'nav.logout': 'Déconnexion',

                // Page de Configuration
                'config.title': 'Configuration du Profil',
                'config.subtitle': 'Gérez vos informations personnelles, paramètres de sécurité et préférences. Personnalisez votre expérience sur TalentScope selon vos besoins professionnels.',
                'config.personal-info': 'Informations Personnelles',
                'config.account-security': 'Sécurité du Compte',
                'config.system-preferences': 'Préférences Système',
                'config.usage-stats': 'Statistiques d\'Utilisation',

                // Informations Personnelles
                'personal.verified-account': 'Compte vérifié',
                'personal.full-name': 'Nom complet',
                'personal.email': 'Adresse e-mail professionnelle',
                'personal.department': 'Département',
                'personal.position': 'Poste',
                'personal.phone': 'Téléphone professionnel',
                'personal.cancel': 'Annuler',
                'personal.save': 'Enregistrer',
                'personal.upload-photo': 'Changer la photo',

                // Sécurité
                'security.password': 'Mot de passe',
                'security.password.last-modified': 'Dernière modification il y a 30 jours',
                'security.password.secure': 'Sécurisé',
                'security.password.modify': 'Modifier',
                'security.2fa': 'Authentification à deux facteurs',
                'security.2fa.description': 'Ajoutez une couche de sécurité supplémentaire',
                'security.2fa.not-activated': 'Non activé',
                'security.2fa.activate': 'Activer',
                'security.sessions': 'Sessions actives',
                'security.sessions.description': '2 appareils connectés actuellement',
                'security.sessions.manage': 'Gérer',
                'security.delete-account': 'Suppression du compte',
                'security.delete-account.description': 'Action irréversible - Supprimer définitivement',
                'security.delete-account.delete': 'Supprimer',

                // Préférences
                'preferences.email-notifications': 'Notifications par e-mail',
                'preferences.email-notifications.description': 'Recevoir des notifications importantes',
                'preferences.dark-mode': 'Mode sombre',
                'preferences.dark-mode.description': 'Interface en thème sombre',
                'preferences.language': 'Langue de l\'interface',
                'preferences.language.current': 'Français (FR)',
                'preferences.language.change': 'Changer',
                'preferences.timezone': 'Fuseau horaire',
                'preferences.timezone.current': 'Europe/Paris (UTC+1)',
                'preferences.timezone.change': 'Modifier',

                // Statistiques
                'stats.analyses-performed': 'Analyses effectuées',
                'stats.average-score': 'Score moyen',
                'stats.member-since': 'Membre depuis',
                'stats.last-login': 'Dernière connexion',

                // Messages
                'message.success': 'Modifications sauvegardées avec succès !',
                'message.error': 'Une erreur est survenue lors de la sauvegarde.',
                'message.profile-updated': 'Profil mis à jour avec succès !',
                'message.form-reset': 'Formulaire réinitialisé',
                'message.password-changed': 'Mot de passe modifié avec succès',
                'message.password-too-short': 'Le mot de passe doit contenir au moins 8 caractères',
                'message.2fa-enabled': '2FA activé avec succès',
                'message.language-changed': 'Langue changée vers',
                'message.timezone-changed': 'Fuseau horaire changé vers',
                'message.preference-enabled': 'activée',
                'message.preference-disabled': 'désactivée',
                'message.photo-updated': 'Photo de profil mise à jour',

                // Confirmations
                'confirm.logout': 'Êtes-vous sûr de vouloir vous déconnecter ?',
                'confirm.enable-2fa': 'Voulez-vous activer l\'authentification à deux facteurs ?',
                'confirm.delete-account': 'Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.',
                'confirm.delete-account-final': 'Confirmez la suppression définitive de votre compte.',

                // Départements
                'department.development': 'Développement',
                'department.finance': 'Finance',
                'department.hr': 'Ressources Humaines',
                'department.marketing': 'Marketing',
                'department.operations': 'Opérations'
            },
            en: {
                // Navigation
                'nav.home': 'Home',
                'nav.home.subtitle': 'Main page',
                'nav.dashboard': 'Dashboard',
                'nav.dashboard.subtitle': 'Overview',
                'nav.new-analysis': 'New Analysis',
                'nav.new-analysis.subtitle': 'Analyze CVs',
                'nav.history': 'History',
                'nav.history.subtitle': 'Previous analyses',
                'nav.translator': 'Translator',
                'nav.translator.subtitle': 'Multilingual translation',
                'nav.configuration': 'Configuration',
                'nav.configuration.subtitle': 'Account management',
                'nav.logout': 'Logout',

                // Page de Configuration
                'config.title': 'Profile Configuration',
                'config.subtitle': 'Manage your personal information, security settings and preferences. Personalize your TalentScope experience according to your professional needs.',
                'config.personal-info': 'Personal Information',
                'config.account-security': 'Account Security',
                'config.system-preferences': 'System Preferences',
                'config.usage-stats': 'Usage Statistics',

                // Informations Personnelles
                'personal.verified-account': 'Verified account',
                'personal.full-name': 'Full name',
                'personal.email': 'Professional email address',
                'personal.department': 'Department',
                'personal.position': 'Position',
                'personal.phone': 'Professional phone',
                'personal.cancel': 'Cancel',
                'personal.save': 'Save',
                'personal.upload-photo': 'Change photo',

                // Sécurité
                'security.password': 'Password',
                'security.password.last-modified': 'Last modified 30 days ago',
                'security.password.secure': 'Secure',
                'security.password.modify': 'Modify',
                'security.2fa': 'Two-factor authentication',
                'security.2fa.description': 'Add an additional layer of security',
                'security.2fa.not-activated': 'Not activated',
                'security.2fa.activate': 'Activate',
                'security.sessions': 'Active sessions',
                'security.sessions.description': '2 devices currently connected',
                'security.sessions.manage': 'Manage',
                'security.delete-account': 'Account deletion',
                'security.delete-account.description': 'Irreversible action - Delete permanently',
                'security.delete-account.delete': 'Delete',

                // Préférences
                'preferences.email-notifications': 'Email notifications',
                'preferences.email-notifications.description': 'Receive important notifications',
                'preferences.dark-mode': 'Dark mode',
                'preferences.dark-mode.description': 'Dark theme interface',
                'preferences.language': 'Interface language',
                'preferences.language.current': 'English (EN)',
                'preferences.language.change': 'Change',
                'preferences.timezone': 'Timezone',
                'preferences.timezone.current': 'Europe/Paris (UTC+1)',
                'preferences.timezone.change': 'Modify',

                // Statistiques
                'stats.analyses-performed': 'Analyses performed',
                'stats.average-score': 'Average score',
                'stats.member-since': 'Member since',
                'stats.last-login': 'Last login',

                // Messages
                'message.success': 'Changes saved successfully!',
                'message.error': 'An error occurred while saving.',
                'message.profile-updated': 'Profile updated successfully!',
                'message.form-reset': 'Form reset',
                'message.password-changed': 'Password changed successfully',
                'message.password-too-short': 'Password must contain at least 8 characters',
                'message.2fa-enabled': '2FA enabled successfully',
                'message.language-changed': 'Language changed to',
                'message.timezone-changed': 'Timezone changed to',
                'message.preference-enabled': 'enabled',
                'message.preference-disabled': 'disabled',
                'message.photo-updated': 'Profile photo updated',

                // Confirmations
                'confirm.logout': 'Are you sure you want to logout?',
                'confirm.enable-2fa': 'Do you want to enable two-factor authentication?',
                'confirm.delete-account': 'Are you sure you want to delete your account? This action is irreversible.',
                'confirm.delete-account-final': 'Confirm the permanent deletion of your account.',

                // Départements
                'department.development': 'Development',
                'department.finance': 'Finance',
                'department.hr': 'Human Resources',
                'department.marketing': 'Marketing',
                'department.operations': 'Operations'
            }
        };
        
        this.init();
    }

    init() {
        this.applyTranslations();
        this.setupLanguageSelector();
    }

    setLanguage(language) {
        if (this.translations[language]) {
            this.currentLanguage = language;
            localStorage.setItem('talentScope_language', language);
            this.applyTranslations();
            this.updateLanguageSelector();
            
            // Notifier les autres composants du changement de langue
            window.dispatchEvent(new CustomEvent('languageChanged', {
                detail: { language: language }
            }));
        }
    }

    getTranslation(key) {
        const keys = key.split('.');
        let translation = this.translations[this.currentLanguage];
        
        for (const k of keys) {
            if (translation && translation[k]) {
                translation = translation[k];
            } else {
                // Fallback vers le français si la traduction n'existe pas
                translation = this.translations.fr;
                for (const fallbackKey of keys) {
                    if (translation && translation[fallbackKey]) {
                        translation = translation[fallbackKey];
                    } else {
                        return key; // Retourner la clé si aucune traduction trouvée
                    }
                }
                break;
            }
        }
        
        return translation || key;
    }

    applyTranslations() {
        // Traduire les éléments avec data-translate
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else if (element.tagName === 'INPUT' && element.type === 'email') {
                element.placeholder = translation;
            } else if (element.tagName === 'INPUT' && element.type === 'tel') {
                element.placeholder = translation;
            } else if (element.tagName === 'SELECT') {
                // Pour les selects, on traduit les options
                const options = element.querySelectorAll('option');
                options.forEach(option => {
                    const optionKey = option.getAttribute('data-translate');
                    if (optionKey) {
                        option.textContent = this.getTranslation(optionKey);
                    }
                });
            } else {
                element.textContent = translation;
            }
        });

        // Traduire les éléments avec data-translate-title
        document.querySelectorAll('[data-translate-title]').forEach(element => {
            const key = element.getAttribute('data-translate-title');
            element.title = this.getTranslation(key);
        });

        // Traduire les éléments avec data-translate-placeholder
        document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
            const key = element.getAttribute('data-translate-placeholder');
            element.placeholder = this.getTranslation(key);
        });

        // Mettre à jour le sélecteur de langue
        this.updateLanguageSelector();
    }

    setupLanguageSelector() {
        // Créer le sélecteur de langue s'il n'existe pas
        let languageSelector = document.getElementById('language-selector');
        if (!languageSelector) {
            languageSelector = document.createElement('select');
            languageSelector.id = 'language-selector';
            languageSelector.className = 'language-selector';
            languageSelector.innerHTML = `
                <option value="fr">Français</option>
                <option value="en">English</option>
            `;
            
            // Ajouter le sélecteur à la page
            const header = document.querySelector('.page-header');
            if (header) {
                const titleContainer = header.querySelector('.page-title');
                if (titleContainer) {
                    titleContainer.appendChild(languageSelector);
                }
            }
        }

        // Ajouter l'événement de changement
        languageSelector.addEventListener('change', (e) => {
            this.setLanguage(e.target.value);
        });
    }

    updateLanguageSelector() {
        const languageSelector = document.getElementById('language-selector');
        if (languageSelector) {
            languageSelector.value = this.currentLanguage;
        }
    }

    // Méthode pour ajouter des traductions dynamiquement
    addTranslations(language, translations) {
        if (!this.translations[language]) {
            this.translations[language] = {};
        }
        Object.assign(this.translations[language], translations);
    }

    // Méthode pour obtenir la langue actuelle
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Méthode pour obtenir toutes les langues disponibles
    getAvailableLanguages() {
        return Object.keys(this.translations);
    }
}

// Créer une instance globale
window.translationSystem = new TranslationSystem();

// Fonction utilitaire pour traduire du texte
function translate(key) {
    return window.translationSystem.getTranslation(key);
}

// Fonction utilitaire pour changer de langue
function changeLanguage(language) {
    window.translationSystem.setLanguage(language);
}

// Initialiser le système quand le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    if (window.translationSystem) {
        window.translationSystem.init();
    }
});

// Exporter pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TranslationSystem;
}
