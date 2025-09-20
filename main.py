"""
TalentScope - Dashboard Principal Modernisé
Ministère de l'Économie et des Finances
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports des composants
from components.charts import ChartFactory, get_sample_data
from components.metrics import (
    MetricsDashboard, CVCard, ProgressIndicator, 
    QuickActions, SystemInfo, TipsSection, get_sample_cv_data
)
from components.ui_elements import (
    HeaderComponent, SidebarNavigation, FilterComponent,
    ModalComponent, NotificationComponent, ResponsiveGrid
)
from i18n import t

# Configuration de la page
st.set_page_config(
    page_title="TalentScope - Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger les styles CSS
def load_css():
    """Charge les styles CSS personnalisés"""
    try:
        with open("assets/styles.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Styles de base si le fichier CSS n'existe pas
        st.markdown("""
        <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
        }
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
            margin: 0;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialiser les styles
load_css()

def init_session_state():
    """Initialise l'état de la session"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_home' not in st.session_state:
        st.session_state.show_home = True
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    if 'show_comparison' not in st.session_state:
        st.session_state.show_comparison = False
    if 'show_processed_cvs' not in st.session_state:
        st.session_state.show_processed_cvs = False
    if 'show_configuration' not in st.session_state:
        st.session_state.show_configuration = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False

def render_authentication():
    """Rendu de la page d'authentification"""
    st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    ">
        <div style="
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
        ">
            <h1 style="color: #333; margin-bottom: 2rem;">🏛️ TalentScope</h1>
            <p style="color: #666; margin-bottom: 2rem;">Ministère de l'Économie et des Finances</p>
            
            <form>
                <div style="margin-bottom: 1rem;">
                    <input type="text" placeholder="Nom d'utilisateur" style="
                        width: 100%;
                        padding: 0.75rem;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        font-size: 1rem;
                    ">
                </div>
                <div style="margin-bottom: 2rem;">
                    <input type="password" placeholder="Mot de passe" style="
                        width: 100%;
                        padding: 0.75rem;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        font-size: 1rem;
                    ">
                </div>
                <button type="submit" style="
                    width: 100%;
                    padding: 0.75rem;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 1rem;
                    cursor: pointer;
                ">Se connecter</button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulation d'authentification
    if st.button("Se connecter (Demo)", type="primary"):
        st.session_state.authenticated = True
        st.session_state.show_home = True
        st.rerun()

def render_home_page():
    """Rendu de la page d'accueil"""
    HeaderComponent.render()
    
    # Métriques principales
    st.markdown("## 📊 Vue d'ensemble")
    MetricsDashboard.render_main_metrics()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Actions rapides
    QuickActions.render()
    
    # Graphiques de tendances
    st.markdown("## 📈 Tendances des 7 derniers jours")
    
    sample_data = get_sample_data()
    trend_chart = ChartFactory.create_trend_chart(
        sample_data['trend_data'], 
        "Évolution des Analyses et Scores"
    )
    st.plotly_chart(trend_chart, use_container_width=True)
    
    # Deux colonnes pour les analyses détaillées
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 📋 Dernières Analyses")
        
        cv_data = get_sample_cv_data()
        for cv in cv_data[:4]:  # Afficher les 4 premiers
            CVCard(
                name=cv['name'],
                score=cv['score'],
                status=cv['status'],
                position=cv['position'],
                skills=cv['skills'],
                date=cv['date']
            ).render()
    
    with col2:
        st.markdown("## 🎯 Compétences les Plus Demandées")
        
        skills_chart = ChartFactory.create_skills_radar(
            sample_data['skills_data'],
            "Top Compétences Demandées"
        )
        st.plotly_chart(skills_chart, use_container_width=True)
    
    # Conseils d'optimisation
    TipsSection.render()
    
    # Informations système
    SystemInfo.render()

def render_dashboard_page():
    """Rendu de la page dashboard complet"""
    HeaderComponent.render()
    
    st.markdown("## 📊 Dashboard Complet")
    
    # Filtres avancés
    sample_df = pd.DataFrame(get_sample_cv_data())
    filter_component = FilterComponent(sample_df)
    filters = filter_component.render()
    
    # Métriques détaillées
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.plotly_chart(
            ChartFactory.create_gauge_chart(78.5, "Score Moyen"),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            ChartFactory.create_gauge_chart(23, "CVs Excellents"),
            use_container_width=True
        )
    
    with col3:
        st.plotly_chart(
            ChartFactory.create_gauge_chart(8, "Analyses Aujourd'hui"),
            use_container_width=True
        )
    
    with col4:
        st.plotly_chart(
            ChartFactory.create_gauge_chart(156, "Total CVs"),
            use_container_width=True
        )
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribution des Scores")
        distribution_chart = ChartFactory.create_distribution_chart(
            get_sample_data()['cv_scores']
        )
        st.plotly_chart(distribution_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 📅 Timeline des Analyses")
        timeline_chart = ChartFactory.create_timeline_chart(
            get_sample_data()['timeline_data']
        )
        st.plotly_chart(timeline_chart, use_container_width=True)
    
    # Tableau détaillé des CVs
    st.markdown("### 📋 Liste Détaillée des CVs")
    
    # Ajouter des colonnes pour les actions
    cv_df = sample_df.copy()
    cv_df['Actions'] = 'Voir détails'
    
    st.dataframe(
        cv_df[['name', 'score', 'status', 'position', 'date', 'Actions']],
        use_container_width=True,
        hide_index=True
    )

def render_analysis_page():
    """Rendu de la page d'analyse"""
    HeaderComponent.render()
    
    st.markdown("## 🔍 Analyse des CVs")
    
    # Indicateur de progression
    steps = ["Saisie de l'offre", "Importation des CVs", "Vérification", "Résultats"]
    progress = ProgressIndicator(steps, st.session_state.get('current_page', 1))
    progress.render()
    
    # Interface d'analyse (simplifiée pour la démo)
    if st.session_state.get('current_page', 1) == 1:
        st.markdown("### 📝 Étape 1: Saisie de l'offre d'emploi")
        job_description = st.text_area(
            "Description du poste",
            placeholder="Exemple: Développeur Python senior avec 5 ans d'expérience...",
            height=200
        )
        
        if st.button("Suivant", type="primary"):
            st.session_state.current_page = 2
            st.rerun()
    
    elif st.session_state.get('current_page', 1) == 2:
        st.markdown("### 📁 Étape 2: Importation des CVs")
        uploaded_files = st.file_uploader(
            "Choisir les fichiers CV",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} fichier(s) importé(s)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Précédent"):
                st.session_state.current_page = 1
                st.rerun()
        with col2:
            if st.button("Suivant", type="primary"):
                st.session_state.current_page = 3
                st.rerun()
    
    elif st.session_state.get('current_page', 1) == 3:
        st.markdown("### ✅ Étape 3: Vérification des données")
        st.info("Vérification en cours...")
        
        # Simulation de la vérification
        import time
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
            time.sleep(0.01)
        
        st.success("✅ Vérification terminée!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Précédent"):
                st.session_state.current_page = 2
                st.rerun()
        with col2:
            if st.button("Commencer l'analyse", type="primary"):
                st.session_state.current_page = 4
                st.rerun()
    
    elif st.session_state.get('current_page', 1) == 4:
        st.markdown("### 📊 Étape 4: Résultats de l'analyse")
        
        # Afficher les résultats
        cv_data = get_sample_cv_data()
        for cv in cv_data:
            CVCard(
                name=cv['name'],
                score=cv['score'],
                status=cv['status'],
                position=cv['position'],
                skills=cv['skills']
            ).render()
        
        if st.button("Nouvelle analyse", type="primary"):
            st.session_state.current_page = 1
            st.rerun()

def render_comparison_page():
    """Rendu de la page de comparaison"""
    HeaderComponent.render()
    
    st.markdown("## ⚖️ Comparaison des CVs")
    
    # Sélection des CVs à comparer
    cv_data = get_sample_cv_data()
    cv_names = [cv['name'] for cv in cv_data]
    
    selected_cvs = st.multiselect(
        "Sélectionner les CVs à comparer",
        cv_names,
        default=cv_names[:3]
    )
    
    if selected_cvs:
        # Données de comparaison
        comparison_data = {}
        for cv in cv_data:
            if cv['name'] in selected_cvs:
                comparison_data[cv['name']] = [
                    cv['score'],  # Score total
                    cv['score'] * 0.8,  # Compétences techniques
                    cv['score'] * 0.6,  # Expérience
                    cv['score'] * 0.7   # Éducation
                ]
        
        # Graphique de comparaison
        comparison_chart = ChartFactory.create_comparison_chart(
            comparison_data,
            "Comparaison des Scores par Critère"
        )
        st.plotly_chart(comparison_chart, use_container_width=True)
        
        # Tableau de comparaison
        comparison_df = pd.DataFrame(comparison_data).T
        comparison_df.columns = ['Score Total', 'Compétences', 'Expérience', 'Éducation']
        st.dataframe(comparison_df, use_container_width=True)

def render_processed_cvs_page():
    """Rendu de la page des CVs traités"""
    HeaderComponent.render()
    
    st.markdown("## 📁 CVs Traités")
    
    # Filtres
    filter_component = FilterComponent(pd.DataFrame(get_sample_cv_data()))
    filters = filter_component.render()
    
    # Liste des CVs
    cv_data = get_sample_cv_data()
    for cv in cv_data:
        with st.expander(f"📄 {cv['name']} - {cv['score']}%", expanded=False):
            CVCard(
                name=cv['name'],
                score=cv['score'],
                status=cv['status'],
                position=cv['position'],
                skills=cv['skills'],
                date=cv['date']
            ).render(show_skills=True)

def render_configuration_page():
    """Rendu de la page de configuration"""
    HeaderComponent.render()
    
    st.markdown("## ⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Interface")
        theme = st.selectbox("Thème", ["Clair", "Sombre", "Auto"])
        language = st.selectbox("Langue", ["Français", "Anglais"])
    
    with col2:
        st.markdown("### 🔧 Algorithme")
        st.slider("Poids des compétences techniques", 0.0, 1.0, 0.25)
        st.slider("Poids de l'expérience", 0.0, 1.0, 0.15)
        st.slider("Poids de l'éducation", 0.0, 1.0, 0.10)
    
    if st.button("💾 Sauvegarder la configuration", type="primary"):
        st.success("✅ Configuration sauvegardée!")

def render_profile_page():
    """Rendu de la page de profil"""
    HeaderComponent.render()
    
    st.markdown("## 👤 Mon Profil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Informations personnelles")
        st.text_input("Nom", value="Utilisateur")
        st.text_input("Email", value="user@ministere.gouv.fr")
        st.text_input("Département", value="Ministère de l'Économie et des Finances")
    
    with col2:
        st.markdown("### Préférences")
        st.selectbox("Langue préférée", ["Français", "Anglais"])
        st.selectbox("Thème préféré", ["Clair", "Sombre", "Auto"])
        st.checkbox("Notifications par email", value=True)

def main():
    """Fonction principale"""
    init_session_state()
    
    # Vérification de l'authentification
    if not st.session_state.authenticated:
        render_authentication()
        return
    
    # Navigation sidebar
    navigation = SidebarNavigation()
    navigation.render()
    
    # Rendu du contenu principal selon la page sélectionnée
    if st.session_state.get('show_home', True):
        render_home_page()
    elif st.session_state.get('show_dashboard', False):
        render_dashboard_page()
    elif st.session_state.get('show_analysis', False):
        render_analysis_page()
    elif st.session_state.get('show_comparison', False):
        render_comparison_page()
    elif st.session_state.get('show_processed_cvs', False):
        render_processed_cvs_page()
    elif st.session_state.get('show_configuration', False):
        render_configuration_page()
    elif st.session_state.get('show_profile', False):
        render_profile_page()
    else:
        render_home_page()

if __name__ == "__main__":
    main()
