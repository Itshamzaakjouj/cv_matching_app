"""
Optimiseur de performance pour TalentScope
Améliore la vitesse de chargement et la réactivité de l'application
"""

import streamlit as st
import functools
import time
from typing import Any, Callable, Dict, List, Optional
import pandas as pd
import numpy as np

class PerformanceOptimizer:
    """Classe pour optimiser les performances de l'application"""
    
    @staticmethod
    def cache_data(ttl: int = 3600, max_entries: int = 100):
        """
        Décorateur pour mettre en cache les données avec TTL et limite d'entrées
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Créer une clé unique pour le cache
                cache_key = f"{func.__name__}_{hash(str(args))}_{hash(str(kwargs))}"
                
                # Vérifier si les données sont en cache
                if 'performance_cache' not in st.session_state:
                    st.session_state.performance_cache = {}
                
                cache = st.session_state.performance_cache
                
                # Nettoyer le cache si nécessaire
                if len(cache) > max_entries:
                    # Supprimer les entrées les plus anciennes
                    oldest_keys = sorted(cache.keys(), key=lambda k: cache[k]['timestamp'])[:len(cache)-max_entries+10]
                    for key in oldest_keys:
                        del cache[key]
                
                # Vérifier si la donnée est en cache et valide
                if cache_key in cache:
                    cached_data = cache[cache_key]
                    if time.time() - cached_data['timestamp'] < ttl:
                        return cached_data['data']
                
                # Exécuter la fonction et mettre en cache
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                cache[cache_key] = {
                    'data': result,
                    'timestamp': time.time(),
                    'execution_time': execution_time
                }
                
                return result
            
            return wrapper
        return decorator
    
    @staticmethod
    def lazy_load(component_func: Callable, loading_text: str = "Chargement..."):
        """
        Chargement paresseux des composants
        """
        @functools.wraps(component_func)
        def wrapper(*args, **kwargs):
            if f"loaded_{component_func.__name__}" not in st.session_state:
                with st.spinner(loading_text):
                    st.session_state[f"loaded_{component_func.__name__}"] = component_func(*args, **kwargs)
            return st.session_state[f"loaded_{component_func.__name__}"]
        return wrapper
    
    @staticmethod
    def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimise un DataFrame en réduisant l'utilisation mémoire
        """
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
    
    @staticmethod
    def batch_operations(operations: List[Callable], batch_size: int = 10):
        """
        Exécute les opérations par lots pour éviter de surcharger l'interface
        """
        results = []
        for i in range(0, len(operations), batch_size):
            batch = operations[i:i+batch_size]
            batch_results = []
            for op in batch:
                batch_results.append(op())
            results.extend(batch_results)
            # Petite pause pour éviter de bloquer l'interface
            time.sleep(0.01)
        return results

# Fonctions utilitaires optimisées
@PerformanceOptimizer.cache_data(ttl=1800)  # Cache 30 minutes
def get_sample_data_optimized():
    """Version optimisée de get_sample_data avec cache"""
    return {
        'trend_data': {
            'dates': pd.date_range('2024-01-01', periods=30, freq='D'),
            'analyses': np.random.randint(10, 50, 30),
            'scores': np.random.uniform(60, 95, 30)
        },
        'skills_data': {
            'skills': ['Python', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis'],
            'demand': [85, 78, 92, 88, 76]
        }
    }

@PerformanceOptimizer.cache_data(ttl=3600)  # Cache 1 heure
def get_sample_cv_data_optimized():
    """Version optimisée de get_sample_cv_data avec cache"""
    cv_data = []
    for i in range(20):  # Réduire le nombre de CVs par défaut
        cv_data.append({
            'name': f'CV_{i+1}',
            'score': np.random.uniform(70, 95),
            'status': np.random.choice(['Excellent', 'Bon', 'Moyen']),
            'position': f'Position_{i+1}',
            'skills': np.random.choice(['Python', 'JavaScript', 'SQL', 'ML'], size=3, replace=False).tolist(),
            'date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 30))
        })
    
    return PerformanceOptimizer.optimize_dataframe(pd.DataFrame(cv_data))

# Configuration optimisée de Streamlit
def configure_streamlit_performance():
    """Configure Streamlit pour de meilleures performances"""
    st.set_page_config(
        page_title="TalentScope - Optimisé",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS pour améliorer les performances
    st.markdown("""
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
    </style>
    """, unsafe_allow_html=True)

# Gestionnaire de mémoire
class MemoryManager:
    """Gestionnaire de mémoire pour optimiser l'utilisation"""
    
    @staticmethod
    def cleanup_session_state():
        """Nettoie le session_state des données inutiles"""
        keys_to_remove = []
        for key in st.session_state.keys():
            if key.startswith('temp_') or key.startswith('cache_'):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    @staticmethod
    def get_memory_usage():
        """Retourne l'utilisation mémoire approximative"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB

# Optimiseur de rendu
class RenderOptimizer:
    """Optimiseur pour le rendu des composants"""
    
    @staticmethod
    def conditional_render(condition: bool, component_func: Callable, *args, **kwargs):
        """Rend un composant seulement si la condition est vraie"""
        if condition:
            return component_func(*args, **kwargs)
        return None
    
    @staticmethod
    def memoize_expensive_operation(func: Callable):
        """Mémorise les opérations coûteuses"""
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
