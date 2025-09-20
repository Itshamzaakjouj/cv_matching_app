"""
Composants de métriques et cartes pour TalentScope
"""
import streamlit as st
from typing import Dict, List, Optional, Tuple
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class MetricCard:
    """Classe pour créer des cartes de métriques stylisées"""
    
    def __init__(self, title: str, value: str, change: str = None, 
                 change_type: str = "positive", icon: str = "📊"):
        self.title = title
        self.value = value
        self.change = change
        self.change_type = change_type
        self.icon = icon
    
    def render(self, variant: str = "primary"):
        """Rendu de la carte de métrique"""
        change_color = "#90EE90" if self.change_type == "positive" else "#FFB6C1"
        
        st.markdown(f"""
        <div class="metric-card {variant}">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{self.icon}</span>
                <p class="metric-value">{self.value}</p>
            </div>
            <p class="metric-label">{self.title}</p>
            {f'<small class="metric-change" style="color: {change_color};">{self.change}</small>' if self.change else ''}
        </div>
        """, unsafe_allow_html=True)

class MetricsDashboard:
    """Dashboard de métriques principal"""
    
    @staticmethod
    @st.cache_data
    def get_analytics_data() -> Dict:
        """Récupère les données d'analytics"""
        return {
            'total_cvs': 156,
            'avg_score': 78.5,
            'excellent_cvs': 23,
            'today_analyses': 8,
            'weekly_change': {
                'cvs': 12,
                'score': 2.3,
                'excellent': 5,
                'analyses': 3
            }
        }
    
    @staticmethod
    def render_main_metrics():
        """Affiche les métriques principales"""
        data = MetricsDashboard.get_analytics_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            MetricCard(
                title="CVs Analysés",
                value=str(data['total_cvs']),
                change=f"↗ +{data['weekly_change']['cvs']} cette semaine",
                change_type="positive",
                icon="📄"
            ).render("primary")
        
        with col2:
            MetricCard(
                title="Score Moyen",
                value=f"{data['avg_score']}%",
                change=f"↗ +{data['weekly_change']['score']}%",
                change_type="positive",
                icon="📊"
            ).render("danger")
        
        with col3:
            MetricCard(
                title="CVs Excellents",
                value=str(data['excellent_cvs']),
                change=f"↗ +{data['weekly_change']['excellent']}",
                change_type="positive",
                icon="⭐"
            ).render("success")
        
        with col4:
            MetricCard(
                title="Analyses Aujourd'hui",
                value=str(data['today_analyses']),
                change=f"↗ +{data['weekly_change']['analyses']}",
                change_type="positive",
                icon="⚡"
            ).render("warning")

class CVCard:
    """Carte pour afficher les informations d'un CV"""
    
    def __init__(self, name: str, score: float, status: str, position: str, 
                 skills: List[str] = None, date: str = None):
        self.name = name
        self.score = score
        self.status = status
        self.position = position
        self.skills = skills or []
        self.date = date or datetime.now().strftime("%d/%m/%Y")
    
    def get_status_class(self) -> str:
        """Retourne la classe CSS selon le score"""
        if self.score >= 85:
            return "excellent"
        elif self.score >= 70:
            return "good"
        else:
            return "average"
    
    def render(self, show_skills: bool = True):
        """Rendu de la carte CV"""
        status_class = self.get_status_class()
        
        skills_html = ""
        if show_skills and self.skills:
            skills_html = f"""
            <div style="margin-top: 0.5rem;">
                <small style="color: #6c757d;">Compétences: {', '.join(self.skills[:3])}</small>
            </div>
            """
        
        st.markdown(f"""
        <div class="cv-card">
            <div class="cv-card-header">
                <div>
                    <p class="cv-card-title">📄 {self.name}</p>
                    <p class="cv-card-subtitle">{self.position}</p>
                    <small style="color: #6c757d;">{self.date}</small>
                </div>
                <div class="cv-card-score">
                    <div class="cv-score-value">{self.score}%</div>
                    <span class="status-{status_class}">{self.status}</span>
                </div>
            </div>
            {skills_html}
        </div>
        """, unsafe_allow_html=True)

class ProgressIndicator:
    """Indicateur de progression pour les étapes"""
    
    def __init__(self, steps: List[str], current_step: int = 1):
        self.steps = steps
        self.current_step = current_step
    
    def render(self):
        """Rendu de l'indicateur de progression"""
        progress = (self.current_step / len(self.steps)) * 100
        
        steps_html = ""
        for i, step in enumerate(self.steps, 1):
            is_active = i <= self.current_step
            color = "#1976D2" if is_active else "#64748b"
            steps_html += f'<span style="color: {color}; font-weight: {"bold" if is_active else "normal"};">{step}</span>'
            if i < len(self.steps):
                steps_html += " → "
        
        st.markdown(f"""
        <div style="
            padding: 1rem;
            margin-bottom: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        ">
            <div style="
                width: 100%;
                background-color: #e0e0e0;
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 1rem;
            ">
                <div style="
                    width: {progress}%;
                    height: 8px;
                    background: linear-gradient(90deg, #1976D2, #2196F3);
                    transition: width 0.3s ease;
                "></div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                margin-top: 0.5rem;
                color: #64748b;
                font-size: 0.875rem;
            ">
                {steps_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

class QuickActions:
    """Composant pour les actions rapides"""
    
    @staticmethod
    def render():
        """Affiche les actions rapides"""
        st.markdown("## ⚡ Actions Rapides")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Nouvelle Analyse", use_container_width=True, type="primary"):
                st.session_state.show_analysis = True
                st.session_state.current_page = 1
                st.rerun()
        
        with col2:
            if st.button("📊 Dashboard Complet", use_container_width=True):
                st.session_state.show_dashboard = True
                st.rerun()
        
        with col3:
            if st.button("⚖️ Comparer CVs", use_container_width=True):
                st.session_state.show_comparison = True
                st.rerun()

class SystemInfo:
    """Informations système"""
    
    @staticmethod
    def render():
        """Affiche les informations système"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Version**: 1.0.0")
        with col2:
            st.markdown("**Dernière MAJ**: 18/09/2024")
        with col3:
            st.markdown("**Performance**: ⚡ Excellente")

class TipsSection:
    """Section de conseils d'optimisation"""
    
    @staticmethod
    def render():
        """Affiche les conseils d'optimisation"""
        st.markdown("## 💡 Conseils d'Optimisation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **🎯 Mots-clés pertinents**: Utilisez des termes techniques précis
            - Python, scikit-learn, pandas
            - Machine Learning, Deep Learning
            - SQL, PostgreSQL, MongoDB
            """)
        
        with col2:
            st.success("""
            **📊 Quantifiez vos résultats**: Mentionnez des chiffres concrets
            - "Amélioration de 25% des performances"
            - "Gestion de 10,000+ enregistrements"
            - "Réduction de 40% du temps de traitement"
            """)

@st.cache_data
def get_sample_cv_data() -> List[Dict]:
    """Génère des données d'exemple pour les CVs"""
    return [
        {
            "name": "cv_Hamza.pdf",
            "score": 91.3,
            "status": "Excellent",
            "position": "Data Scientist",
            "skills": ["Python", "Machine Learning", "TensorFlow"],
            "date": "18/09/2024"
        },
        {
            "name": "cv_Sophia.pdf",
            "score": 76.1,
            "status": "Très bon",
            "position": "Développeur Python",
            "skills": ["Python", "Django", "PostgreSQL"],
            "date": "17/09/2024"
        },
        {
            "name": "cv_Adam.pdf",
            "score": 85.2,
            "status": "Excellent",
            "position": "Analyste Data",
            "skills": ["Python", "Pandas", "SQL"],
            "date": "16/09/2024"
        },
        {
            "name": "cv_Ali.pdf",
            "score": 72.8,
            "status": "Bon",
            "position": "Ingénieur ML",
            "skills": ["Python", "Scikit-learn", "Docker"],
            "date": "15/09/2024"
        }
    ]
