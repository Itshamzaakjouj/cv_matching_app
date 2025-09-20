"""
Page de comparaison des CVs - TalentScope
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.ui_elements import HeaderComponent, FilterComponent
from components.charts import ChartFactory
from components.metrics import CVCard, get_sample_cv_data
from i18n import t

# Configuration de la page
st.set_page_config(
    page_title="TalentScope - Comparaison",
    page_icon="⚖️",
    layout="wide"
)

def render_comparison_interface():
    """Interface de comparaison des CVs"""
    HeaderComponent.render()
    
    st.markdown("## ⚖️ Comparaison des CVs")
    
    # Sélection des CVs à comparer
    cv_data = get_sample_cv_data()
    cv_names = [cv['name'] for cv in cv_data]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_cvs = st.multiselect(
            "Sélectionner les CVs à comparer",
            cv_names,
            default=cv_names[:3],
            help="Sélectionnez 2 à 5 CVs pour une comparaison optimale"
        )
    
    with col2:
        comparison_type = st.selectbox(
            "Type de comparaison",
            ["Score global", "Par critères", "Radar", "Timeline"]
        )
    
    if len(selected_cvs) < 2:
        st.warning("⚠️ Veuillez sélectionner au moins 2 CVs pour la comparaison")
        return
    
    if len(selected_cvs) > 5:
        st.warning("⚠️ Maximum 5 CVs recommandé pour une comparaison claire")
        selected_cvs = selected_cvs[:5]
    
    # Filtres avancés
    with st.expander("🔍 Filtres avancés", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_score = st.slider("Score minimum", 0, 100, 0)
        with col2:
            max_score = st.slider("Score maximum", 0, 100, 100)
        with col3:
            status_filter = st.multiselect("Statut", ["Excellent", "Très bon", "Bon", "Moyen"])
    
    # Données filtrées
    filtered_cvs = [cv for cv in cv_data if cv['name'] in selected_cvs]
    filtered_cvs = [cv for cv in filtered_cvs if min_score <= cv['score'] <= max_score]
    
    if status_filter:
        filtered_cvs = [cv for cv in filtered_cvs if cv['status'] in status_filter]
    
    if not filtered_cvs:
        st.error("❌ Aucun CV ne correspond aux critères sélectionnés")
        return
    
    # Affichage selon le type de comparaison
    if comparison_type == "Score global":
        render_global_comparison(filtered_cvs)
    elif comparison_type == "Par critères":
        render_criteria_comparison(filtered_cvs)
    elif comparison_type == "Radar":
        render_radar_comparison(filtered_cvs)
    elif comparison_type == "Timeline":
        render_timeline_comparison(filtered_cvs)
    
    # Tableau de comparaison détaillé
    render_detailed_table(filtered_cvs)
    
    # Actions d'export
    render_export_actions(filtered_cvs)

def render_global_comparison(cv_data):
    """Comparaison par score global"""
    st.markdown("### 📊 Comparaison des Scores Globaux")
    
    # Graphique en barres
    names = [cv['name'] for cv in cv_data]
    scores = [cv['score'] for cv in cv_data]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=scores,
            marker_color=colors[:len(names)],
            text=[f"{score}%" for score in scores],
            textposition='auto',
            hovertemplate="<b>%{x}</b><br>Score: %{y}%<extra></extra>"
        )
    ])
    
    fig.update_layout(
        title="Scores de Compatibilité",
        xaxis_title="CVs",
        yaxis_title="Score (%)",
        height=400,
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métriques de comparaison
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Meilleur score", f"{max(scores):.1f}%")
    with col2:
        st.metric("Score moyen", f"{sum(scores)/len(scores):.1f}%")
    with col3:
        st.metric("Écart type", f"{pd.Series(scores).std():.1f}")
    with col4:
        st.metric("CVs comparés", len(cv_data))

def render_criteria_comparison(cv_data):
    """Comparaison par critères"""
    st.markdown("### 🎯 Comparaison par Critères")
    
    # Données simulées pour les critères
    criteria_data = {}
    criteria_names = ['Compétences techniques', 'Expérience', 'Éducation', 'Compétences douces']
    
    for cv in cv_data:
        base_score = cv['score']
        criteria_scores = [
            base_score * 0.8,  # Compétences techniques
            base_score * 0.6,  # Expérience
            base_score * 0.7,  # Éducation
            base_score * 0.5   # Compétences douces
        ]
        criteria_data[cv['name']] = criteria_scores
    
    # Graphique en barres groupées
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (cv_name, scores) in enumerate(criteria_data.items()):
        fig.add_trace(go.Bar(
            name=cv_name,
            x=criteria_names,
            y=scores,
            marker_color=colors[i % len(colors)],
            hovertemplate=f"<b>{cv_name}</b><br>%{{x}}: %{{y}}%<extra></extra>"
        ))
    
    fig.update_layout(
        title="Scores par Critère",
        xaxis_title="Critères",
        yaxis_title="Score (%)",
        height=500,
        barmode='group',
        font=dict(family="Segoe UI, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_radar_comparison(cv_data):
    """Comparaison en graphique radar"""
    st.markdown("### 🎯 Comparaison Radar")
    
    # Données pour le radar
    skills = ['Python', 'Machine Learning', 'SQL', 'Git', 'Docker', 'JavaScript']
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, cv in enumerate(cv_data):
        # Générer des scores simulés pour les compétences
        base_score = cv['score']
        skill_scores = [
            base_score * 0.9,  # Python
            base_score * 0.8,  # Machine Learning
            base_score * 0.7,  # SQL
            base_score * 0.6,  # Git
            base_score * 0.5,  # Docker
            base_score * 0.4   # JavaScript
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=skill_scores,
            theta=skills,
            fill='toself',
            name=cv['name'],
            line_color=colors[i % len(colors)],
            fillcolor=f'rgba({colors[i % len(colors)][1:3]}, {colors[i % len(colors)][3:5]}, {colors[i % len(colors)][5:7]}, 0.3)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Comparaison des Compétences",
        height=500,
        font=dict(family="Segoe UI, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_timeline_comparison(cv_data):
    """Comparaison en timeline"""
    st.markdown("### 📅 Timeline de Comparaison")
    
    # Données simulées pour la timeline
    timeline_data = []
    for i, cv in enumerate(cv_data):
        timeline_data.append({
            'date': f"2024-09-{15 + i}",
            'cv_name': cv['name'],
            'score': cv['score'],
            'status': cv['status']
        })
    
    # Graphique timeline
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, data in enumerate(timeline_data):
        fig.add_trace(go.Scatter(
            x=[data['date'], data['date']],
            y=[0, 1],
            mode='lines+markers',
            name=data['cv_name'],
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=10, color=colors[i % len(colors)]),
            hovertemplate=f"<b>{data['cv_name']}</b><br>" +
                         f"Date: {data['date']}<br>" +
                         f"Score: {data['score']}%<br>" +
                         f"Statut: {data['status']}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Évolution des Scores",
        xaxis_title="Date",
        yaxis_title="",
        height=300,
        showlegend=True,
        font=dict(family="Segoe UI, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_detailed_table(cv_data):
    """Tableau de comparaison détaillé"""
    st.markdown("### 📋 Tableau de Comparaison Détaillé")
    
    # Préparer les données pour le tableau
    table_data = []
    for cv in cv_data:
        table_data.append({
            'CV': cv['name'],
            'Score Global': f"{cv['score']}%",
            'Statut': cv['status'],
            'Poste': cv['position'],
            'Compétences': ', '.join(cv['skills'][:3]),
            'Date': cv['date']
        })
    
    df = pd.DataFrame(table_data)
    
    # Afficher le tableau avec style
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score Global": st.column_config.ProgressColumn(
                "Score Global",
                help="Score de compatibilité",
                min_value=0,
                max_value=100,
            )
        }
    )

def render_export_actions(cv_data):
    """Actions d'export"""
    st.markdown("### 📤 Export des Résultats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exporter en CSV", use_container_width=True):
            df = pd.DataFrame(cv_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name="comparaison_cvs.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Exporter en Excel", use_container_width=True):
            df = pd.DataFrame(cv_data)
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Comparaison')
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="Télécharger Excel",
                data=excel_data,
                file_name="comparaison_cvs.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        if st.button("📄 Générer rapport PDF", use_container_width=True):
            st.info("Fonctionnalité PDF en cours de développement")

def main():
    """Fonction principale"""
    render_comparison_interface()

if __name__ == "__main__":
    main()
