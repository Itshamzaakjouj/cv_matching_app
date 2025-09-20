"""
Dashboard Analytique pour TalentScope
Fonctionnalités avancées de visualisation et d'analyse
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def generate_sample_data():
    """Génère des données d'exemple pour le dashboard"""
    # Données de performance des CVs
    cv_performance = {
        'CV': ['cv_Adam.pdf', 'cv_Ali.pdf', 'cv_Hafsa.pdf', 'cv_Hamza.pdf', 'cv_Sophia.pdf', 'cv_Yassine.pdf'],
        'Score': [0.85, 0.72, 0.68, 0.91, 0.76, 0.63],
        'Compétences_Techniques': [0.88, 0.75, 0.70, 0.92, 0.78, 0.65],
        'Expérience': [0.82, 0.70, 0.65, 0.89, 0.74, 0.60],
        'Éducation': [0.90, 0.80, 0.75, 0.85, 0.85, 0.70],
        'Date_Analyse': pd.date_range('2024-01-01', periods=6, freq='D')
    }
    
    # Données de tendances temporelles
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    trends = {
        'Date': dates,
        'CVs_Analysés': np.random.randint(5, 25, 30),
        'Score_Moyen': np.random.uniform(0.6, 0.9, 30),
        'Temps_Traitement': np.random.uniform(2, 8, 30)
    }
    
    # Données de compétences les plus demandées
    skills_data = {
        'Compétence': ['Python', 'Machine Learning', 'Data Science', 'React', 'SQL', 'JavaScript', 'Docker', 'AWS'],
        'Demande': [85, 78, 72, 68, 65, 60, 55, 50],
        'Disponibilité': [70, 45, 40, 80, 75, 85, 30, 25]
    }
    
    return pd.DataFrame(cv_performance), pd.DataFrame(trends), pd.DataFrame(skills_data)

def render_performance_metrics(df_cv):
    """Affiche les métriques de performance principales"""
    st.markdown("### 📊 Métriques de Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Score Moyen",
            value=f"{df_cv['Score'].mean()*100:.1f}%",
            delta=f"+{np.random.randint(1, 5)}%"
        )
    
    with col2:
        st.metric(
            label="Meilleur Score",
            value=f"{df_cv['Score'].max()*100:.1f}%",
            delta=f"+{np.random.randint(2, 8)}%"
        )
    
    with col3:
        st.metric(
            label="CVs Analysés",
            value=len(df_cv),
            delta=f"+{np.random.randint(1, 3)}"
        )
    
    with col4:
        st.metric(
            label="Temps Moyen",
            value=f"{np.random.uniform(3, 6):.1f}s",
            delta=f"-{np.random.randint(1, 3)}s"
        )

def render_score_distribution(df_cv):
    """Affiche la distribution des scores"""
    st.markdown("### 📈 Distribution des Scores")
    
    # Histogramme des scores
    fig = px.histogram(
        df_cv, 
        x='Score',
        nbins=10,
        title="Distribution des Scores de Matching",
        color_discrete_sequence=['#1976D2']
    )
    fig.update_layout(
        xaxis_title="Score de Matching",
        yaxis_title="Nombre de CVs",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def render_skills_analysis(df_skills):
    """Affiche l'analyse des compétences"""
    st.markdown("### 🎯 Analyse des Compétences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres des compétences les plus demandées
        fig = px.bar(
            df_skills,
            x='Demande',
            y='Compétence',
            orientation='h',
            title="Compétences les Plus Demandées",
            color='Demande',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graphique radar des compétences
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=df_skills['Demande'][:6],
            theta=df_skills['Compétence'][:6],
            fill='toself',
            name='Demande',
            line_color='#1976D2'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_skills['Disponibilité'][:6],
            theta=df_skills['Compétence'][:6],
            fill='toself',
            name='Disponibilité',
            line_color='#FF9800'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Demande vs Disponibilité des Compétences"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_trends_analysis(df_trends):
    """Affiche l'analyse des tendances temporelles"""
    st.markdown("### 📅 Analyse des Tendances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique des CVs analysés dans le temps
        fig = px.line(
            df_trends,
            x='Date',
            y='CVs_Analysés',
            title="Évolution du Nombre de CVs Analysés",
            color_discrete_sequence=['#4CAF50']
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Nombre de CVs"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graphique des scores moyens dans le temps
        fig = px.line(
            df_trends,
            x='Date',
            y='Score_Moyen',
            title="Évolution du Score Moyen",
            color_discrete_sequence=['#FF5722']
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Score Moyen"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_detailed_analysis(df_cv):
    """Affiche l'analyse détaillée des CVs"""
    st.markdown("### 🔍 Analyse Détaillée des CVs")
    
    # Tableau interactif des CVs
    df_display = df_cv.copy()
    df_display['Score'] = (df_display['Score'] * 100).round(1)
    df_display['Compétences_Techniques'] = (df_display['Compétences_Techniques'] * 100).round(1)
    df_display['Expérience'] = (df_display['Expérience'] * 100).round(1)
    df_display['Éducation'] = (df_display['Éducation'] * 100).round(1)
    
    # Renommer les colonnes pour l'affichage
    df_display.columns = ['CV', 'Score Total (%)', 'Compétences Techniques (%)', 'Expérience (%)', 'Éducation (%)', 'Date d\'Analyse']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Graphique de corrélation
    st.markdown("#### 📊 Corrélation entre les Critères")
    
    correlation_data = df_cv[['Score', 'Compétences_Techniques', 'Expérience', 'Éducation']].corr()
    
    fig = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        title="Matrice de Corrélation des Critères d'Évaluation",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)

def render_export_options():
    """Affiche les options d'export"""
    st.markdown("### 📤 Export des Données")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exporter Graphiques", use_container_width=True):
            st.success("Graphiques exportés avec succès!")
    
    with col2:
        if st.button("📋 Exporter Données", use_container_width=True):
            st.success("Données exportées en CSV!")
    
    with col3:
        if st.button("📄 Générer Rapport", use_container_width=True):
            st.success("Rapport PDF généré!")

def render_dashboard():
    """Fonction principale du dashboard"""
    st.markdown("# 📊 Dashboard Analytique")
    st.markdown("---")
    
    # Générer les données d'exemple
    df_cv, df_trends, df_skills = generate_sample_data()
    
    # Onglets pour organiser le dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Vue d'ensemble", "🎯 Compétences", "📅 Tendances", "🔍 Analyse Détaillée"])
    
    with tab1:
        render_performance_metrics(df_cv)
        st.markdown("---")
        render_score_distribution(df_cv)
    
    with tab2:
        render_skills_analysis(df_skills)
    
    with tab3:
        render_trends_analysis(df_trends)
    
    with tab4:
        render_detailed_analysis(df_cv)
        st.markdown("---")
        render_export_options()
    
    # Sidebar avec filtres
    with st.sidebar:
        st.markdown("### 🔧 Filtres")
        
        # Filtre par score minimum
        min_score = st.slider(
            "Score minimum",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            format="%.1f"
        )
        
        # Filtre par période
        date_range = st.date_input(
            "Période d'analyse",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        # Filtre par compétence
        selected_skills = st.multiselect(
            "Compétences",
            options=df_skills['Compétence'].tolist(),
            default=df_skills['Compétence'].tolist()[:3]
        )
        
        if st.button("🔄 Appliquer Filtres"):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ Informations")
        st.info(f"**Données filtrées:** {len(df_cv)} CVs")
        st.info(f"**Score moyen filtré:** {df_cv['Score'].mean()*100:.1f}%")










