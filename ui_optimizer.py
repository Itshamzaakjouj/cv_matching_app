"""
Optimiseur d'interface utilisateur pour TalentScope
Améliore les performances de rendu et la réactivité
"""

import streamlit as st
import time
from typing import Any, Callable, Dict, List
from performance_optimizer import RenderOptimizer, MemoryManager

class UIOptimizer:
    """Classe pour optimiser le rendu de l'interface utilisateur"""
    
    @staticmethod
    def render_loading_state(component_name: str, loading_text: str = "Chargement..."):
        """Affiche un état de chargement pendant le rendu d'un composant"""
        with st.spinner(f"{loading_text} {component_name}..."):
            time.sleep(0.1)  # Petite pause pour éviter le scintillement
    
    @staticmethod
    def lazy_render_component(component_func: Callable, *args, **kwargs):
        """Rend un composant de manière paresseuse"""
        component_key = f"rendered_{component_func.__name__}"
        
        if component_key not in st.session_state:
            with st.spinner("Chargement du composant..."):
                st.session_state[component_key] = component_func(*args, **kwargs)
        
        return st.session_state[component_key]
    
    @staticmethod
    def conditional_render(condition: bool, component_func: Callable, *args, **kwargs):
        """Rend un composant seulement si la condition est vraie"""
        if condition:
            return component_func(*args, **kwargs)
        return None
    
    @staticmethod
    def batch_render_components(components: List[Dict[str, Any]]):
        """Rend plusieurs composants par lots pour optimiser les performances"""
        for i, component in enumerate(components):
            if component.get('condition', True):
                component['func'](*component.get('args', []), **component.get('kwargs', {}))
            
            # Petite pause entre les composants pour éviter de bloquer l'interface
            if i % 5 == 0:
                time.sleep(0.01)

class ChartOptimizer:
    """Optimiseur pour les graphiques et visualisations"""
    
    @staticmethod
    def optimize_plotly_config():
        """Configuration optimisée pour Plotly"""
        return {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'chart',
                'height': 500,
                'width': 700,
                'scale': 1
            }
        }
    
    @staticmethod
    def create_lightweight_chart(data, chart_type="bar"):
        """Crée un graphique léger pour de meilleures performances"""
        import plotly.express as px
        
        if chart_type == "bar":
            fig = px.bar(data, x='x', y='y')
        elif chart_type == "line":
            fig = px.line(data, x='x', y='y')
        elif chart_type == "scatter":
            fig = px.scatter(data, x='x', y='y')
        else:
            fig = px.bar(data, x='x', y='y')
        
        # Optimiser la configuration
        fig.update_layout(
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        
        return fig

class SidebarOptimizer:
    """Optimiseur pour la sidebar"""
    
    @staticmethod
    def render_optimized_sidebar():
        """Rend une sidebar optimisée"""
        with st.sidebar:
            st.markdown("### 🚀 TalentScope Optimisé")
            
            # Métriques de performance
            if st.checkbox("📊 Afficher les stats de performance"):
                MemoryManager.cleanup_session_state()
                memory_usage = MemoryManager.get_memory_usage()
                st.metric("Utilisation mémoire", f"{memory_usage:.1f} MB")
                
                # Afficher les stats du cache
                if 'performance_cache' in st.session_state:
                    cache_size = len(st.session_state.performance_cache)
                    st.metric("Taille du cache", f"{cache_size} entrées")
            
            # Bouton de nettoyage
            if st.button("🧹 Nettoyer le cache"):
                MemoryManager.cleanup_session_state()
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

class DataTableOptimizer:
    """Optimiseur pour les tableaux de données"""
    
    @staticmethod
    def render_optimized_dataframe(df, max_rows=100):
        """Rend un DataFrame optimisé"""
        if len(df) > max_rows:
            st.warning(f"Affichage des {max_rows} premières lignes sur {len(df)}")
            df = df.head(max_rows)
        
        # Optimiser le DataFrame
        from optimized_data_functions import optimize_dataframe_performance
        df_optimized = optimize_dataframe_performance(df.copy())
        
        return st.dataframe(df_optimized, use_container_width=True)
    
    @staticmethod
    def render_paginated_table(df, page_size=20):
        """Rend un tableau avec pagination"""
        total_pages = (len(df) - 1) // page_size + 1
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Précédent") and st.session_state.current_page > 0:
                st.session_state.current_page -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"Page {st.session_state.current_page + 1} sur {total_pages}")
        
        with col3:
            if st.button("➡️ Suivant") and st.session_state.current_page < total_pages - 1:
                st.session_state.current_page += 1
                st.rerun()
        
        # Afficher la page actuelle
        start_idx = st.session_state.current_page * page_size
        end_idx = start_idx + page_size
        page_df = df.iloc[start_idx:end_idx]
        
        return st.dataframe(page_df, use_container_width=True)

# CSS optimisé pour de meilleures performances
OPTIMIZED_CSS = """
<style>
/* Optimisations CSS pour de meilleures performances */
.stApp {
    background-color: #f8f9fa;
}

/* Réduire les animations pour de meilleures performances */
* {
    animation-duration: 0.2s !important;
    transition-duration: 0.2s !important;
}

/* Optimiser le rendu des graphiques */
.plotly-graph-div {
    will-change: transform;
}

/* Masquer les éléments non essentiels */
.stDeployButton {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Optimiser les colonnes */
.stColumn {
    min-height: 0;
}

/* Optimiser les boutons */
.stButton > button {
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Optimiser les métriques */
.metric-container {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}

/* Optimiser les cartes */
.card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Loading states */
.loading {
    opacity: 0.6;
    pointer-events: none;
}

/* Optimiser les tableaux */
.dataframe {
    font-size: 0.9rem;
}

/* Optimiser les sidebar */
.stSidebar {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}

/* Optimiser les alertes */
.stAlert {
    border-radius: 8px;
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
"""

def apply_optimized_styling():
    """Applique le style CSS optimisé"""
    st.markdown(OPTIMIZED_CSS, unsafe_allow_html=True)
