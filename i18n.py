from typing import Dict


LANG_FR: Dict[str, str] = {
    # Common
    "app.title": "TalentScope",
    "app.subtitle": "Ministère de l'Économie et des Finances",
    "btn.login": "Se connecter",
    "btn.create_account": "Créer un compte",
    "btn.back_to_login": "Retour connexion",
    "btn.logout": "Se déconnecter",
    "btn.next": "Suivant",
    "btn.prev": "Précédent",
    "btn.start": "Commencer l'analyse",
    "btn.new_analysis": "Nouvelle analyse",
    "label.email": "Adresse e-mail",
    "label.password": "Mot de passe",
    "label.confirm_password": "Confirmer le mot de passe",
    "msg.fill_all": "Veuillez remplir tous les champs",
    "msg.success_login": "Connexion réussie !",
    "msg.invalid_email": "Format d'email invalide.",
    "msg.email_exists": "Cet email est déjà utilisé.",
    "msg.password_short": "Le mot de passe doit contenir au moins 8 caractères.",
    "msg.password_upper": "Le mot de passe doit contenir au moins une majuscule.",
    "msg.password_lower": "Le mot de passe doit contenir au moins une minuscule.",
    "msg.password_digit": "Le mot de passe doit contenir au moins un chiffre.",
    "msg.password_special": "Le mot de passe doit contenir au moins un caractère spécial.",
    "msg.password_mismatch": "Les mots de passe ne correspondent pas.",
    "auth.title_create": "Créer un nouveau compte",

    # Main flow
    "step.job.title": "Saisie de l'offre d'emploi",
    "step.job.help": "Veuillez saisir la description du poste à pourvoir :",
    "step.job.text": "Description du poste",
    "step.job.placeholder": "Exemple: Développeur Python senior avec 5 ans d'expérience...",
    "error.job_required": "Veuillez saisir une description de poste.",

    "step.upload.title": "Importation des CVs",
    "step.upload.help": "Veuillez sélectionner les CVs à analyser :",
    "step.upload.input": "Choisir des fichiers PDF",
    "step.upload.help_input": "Sélectionnez un ou plusieurs fichiers PDF de CVs",
    "step.upload.success": "fichier(s) sélectionné(s)",
    "step.upload.selected": "Fichiers sélectionnés :",
    "error.upload_required": "Veuillez sélectionner au moins un CV.",

    "step.verify.title": "Vérification des données",
    "step.verify.help": "Veuillez vérifier les informations avant de lancer l'analyse :",
    "step.verify.job": "Offre d'emploi",
    "step.verify.cv": "CVs sélectionnés",
    "step.verify.none": "Aucun CV sélectionné",
    "error.incomplete": "Données incomplètes. Veuillez retourner aux étapes précédentes.",

    "step.results.title": "Résultats de l'analyse",
    "error.no_data": "Aucune donnée disponible pour l'analyse. Veuillez retourner aux étapes précédentes.",
    "results.classification": "Classification des CVs",
    "results.details": "Détails:",
    "results.technical": "Compétences",
    "results.experience": "Expérience",
    "results.education": "Éducation",
    "results.status.excellent": "Excellent",
    "results.status.very_good": "Très bon",
    "results.status.good": "Bon",
    "results.status.average": "Moyen",
    "results.global_stats": "Statistiques globales",
    "metric.total_cvs": "CVs analysés",
    "metric.avg_score": "Score moyen",
    "metric.best_score": "Meilleur score",
    
    # Navigation and main pages
    "nav.home": "Accueil",
    "nav.dashboard": "Dashboard",
    "nav.comparison": "Comparaison",
    "nav.processed_cvs": "CVs Traités",
    "nav.configuration": "Configuration",
    "nav.new_analysis": "Nouvelle analyse",
    "nav.profile": "Mon Profil",
    "nav.logout": "Déconnexion",
    
    # Home page
    "home.title": "Accueil - TalentScope",
    "home.welcome": "Bienvenue dans TalentScope",
    "home.subtitle": "Plateforme intelligente de matching CVs et offres d'emploi",
    "home.description": "Utilisez l'IA pour analyser et classer automatiquement les CVs selon leur pertinence.",
    "home.overview": "Vue d'ensemble",
    "home.quick_actions": "Actions Rapides",
    "home.trends": "Tendances des 7 derniers jours",
    "home.recent_analyses": "Dernières Analyses",
    "home.skills_demanded": "Compétences les Plus Demandées",
    "home.optimization_tips": "Conseils d'Optimisation",
    "home.system_info": "Informations Système",
    
    # Profile page
    "profile.title": "Mon Profil",
    "profile.photo": "Photo de profil",
    "profile.change_photo": "Changer la photo",
    "profile.personal_info": "Informations personnelles",
    "profile.full_name": "Nom complet",
    "profile.department": "Département",
    "profile.position": "Poste",
    "profile.bio": "Biographie",
    "profile.save": "Sauvegarder",
    "profile.cancel": "Annuler",
    "profile.stats": "Mes statistiques",
    "profile.analyses_done": "Analyses effectuées",
    "profile.avg_score": "Score moyen",
    "profile.excellent_cvs": "CVs excellents trouvés",
    "profile.last_login": "Dernière connexion",
    "profile.quick_actions": "Actions rapides",
    "profile.change_password": "Changer le mot de passe",
    "profile.notifications": "Notifications",
    "profile.advanced_settings": "Paramètres avancés",
    
    # Configuration page
    "config.title": "Configuration",
    "config.app_settings": "Paramètres de l'application",
    "config.algorithm": "Algorithme de matching",
    "config.criteria_weights": "Poids des critères:",
    "config.technical_skills": "Compétences techniques",
    "config.experience": "Expérience",
    "config.education": "Éducation",
    "config.classification_thresholds": "Seuils de classification:",
    "config.excellent": "Excellent (≥)",
    "config.very_good": "Très bon (≥)",
    "config.good": "Bon (≥)",
    "config.ui_settings": "Interface utilisateur",
    "config.theme": "Thème",
    "config.language": "Langue",
    "config.show_progress": "Afficher la barre de progression",
    "config.show_details": "Afficher les détails des scores",
    "config.export_settings": "Export et sauvegarde",
    "config.auto_save": "Sauvegarde automatique",
    "config.default_export": "Format d'export par défaut",
    "config.include_charts": "Inclure les graphiques dans l'export",
    "config.email_reports": "Envoyer les rapports par email",
    "config.actions": "Actions",
    "config.save_config": "Sauvegarder la configuration",
    "config.reset": "Réinitialiser",
    "config.export_config": "Exporter la config",
    "config.current_summary": "Résumé de la Configuration Actuelle",
    "config.algorithm_title": "Algorithme:",
    "config.interface_title": "Interface:",
    "config.total": "Total:",
    "config.progression": "Progression:",
    "config.details": "Détails:",
    "config.warning_weights": "Attention: La somme des poids des critères ({total:.1%}) n'est pas égale à 100%",
    "config.error_excellent": "Erreur: Le seuil 'Excellent' doit être supérieur au seuil 'Très bon'",
    "config.error_good": "Erreur: Le seuil 'Très bon' doit être supérieur au seuil 'Bon'",
    
    # Comparison page
    "comparison.title": "Comparaison des CVs",
    "comparison.side_by_side": "Comparaison côte à côte",
    "comparison.cv1": "CV 1",
    "comparison.cv2": "CV 2",
    "comparison.select_first": "Sélectionner le premier CV",
    "comparison.select_second": "Sélectionner le deuxième CV",
    "comparison.score": "Score:",
    "comparison.technical": "Compétences:",
    "comparison.experience": "Expérience:",
    "comparison.education": "Éducation:",
    "comparison.analysis": "Analyse comparative",
    "comparison.detailed_analysis": "Analyse détaillée",
    "comparison.best_global": "Meilleur score global:",
    "comparison.criteria_comparison": "Comparaison par critère",
    "comparison.equality": "Égalité",
    
    # Processed CVs page
    "processed.title": "CVs Traités",
    "processed.history": "Historique des analyses",
    "processed.filter_status": "Filtrer par statut",
    "processed.filter_date": "Filtrer par date",
    "processed.min_score": "Score minimum",
    "processed.stats": "Statistiques",
    "processed.total_cvs": "Total CVs",
    "processed.avg_score": "Score moyen",
    "processed.best_score": "Meilleur score",
    "processed.excellent_cvs": "CVs excellents",
    
    # Common statuses
    "status.excellent": "Excellent",
    "status.very_good": "Très bon",
    "status.good": "Bon",
    "status.average": "Moyen",
    
    # Departments
    "dept.hr": "Ressources Humaines",
    "dept.it": "Informatique",
    "dept.finance": "Finance",
    "dept.admin": "Administration",
    "dept.other": "Autre",
    
    # Export formats
    "export.pdf": "PDF",
    "export.excel": "Excel",
    "export.csv": "CSV",
    
    # Themes
    "theme.light": "Clair",
    "theme.dark": "Sombre",
    "theme.auto": "Auto",
    
    # Languages
    "lang.french": "Français",
    "lang.english": "Anglais",
    
    # Dashboard
    "dashboard.title": "Dashboard",
    "dashboard.metrics": "Métriques",
    "dashboard.trends": "Tendances",
    "dashboard.recent_analyses": "Dernières Analyses",
}


LANG_EN: Dict[str, str] = {
    # Common
    "app.title": "TalentScope",
    "app.subtitle": "Ministry of Economy and Finance",
    "btn.login": "Sign in",
    "btn.create_account": "Create account",
    "btn.back_to_login": "Back to login",
    "btn.logout": "Log out",
    "btn.next": "Next",
    "btn.prev": "Previous",
    "btn.start": "Start analysis",
    "btn.new_analysis": "New analysis",
    "label.email": "Email address",
    "label.password": "Password",
    "label.confirm_password": "Confirm password",
    "msg.fill_all": "Please fill in all fields",
    "msg.success_login": "Login successful!",
    "msg.invalid_email": "Invalid email format.",
    "msg.email_exists": "This email is already in use.",
    "msg.password_short": "Password must be at least 8 characters.",
    "msg.password_upper": "Password must contain at least one uppercase letter.",
    "msg.password_lower": "Password must contain at least one lowercase letter.",
    "msg.password_digit": "Password must contain at least one digit.",
    "msg.password_special": "Password must contain at least one special character.",
    "msg.password_mismatch": "Passwords do not match.",
    "auth.title_create": "Create a new account",

    # Main flow
    "step.job.title": "Job description",
    "step.job.help": "Please enter the job description:",
    "step.job.text": "Job description",
    "step.job.placeholder": "Example: Senior Python developer with 5+ years experience...",
    "error.job_required": "Please enter a job description.",

    "step.upload.title": "Upload CVs",
    "step.upload.help": "Please select the CVs to analyze:",
    "step.upload.input": "Choose PDF files",
    "step.upload.help_input": "Select one or more PDF CV files",
    "step.upload.success": "file(s) selected",
    "step.upload.selected": "Selected files:",
    "error.upload_required": "Please select at least one CV.",

    "step.verify.title": "Data verification",
    "step.verify.help": "Please verify the information before starting the analysis:",
    "step.verify.job": "Job offer",
    "step.verify.cv": "Selected CVs",
    "step.verify.none": "No CV selected",
    "error.incomplete": "Incomplete data. Please go back to the previous steps.",

    "step.results.title": "Analysis results",
    "error.no_data": "No data available for analysis. Please go back to previous steps.",
    "results.classification": "CV classification",
    "results.details": "Details:",
    "results.technical": "Technical skills",
    "results.experience": "Experience",
    "results.education": "Education",
    "results.status.excellent": "Excellent",
    "results.status.very_good": "Very good",
    "results.status.good": "Good",
    "results.status.average": "Average",
    "results.global_stats": "Global statistics",
    "metric.total_cvs": "CVs analyzed",
    "metric.avg_score": "Average score",
    "metric.best_score": "Best score",
    
    # Navigation and main pages
    "nav.home": "Home",
    "nav.dashboard": "Dashboard",
    "nav.comparison": "Comparison",
    "nav.processed_cvs": "Processed CVs",
    "nav.configuration": "Configuration",
    "nav.new_analysis": "New analysis",
    "nav.profile": "My Profile",
    "nav.logout": "Log out",
    
    # Home page
    "home.title": "Home - TalentScope",
    "home.welcome": "Welcome to TalentScope",
    "home.subtitle": "Intelligent CV and job matching platform",
    "home.description": "Use AI to automatically analyze and rank CVs by relevance.",
    "home.overview": "Overview",
    "home.quick_actions": "Quick Actions",
    "home.trends": "7-day trends",
    "home.recent_analyses": "Recent Analyses",
    "home.skills_demanded": "Most Demanded Skills",
    "home.optimization_tips": "Optimization Tips",
    "home.system_info": "System Information",
    
    # Profile page
    "profile.title": "My Profile",
    "profile.photo": "Profile photo",
    "profile.change_photo": "Change photo",
    "profile.personal_info": "Personal information",
    "profile.full_name": "Full name",
    "profile.department": "Department",
    "profile.position": "Position",
    "profile.bio": "Biography",
    "profile.save": "Save",
    "profile.cancel": "Cancel",
    "profile.stats": "My statistics",
    "profile.analyses_done": "Analyses performed",
    "profile.avg_score": "Average score",
    "profile.excellent_cvs": "Excellent CVs found",
    "profile.last_login": "Last login",
    "profile.quick_actions": "Quick actions",
    "profile.change_password": "Change password",
    "profile.notifications": "Notifications",
    "profile.advanced_settings": "Advanced settings",
    
    # Configuration page
    "config.title": "Configuration",
    "config.app_settings": "Application settings",
    "config.algorithm": "Matching algorithm",
    "config.criteria_weights": "Criteria weights:",
    "config.technical_skills": "Technical skills",
    "config.experience": "Experience",
    "config.education": "Education",
    "config.classification_thresholds": "Classification thresholds:",
    "config.excellent": "Excellent (≥)",
    "config.very_good": "Very good (≥)",
    "config.good": "Good (≥)",
    "config.ui_settings": "User interface",
    "config.theme": "Theme",
    "config.language": "Language",
    "config.show_progress": "Show progress bar",
    "config.show_details": "Show score details",
    "config.export_settings": "Export and save",
    "config.auto_save": "Auto save",
    "config.default_export": "Default export format",
    "config.include_charts": "Include charts in export",
    "config.email_reports": "Send reports by email",
    "config.actions": "Actions",
    "config.save_config": "Save configuration",
    "config.reset": "Reset",
    "config.export_config": "Export config",
    "config.current_summary": "Current Configuration Summary",
    "config.algorithm_title": "Algorithm:",
    "config.interface_title": "Interface:",
    "config.total": "Total:",
    "config.progression": "Progress:",
    "config.details": "Details:",
    "config.warning_weights": "Warning: Sum of criteria weights ({total:.1%}) is not equal to 100%",
    "config.error_excellent": "Error: 'Excellent' threshold must be higher than 'Very good' threshold",
    "config.error_good": "Error: 'Very good' threshold must be higher than 'Good' threshold",
    
    # Comparison page
    "comparison.title": "CV Comparison",
    "comparison.side_by_side": "Side-by-side comparison",
    "comparison.cv1": "CV 1",
    "comparison.cv2": "CV 2",
    "comparison.select_first": "Select first CV",
    "comparison.select_second": "Select second CV",
    "comparison.score": "Score:",
    "comparison.technical": "Skills:",
    "comparison.experience": "Experience:",
    "comparison.education": "Education:",
    "comparison.analysis": "Comparative analysis",
    "comparison.detailed_analysis": "Detailed analysis",
    "comparison.best_global": "Best global score:",
    "comparison.criteria_comparison": "Criteria comparison",
    "comparison.equality": "Equality",
    
    # Processed CVs page
    "processed.title": "Processed CVs",
    "processed.history": "Analysis history",
    "processed.filter_status": "Filter by status",
    "processed.filter_date": "Filter by date",
    "processed.min_score": "Minimum score",
    "processed.stats": "Statistics",
    "processed.total_cvs": "Total CVs",
    "processed.avg_score": "Average score",
    "processed.best_score": "Best score",
    "processed.excellent_cvs": "Excellent CVs",
    
    # Common statuses
    "status.excellent": "Excellent",
    "status.very_good": "Very good",
    "status.good": "Good",
    "status.average": "Average",
    
    # Departments
    "dept.hr": "Human Resources",
    "dept.it": "Information Technology",
    "dept.finance": "Finance",
    "dept.admin": "Administration",
    "dept.other": "Other",
    
    # Export formats
    "export.pdf": "PDF",
    "export.excel": "Excel",
    "export.csv": "CSV",
    
    # Themes
    "theme.light": "Light",
    "theme.dark": "Dark",
    "theme.auto": "Auto",
    
    # Languages
    "lang.french": "French",
    "lang.english": "English",
    
    # Dashboard
    "dashboard.title": "Dashboard",
    "dashboard.metrics": "Metrics",
    "dashboard.trends": "Trends",
    "dashboard.recent_analyses": "Recent Analyses",
}


def get_language() -> str:
    # Lire la langue depuis le fichier config.json
    try:
        import json
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            language = config.get("language", "Français")
            # Mettre à jour la session state
            try:
                if hasattr(st, 'session_state'):
                    st.session_state.language = language
            except Exception:
                pass
            return language
    except Exception:
        pass
    
    # Fallback: Session state
    try:
        if hasattr(st, 'session_state') and 'language' in st.session_state:
            return st.session_state.language
    except Exception:
        pass
    
    # Fallback: Français par défaut
    return "Français"


def t(key: str) -> str:
    # Lire la langue depuis le fichier config.json à chaque appel
    lang = "Français"  # Par défaut
    
    try:
        import json
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            lang = config.get("language", "Français")
    except Exception:
        pass
    
    # Mettre à jour la session state
    try:
        if hasattr(st, 'session_state'):
            st.session_state.language = lang
    except Exception:
        pass
    
    # Choisir le bon catalogue
    if lang == "Anglais":
        catalog = LANG_EN
    else:
        catalog = LANG_FR
    
    # Ajouter un paramètre de cache-busting si disponible
    result = catalog.get(key, key)
    
    # Si on a un timestamp de langue, ajouter un commentaire pour forcer le rechargement
    try:
        if hasattr(st, 'session_state') and 'language_timestamp' in st.session_state:
            # Forcer le rechargement en ajoutant un caractère invisible
            result = result + "<!-- cache-bust -->"
    except Exception:
        pass
    
    return result

def force_language_reload():
    """Force le rechargement de la langue depuis le fichier config.json"""
    try:
        import json
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            language = config.get("language", "Français")
            if hasattr(st, 'session_state'):
                st.session_state.language = language
            return language
    except Exception:
        pass
    return "Français"


_AUTH_FR_TO_KEY = {
    "Email non trouvé.": "auth.error.email_not_found",
    "Mot de passe incorrect.": "auth.error.bad_password",
    "Connexion réussie !": "msg.success_login",
    "Format d'email invalide.": "msg.invalid_email",
    "Cet email est déjà utilisé.": "msg.email_exists",
    "Le mot de passe doit contenir au moins 8 caractères.": "msg.password_short",
    "Le mot de passe doit contenir au moins une majuscule.": "msg.password_upper",
    "Le mot de passe doit contenir au moins une minuscule.": "msg.password_lower",
    "Le mot de passe doit contenir au moins un chiffre.": "msg.password_digit",
    "Le mot de passe doit contenir au moins un caractère spécial.": "msg.password_special",
    "Les mots de passe ne correspondent pas.": "msg.password_mismatch",
    "Compte créé avec succès !": "auth.success.account_created",
}


LANG_EN.update({
    "auth.error.email_not_found": "Email not found.",
    "auth.error.bad_password": "Incorrect password.",
    "auth.success.account_created": "Account created successfully!",
})


def translate_auth_message(message_fr: str) -> str:
    key = _AUTH_FR_TO_KEY.get(message_fr)
    if not key:
        return message_fr
    return t(key)


