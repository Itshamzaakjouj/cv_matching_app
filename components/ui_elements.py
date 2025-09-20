"""
Composants d'interface utilisateur pour TalentScope
"""
import streamlit as st
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime
import base64

class HeaderComponent:
    """Composant d'en-tête principal"""
    
    @staticmethod
    def render(title: str = "TalentScope", subtitle: str = "Ministère de l'Économie et des Finances"):
        """Rendu de l'en-tête principal"""
        st.markdown(f"""
        <div class="header-container">
            <h1>🏛️ {title} - {subtitle}</h1>
            <p>Plateforme intelligente de matching CVs et offres d'emploi</p>
        </div>
        """, unsafe_allow_html=True)

class SidebarNavigation:
    """Navigation sidebar améliorée"""
    
    def __init__(self):
        self.pages = [
            {"key": "home", "label": "🏠 Accueil", "icon": "🏠"},
            {"key": "dashboard", "label": "📈 Dashboard", "icon": "📈"},
            {"key": "analysis", "label": "🔍 Analyse", "icon": "🔍"},
            {"key": "comparison", "label": "📋 Comparaison", "icon": "📋"},
            {"key": "processed_cvs", "label": "📁 CVs Traités", "icon": "📁"},
            {"key": "configuration", "label": "⚙️ Configuration", "icon": "⚙️"}
        ]
    
    def render(self):
        """Rendu de la navigation sidebar"""
        with st.sidebar:
            st.markdown("## 📊 Navigation")
            
            for page in self.pages:
                if st.button(page["label"], use_container_width=True, key=f"nav_{page['key']}"):
                    st.session_state[f"show_{page['key']}"] = True
                    # Désactiver les autres pages
                    for other_page in self.pages:
                        if other_page["key"] != page["key"]:
                            st.session_state[f"show_{other_page['key']}"] = False
                    st.rerun()
            
            st.markdown("---")
            st.markdown("## ℹ️ Informations Système")
            
            # Informations système avec design amélioré
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <p style="margin: 0; font-weight: bold;">Version: 1.0.0</p>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Statut: ✅ Opérationnel</p>
                <p style="margin: 0.5rem 0 0 0; color: #6c757d;">Performance: ⚡ Excellente</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Bouton de déconnexion
            if st.button("🚪 Déconnexion", use_container_width=True, type="secondary"):
                st.session_state.authenticated = False
                st.session_state.logged_in = False
                st.session_state.show_home = False
                # Redirection vers l'interface d'authentification moderne
                st.markdown("""
                <script>
                    window.location.href = 'http://localhost:8080/auth_interface.html';
                </script>
                """, unsafe_allow_html=True)
                st.rerun()

class FilterComponent:
    """Composant de filtrage avancé"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def render(self) -> Dict[str, Any]:
        """Rendu du composant de filtrage"""
        st.markdown("### 🔍 Filtres Avancés")
        
        col1, col2, col3 = st.columns(3)
        
        filters = {}
        
        with col1:
            if 'score' in self.data.columns:
                score_range = st.slider(
                    "Score minimum",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=1.0
                )
                filters['score'] = score_range
        
        with col2:
            if 'status' in self.data.columns:
                status_options = st.multiselect(
                    "Statut",
                    options=self.data['status'].unique(),
                    default=self.data['status'].unique()
                )
                filters['status'] = status_options
        
        with col3:
            if 'date' in self.data.columns:
                date_range = st.date_input(
                    "Période",
                    value=(self.data['date'].min(), self.data['date'].max()),
                    min_value=self.data['date'].min(),
                    max_value=self.data['date'].max()
                )
                filters['date'] = date_range
        
        return filters

class ModalComponent:
    """Composant modal pour les détails"""
    
    @staticmethod
    def render_cv_details(cv_data: Dict[str, Any]):
        """Rendu des détails d'un CV dans un modal"""
        with st.expander(f"📄 Détails - {cv_data.get('name', 'CV')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Informations générales**")
                st.write(f"**Nom:** {cv_data.get('name', 'N/A')}")
                st.write(f"**Score:** {cv_data.get('score', 'N/A')}%")
                st.write(f"**Statut:** {cv_data.get('status', 'N/A')}")
                st.write(f"**Poste:** {cv_data.get('position', 'N/A')}")
            
            with col2:
                st.markdown("**Compétences**")
                skills = cv_data.get('skills', [])
                if skills:
                    for skill in skills:
                        st.write(f"• {skill}")
                else:
                    st.write("Aucune compétence spécifiée")
            
            # Graphique de score par critère
            if 'criteria_scores' in cv_data:
                st.markdown("**Scores par critère**")
                criteria_data = cv_data['criteria_scores']
                st.bar_chart(criteria_data)

class ExportComponent:
    """Composant d'export des données"""
    
    @staticmethod
    def render_export_buttons(data: pd.DataFrame, filename: str = "talentscope_export"):
        """Rendu des boutons d'export"""
        st.markdown("### 📤 Export des Données")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export CSV
            csv = data.to_csv(index=False)
            st.download_button(
                label="📊 Télécharger CSV",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                data.to_excel(writer, index=False, sheet_name='Données')
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="📈 Télécharger Excel",
                data=excel_data,
                file_name=f"{filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            # Export JSON
            json_data = data.to_json(orient='records', indent=2)
            st.download_button(
                label="📋 Télécharger JSON",
                data=json_data,
                file_name=f"{filename}.json",
                mime="application/json"
            )

class NotificationComponent:
    """Composant de notifications"""
    
    @staticmethod
    def show_success(message: str):
        """Affiche une notification de succès"""
        st.success(f"✅ {message}")
    
    @staticmethod
    def show_error(message: str):
        """Affiche une notification d'erreur"""
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_warning(message: str):
        """Affiche une notification d'avertissement"""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info(message: str):
        """Affiche une notification d'information"""
        st.info(f"ℹ️ {message}")

class LoadingComponent:
    """Composant de chargement"""
    
    @staticmethod
    def render_spinner(message: str = "Chargement..."):
        """Affiche un spinner de chargement"""
        with st.spinner(message):
            st.markdown(f"""
            <div class="loading" style="
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <div style="text-align: center;">
                    <div class="loading"></div>
                    <p style="margin-top: 1rem; color: #6c757d;">{message}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

class SearchComponent:
    """Composant de recherche"""
    
    def __init__(self, placeholder: str = "Rechercher..."):
        self.placeholder = placeholder
    
    def render(self) -> str:
        """Rendu du composant de recherche"""
        return st.text_input(
            "🔍",
            placeholder=self.placeholder,
            key="search_input"
        )

class PaginationComponent:
    """Composant de pagination"""
    
    def __init__(self, total_items: int, items_per_page: int = 10):
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.total_pages = (total_items + items_per_page - 1) // items_per_page
    
    def render(self) -> int:
        """Rendu du composant de pagination"""
        if self.total_pages <= 1:
            return 1
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            page = st.selectbox(
                "Page",
                range(1, self.total_pages + 1),
                index=0,
                key="pagination_select"
            )
        
        return page

class TooltipComponent:
    """Composant de tooltips explicatifs"""
    
    @staticmethod
    def render_with_tooltip(element, tooltip_text: str):
        """Rendu d'un élément avec tooltip"""
        st.markdown(f"""
        <div style="position: relative; display: inline-block;">
            {element}
            <div style="
                visibility: hidden;
                width: 200px;
                background-color: #333;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            ">
                {tooltip_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

class ResponsiveGrid:
    """Grille responsive pour l'affichage"""
    
    @staticmethod
    def render_metrics_grid(metrics: List[Dict[str, Any]]):
        """Rendu d'une grille de métriques responsive"""
        if len(metrics) <= 4:
            cols = st.columns(len(metrics))
        else:
            cols = st.columns(4)
        
        for i, metric in enumerate(metrics):
            with cols[i % len(cols)]:
                MetricCard(
                    title=metric.get('title', ''),
                    value=metric.get('value', ''),
                    change=metric.get('change'),
                    change_type=metric.get('change_type', 'positive'),
                    icon=metric.get('icon', '📊')
                ).render(metric.get('variant', 'primary'))

# Import des dépendances nécessaires
import io
from .metrics import MetricCard
