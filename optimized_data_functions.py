"""
Fonctions de données optimisées pour TalentScope
Améliore les performances avec mise en cache et optimisations
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
from performance_optimizer import PerformanceOptimizer

@PerformanceOptimizer.cache_data(ttl=1800)  # Cache 30 minutes
def get_optimized_sample_data() -> Dict:
    """Version optimisée de get_sample_data avec cache"""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=7, freq='D')
    
    return {
        'trend_data': {
            'date': dates,
            'analyses': [12, 15, 8, 20, 18, 16, 8],
            'score': [75.2, 76.1, 72.8, 81.5, 79.3, 78.1, 80.2]
        },
        'skills_data': {
            'Python': 85,
            'Machine Learning': 78,
            'SQL': 72,
            'Git': 65,
            'Docker': 58,
            'JavaScript': 55,
            'React': 52,
            'AWS': 48
        },
        'cv_scores': [91.3, 76.1, 85.2, 72.8, 88.5, 69.2, 94.1, 81.7],
        'timeline_data': [
            {'date': '2024-09-15', 'cv_name': 'CV_Hamza.pdf', 'score': 91.3},
            {'date': '2024-09-16', 'cv_name': 'CV_Sophia.pdf', 'score': 76.1},
            {'date': '2024-09-17', 'cv_name': 'CV_Adam.pdf', 'score': 85.2},
            {'date': '2024-09-18', 'cv_name': 'CV_Ali.pdf', 'score': 72.8}
        ]
    }

@PerformanceOptimizer.cache_data(ttl=3600)  # Cache 1 heure
def get_optimized_cv_data() -> List[Dict]:
    """Version optimisée de get_sample_cv_data avec cache"""
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

@PerformanceOptimizer.cache_data(ttl=7200)  # Cache 2 heures
def get_optimized_dashboard_metrics() -> Dict:
    """Métriques du dashboard optimisées"""
    return {
        'total_cvs': 156,
        'average_score': 78.5,
        'recent_analyses': 12,
        'best_score': 94.2,
        'top_cvs': [
            {'name': 'CV_Anna.pdf', 'score': 94.2},
            {'name': 'CV_Hamza.pdf', 'score': 91.3},
            {'name': 'CV_Pierre.pdf', 'score': 88.7}
        ],
        'performance_trend': [75, 78, 76, 82, 79, 85, 78],
        'skills_demand': {
            'Python': 85,
            'Machine Learning': 78,
            'SQL': 72,
            'Git': 65,
            'Docker': 58
        }
    }

@PerformanceOptimizer.cache_data(ttl=1800)  # Cache 30 minutes
def get_optimized_comparison_data() -> Dict:
    """Données de comparaison optimisées"""
    return {
        'cv_names': ['CV_Hamza.pdf', 'CV_Sophia.pdf', 'CV_Adam.pdf', 'CV_Ali.pdf'],
        'scores': [91.3, 76.1, 85.2, 72.8],
        'categories': {
            'Compétences Techniques': [92, 78, 88, 75],
            'Expérience': [89, 74, 82, 70],
            'Éducation': [85, 80, 90, 75],
            'Projets': [88, 72, 85, 68]
        },
        'recommendations': [
            "CV_Hamza.pdf présente le meilleur profil global",
            "CV_Sophia.pdf pourrait améliorer ses compétences techniques",
            "CV_Adam.pdf a un bon équilibre général",
            "CV_Ali.pdf nécessite plus d'expérience pratique"
        ]
    }

# Fonction de nettoyage du cache
def clear_performance_cache():
    """Nettoie le cache de performance"""
    if 'performance_cache' in st.session_state:
        st.session_state.performance_cache.clear()
        st.success("Cache de performance nettoyé !")

# Fonction pour afficher les statistiques de performance
def show_performance_stats():
    """Affiche les statistiques de performance du cache"""
    if 'performance_cache' in st.session_state:
        cache = st.session_state.performance_cache
        st.sidebar.markdown("### 📊 Statistiques de Performance")
        st.sidebar.metric("Entrées en cache", len(cache))
        
        # Calculer le temps d'exécution moyen
        if cache:
            avg_time = np.mean([entry['execution_time'] for entry in cache.values()])
            st.sidebar.metric("Temps d'exécution moyen", f"{avg_time:.3f}s")
        
        # Afficher les clés du cache
        st.sidebar.markdown("**Fonctions en cache:**")
        for key in list(cache.keys())[:5]:  # Afficher les 5 premières
            st.sidebar.text(f"• {key}")
        
        if len(cache) > 5:
            st.sidebar.text(f"... et {len(cache) - 5} autres")

# Fonction pour optimiser les DataFrames
def optimize_dataframe_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Optimise un DataFrame pour de meilleures performances"""
    # Optimiser les types de données
    for col in df.columns:
        if df[col].dtype == 'object':
            # Essayer de convertir en catégorie si peu de valeurs uniques
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        elif df[col].dtype == 'int64':
            # Réduire la taille des entiers
            if df[col].min() >= 0:
                if df[col].max() < 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].max() < 65535:
                    df[col] = df[col].astype('uint16')
                else:
                    df[col] = df[col].astype('uint32')
            else:
                if df[col].min() > -128 and df[col].max() < 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() > -32768 and df[col].max() < 32767:
                    df[col] = df[col].astype('int16')
                else:
                    df[col] = df[col].astype('int32')
        elif df[col].dtype == 'float64':
            # Réduire la précision des flottants
            df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df
