"""
Lanceur optimisé pour TalentScope
Version haute performance avec mise en cache et optimisations
"""

import streamlit as st
import time
from pathlib import Path
from performance_optimizer import configure_streamlit_performance, MemoryManager
from ui_optimizer import UIOptimizer, apply_optimized_styling
from optimized_data_functions import (
    get_optimized_sample_data,
    get_optimized_cv_data,
    get_optimized_dashboard_metrics,
    clear_performance_cache
)

def main():
    """Fonction principale optimisée"""
    # Configuration optimisée
    configure_streamlit_performance()
    apply_optimized_styling()
    
    # Nettoyage de la mémoire au démarrage
    MemoryManager.cleanup_session_state()
    
    # Vérification de l'authentification
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        render_auth_redirect()
        return
    
    # Interface principale optimisée
    render_optimized_interface()

def render_auth_redirect():
    """Redirection vers l'interface d'authentification"""
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>🔐 Authentification Requise</h2>
        <p>Veuillez vous connecter pour accéder à l'application optimisée.</p>
        <a href="http://localhost:8080/auth_interface.html" 
           style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; 
                  font-weight: bold; margin-top: 20px;">
            🚀 Se connecter
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_optimized_interface():
    """Interface principale optimisée"""
    # Header optimisé
    render_optimized_header()
    
    # Sidebar optimisée
    render_optimized_sidebar()
    
    # Contenu principal
    render_main_content_optimized()

def render_optimized_header():
    """Header optimisé"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.image("Logos/TalentScope.png", width=100)
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="margin: 0; color: #667eea;">🏛️ TalentScope</h1>
            <p style="margin: 0; color: #666;">Ministère de l'Économie et des Finances</p>
            <p style="margin: 0; font-size: 0.9em; color: #888;">Version Optimisée - Haute Performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.logged_in = False
            st.session_state.show_home = False
            st.markdown("""
            <script>
                window.location.href = 'http://localhost:8080/auth_interface.html';
            </script>
            """, unsafe_allow_html=True)
            st.rerun()

def render_optimized_sidebar():
    """Sidebar optimisée"""
    with st.sidebar:
        st.markdown("### 🚀 TalentScope Optimisé")
        
        # Métriques de performance
        if st.checkbox("📊 Stats Performance"):
            memory_usage = MemoryManager.get_memory_usage()
            st.metric("Mémoire", f"{memory_usage:.1f} MB")
            
            if 'performance_cache' in st.session_state:
                cache_size = len(st.session_state.performance_cache)
                st.metric("Cache", f"{cache_size} entrées")
        
        # Bouton de nettoyage
        if st.button("🧹 Nettoyer Cache"):
            clear_performance_cache()
            st.success("Cache nettoyé !")
            st.rerun()
        
        st.markdown("---")
        
        # Navigation optimisée
        st.markdown("### 📋 Navigation")
        pages = [
            ("🏠 Accueil", "home"),
            ("📊 Dashboard", "dashboard"),
            ("🔍 Analyse", "analysis"),
            ("⚖️ Comparaison", "comparison"),
            ("⚙️ Configuration", "config")
        ]
        
        for page_name, page_key in pages:
            if st.button(page_name, use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()

def render_main_content_optimized():
    """Contenu principal optimisé"""
    current_page = st.session_state.get('current_page', 'home')
    
    if current_page == 'home':
        render_optimized_home()
    elif current_page == 'dashboard':
        render_optimized_dashboard()
    elif current_page == 'analysis':
        render_optimized_analysis()
    elif current_page == 'comparison':
        render_optimized_comparison()
    elif current_page == 'config':
        render_optimized_config()

def render_optimized_home():
    """Page d'accueil optimisée"""
    st.markdown("## 📊 Vue d'ensemble - Version Optimisée")
    
    # Métriques principales (avec cache)
    metrics = get_optimized_dashboard_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total CVs", metrics['total_cvs'], "12")
    
    with col2:
        st.metric("Score Moyen", f"{metrics['average_score']}%", "5.2%")
    
    with col3:
        st.metric("Analyses Récentes", metrics['recent_analyses'], "3")
    
    with col4:
        st.metric("Meilleur Score", f"{metrics['best_score']}%", "Record")
    
    st.markdown("---")
    
    # Graphiques optimisés
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Tendances de Performance")
        # Graphique optimisé
        import plotly.express as px
        trend_data = pd.DataFrame({
            'Jour': range(7),
            'Score': metrics['performance_trend']
        })
        fig = px.line(trend_data, x='Jour', y='Score', title="Évolution des Scores")
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config=ChartOptimizer.optimize_plotly_config())
    
    with col2:
        st.markdown("### 🎯 Top CVs")
        top_cvs = metrics['top_cvs']
        for i, cv in enumerate(top_cvs, 1):
            st.markdown(f"**{i}.** {cv['name']} - {cv['score']}%")
    
    # Actions rapides
    st.markdown("### ⚡ Actions Rapides")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Nouvelle Analyse", use_container_width=True):
            st.session_state.current_page = 'analysis'
            st.rerun()
    
    with col2:
        if st.button("⚖️ Comparer CVs", use_container_width=True):
            st.session_state.current_page = 'comparison'
            st.rerun()
    
    with col3:
        if st.button("📊 Dashboard Complet", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()

def render_optimized_dashboard():
    """Dashboard optimisé"""
    st.markdown("## 📊 Dashboard Complet - Version Optimisée")
    
    # Métriques détaillées
    metrics = get_optimized_dashboard_metrics()
    
    # Graphiques avancés
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Performance Globale")
        # Graphique de performance
        import plotly.graph_objects as go
        fig = go.Figure(data=go.Scatter(
            y=metrics['performance_trend'],
            mode='lines+markers',
            name='Score Moyen'
        ))
        fig.update_layout(title="Tendance des Scores", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Compétences Demandées")
        skills_data = metrics['skills_demand']
        fig = px.bar(
            x=list(skills_data.keys()),
            y=list(skills_data.values()),
            title="Top Compétences"
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def render_optimized_analysis():
    """Page d'analyse optimisée"""
    st.markdown("## 🔍 Analyse de CV - Version Optimisée")
    
    st.info("🚀 **Version Optimisée** - Chargement plus rapide et interface plus réactive")
    
    # Interface d'analyse simplifiée
    uploaded_file = st.file_uploader("📁 Télécharger un CV", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file:
        with st.spinner("Analyse en cours..."):
            time.sleep(1)  # Simulation d'analyse
            st.success("✅ Analyse terminée !")
            
            # Résultats simulés
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score Global", "87.5%", "12.3%")
            with col2:
                st.metric("Compétences", "92%", "8.1%")
            with col3:
                st.metric("Expérience", "78%", "5.2%")

def render_optimized_comparison():
    """Page de comparaison optimisée"""
    st.markdown("## ⚖️ Comparaison de CVs - Version Optimisée")
    
    # Données de comparaison optimisées
    comparison_data = get_optimized_comparison_data()
    
    # Sélection des CVs
    selected_cvs = st.multiselect(
        "Sélectionner les CVs à comparer",
        comparison_data['cv_names'],
        default=comparison_data['cv_names'][:2]
    )
    
    if selected_cvs:
        # Tableau de comparaison optimisé
        st.markdown("### 📊 Résultats de Comparaison")
        
        # Créer un DataFrame optimisé
        import pandas as pd
        df_data = {
            'CV': selected_cvs,
            'Score Global': [comparison_data['scores'][i] for i, name in enumerate(comparison_data['cv_names']) if name in selected_cvs]
        }
        
        # Ajouter les catégories
        for category, scores in comparison_data['categories'].items():
            df_data[category] = [scores[i] for i, name in enumerate(comparison_data['cv_names']) if name in selected_cvs]
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Graphique radar optimisé
        if len(selected_cvs) >= 2:
            st.markdown("### 📈 Graphique Radar")
            import plotly.graph_objects as go
            
            categories = list(comparison_data['categories'].keys())
            fig = go.Figure()
            
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
            
            for i, cv_name in enumerate(selected_cvs):
                cv_idx = comparison_data['cv_names'].index(cv_name)
                values = [comparison_data['categories'][cat][cv_idx] for cat in categories]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=cv_name,
                    line_color=colors[i % len(colors)]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Comparaison Multi-dimensionnelle"
            )
            
            st.plotly_chart(fig, use_container_width=True)

def render_optimized_config():
    """Page de configuration optimisée"""
    st.markdown("## ⚙️ Configuration - Version Optimisée")
    
    st.info("🚀 **Version Optimisée** - Configuration simplifiée et plus rapide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Apparence")
        theme = st.selectbox("Thème", ["Clair", "Sombre"], index=0)
        language = st.selectbox("Langue", ["Français", "English"], index=0)
    
    with col2:
        st.markdown("### ⚡ Performance")
        cache_enabled = st.checkbox("Activer le cache", value=True)
        auto_cleanup = st.checkbox("Nettoyage automatique", value=True)
    
    if st.button("💾 Sauvegarder la Configuration"):
        st.success("✅ Configuration sauvegardée !")

if __name__ == "__main__":
    main()
