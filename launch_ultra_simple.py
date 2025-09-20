import streamlit as st
import base64
from pathlib import Path
from i18n import t
from performance_optimizer import (
    PerformanceOptimizer, 
    MemoryManager, 
    RenderOptimizer,
    configure_streamlit_performance,
    get_sample_data_optimized,
    get_sample_cv_data_optimized
)

@PerformanceOptimizer.cache_data(ttl=3600)  # Cache 1 heure
def set_page_config():
    # Configuration optimisée
    configure_streamlit_performance()
    
    # Charger la configuration
    try:
        import json
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        theme = config.get('theme', 'Clair')
        language = config.get('language', 'Français')
    except:
        theme = 'Clair'
        language = 'Français'
    
    # Lecture du fichier image (optimisée)
    favicon_path = Path("Logos/TalentScope.png")
    if favicon_path.exists():
        with open(favicon_path, "rb") as f:
            favicon_data = base64.b64encode(f.read()).decode()
        
        st.set_page_config(
            page_title="TalentScope - Optimisé",
            page_icon=f"data:image/png;base64,{favicon_data}",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    else:
        st.set_page_config(
            page_title="TalentScope - Optimisé",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    # Appliquer le thème
    if theme == "Sombre":
        st.markdown("""
        <style>
        /* ===== SUPPRIMER COMPLÈTEMENT LE SÉLECTEUR DE PAGES STREAMLIT ===== */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Masquer tous les éléments de navigation automatique */
        .css-1d391kg,
        .css-1cypcdb,
        .stSelectbox[data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] > div:first-child,
        [data-testid="stSidebarNav"] > div,
        [data-testid="stSidebarNav"] ul,
        [data-testid="stSidebarNav"] li,
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] span,
        .css-1d391kg > div:first-child,
        .css-1cypcdb > div:first-child {
            display: none !important;
        }
        
        /* Masquer spécifiquement le composant "launch ultra simple" */
        .stSelectbox,
        .stSelectbox > div,
        .stSelectbox > div > div,
        .stSelectbox > div > div > div {
            display: none !important;
        }
        
        /* Masquer les suggestions et options */
        .stSelectbox label,
        .stSelectbox [role="combobox"],
        .stSelectbox [aria-expanded] {
            display: none !important;
        }
        
        /* Masquer complètement la section redondante */
        .css-1d391kg > div:first-child > div:first-child,
        .css-1cypcdb > div:first-child > div:first-child,
        .css-1d391kg > div:first-child > div:first-child > div,
        .css-1cypcdb > div:first-child > div:first-child > div {
            display: none !important;
        }
        
        /* Masquer les éléments de sélection de page */
        .css-1d391kg .stSelectbox,
        .css-1cypcdb .stSelectbox,
        .css-1d391kg .stSelectbox > div,
        .css-1cypcdb .stSelectbox > div {
            display: none !important;
        }
        
        /* Masquer les textes "launch ultra simple", "analyse", "comparaison" */
        .css-1d391kg div:contains("launch ultra simple"),
        .css-1cypcdb div:contains("launch ultra simple"),
        .css-1d391kg div:contains("analyse"),
        .css-1cypcdb div:contains("analyse"),
        .css-1d391kg div:contains("comparaison"),
        .css-1cypcdb div:contains("comparaison") {
            display: none !important;
        }
        
        /* ===== DESIGN SYSTEM MODERNE ===== */
        
        /* Variables CSS modernes inspirées de Tailwind */
        :root {
            /* Couleurs primaires */
            --primary: #3B82F6;
            --primary-hover: #2563EB;
            --primary-light: #DBEAFE;
            --secondary: #10B981;
            --accent: #F59E0B;
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            
            /* Couleurs de fond */
            --bg-primary: #FAFBFC;
            --bg-secondary: #FFFFFF;
            --bg-tertiary: #F8FAFC;
            --bg-dark: #1F2937;
            --bg-darker: #111827;
            
            /* Couleurs de texte */
            --text-primary: #1F2937;
            --text-secondary: #6B7280;
            --text-muted: #9CA3AF;
            --text-white: #FFFFFF;
            
            /* Bordures et ombres */
            --border: #E5E7EB;
            --border-focus: #3B82F6;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
            
            /* Rayons */
            --radius: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            --radius-full: 9999px;
            
            /* Transitions */
            --transition: all 0.2s ease-in-out;
            --transition-fast: all 0.15s ease-in-out;
        }
        
        /* Reset et base */
        * {
            box-sizing: border-box;
        }
        
        .stApp {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            line-height: 1.6 !important;
        }
        
        /* Typographie moderne */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            line-height: 1.2 !important;
            margin: 0 !important;
        }
        
        h1 { 
            font-size: 2.25rem !important; 
            font-weight: 700 !important;
            margin-bottom: 1rem !important; 
        }
        h2 { 
            font-size: 1.875rem !important; 
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important; 
        }
        h3 { 
            font-size: 1.5rem !important; 
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important; 
        }
        h4 { 
            font-size: 1.25rem !important; 
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important; 
        }
        
        p, span, div, label {
            color: var(--text-secondary) !important;
            line-height: 1.6 !important;
            margin: 0 !important;
        }
        
        .text-display {
            font-size: 2rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }
        
        .text-title {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            line-height: 1.3 !important;
        }
        
        .text-body {
            font-size: 0.875rem !important;
            line-height: 1.5 !important;
        }
        
        .text-caption {
            font-size: 0.75rem !important;
            color: var(--text-muted) !important;
        }
        
        /* Sidebar moderne */
        .css-1d391kg, .css-1cypcdb {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: var(--shadow-sm) !important;
            padding: 1.5rem !important;
        }
        
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
        .css-1cypcdb h1, .css-1cypcdb h2, .css-1cypcdb h3 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }
        
        /* Conteneur principal */
        .main .block-container {
            background: transparent !important;
            color: var(--text-primary) !important;
            padding: 2rem !important;
        }
        
        /* Cartes modernes */
        .stCard, .css-1y4p8pa, .css-1v0mbdj {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow-sm) !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            transition: var(--transition) !important;
        }
        
        .stCard:hover, .css-1y4p8pa:hover, .css-1v0mbdj:hover {
            box-shadow: var(--shadow-md) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Cartes métriques modernes */
        .metric-card {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.5rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        .metric-card:hover {
            box-shadow: var(--shadow-lg) !important;
            transform: translateY(-2px) !important;
        }
        
        .metric-card::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            height: 4px !important;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        }
        
        .metric-value {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
            margin: 0 !important;
        }
        
        .metric-label {
            font-size: 0.875rem !important;
            color: var(--text-secondary) !important;
            margin: 0.5rem 0 0 0 !important;
        }
        
        .metric-trend {
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.25rem !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            padding: 0.25rem 0.5rem !important;
            border-radius: var(--radius-full) !important;
            margin-top: 0.5rem !important;
        }
        
        .metric-trend.positive {
            background: #DCFCE7 !important;
            color: #166534 !important;
        }
        
        .metric-trend.negative {
            background: #FEE2E2 !important;
            color: #DC2626 !important;
        }
        
        /* Boutons modernes */
        .stButton > button {
            background: var(--primary) !important;
            color: var(--text-white) !important;
            border: none !important;
            border-radius: var(--radius) !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            box-shadow: var(--shadow-sm) !important;
            transition: var(--transition) !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background: var(--primary-hover) !important;
            box-shadow: var(--shadow-md) !important;
            transform: translateY(-1px) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        /* Boutons secondaires */
        .stButton > button[data-testid="baseButton-secondary"] {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background: var(--bg-tertiary) !important;
            border-color: var(--primary) !important;
        }
        
        /* Boutons de navigation sidebar */
        .css-1d391kg .stButton > button,
        .css-1cypcdb .stButton > button {
            background: transparent !important;
            color: var(--text-secondary) !important;
            border: none !important;
            border-radius: var(--radius) !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;
            transition: var(--transition) !important;
            text-align: left !important;
            width: 100% !important;
        }
        
        .css-1d391kg .stButton > button:hover,
        .css-1cypcdb .stButton > button:hover {
            background: var(--primary-light) !important;
            color: var(--primary) !important;
            transform: translateX(4px) !important;
        }
        
        /* Inputs modernes */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stTextArea > div > div > textarea {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 0.75rem !important;
            font-size: 0.875rem !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-sm) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            outline: none !important;
        }
        
        .stTextInput > div > div > input:hover,
        .stSelectbox > div > div > div:hover,
        .stTextArea > div > div > textarea:hover {
            border-color: var(--primary) !important;
        }
        
        /* Sliders stylés */
        .stSlider > div > div > div {
            background: var(--bg-tertiary) !important;
            border-radius: 10px !important;
            height: 8px !important;
        }
        
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
            border-radius: 10px !important;
        }
        
        .stSlider > div > div > div > div > div {
            background: white !important;
            border: 3px solid var(--accent-primary) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        /* Checkboxes et radios */
        .stCheckbox > div > label,
        .stRadio > div > label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
        }
        
        .stCheckbox > div > div > div > div {
            background: var(--bg-tertiary) !important;
            border: 2px solid var(--border-color) !important;
        }
        
        .stCheckbox > div > div > div > div[data-checked="true"] {
            background: var(--accent-primary) !important;
            border-color: var(--accent-primary) !important;
        }
        
        /* Métriques et KPIs */
        .metric-container, .css-1r6slb0 {
            background: linear-gradient(145deg, var(--bg-tertiary) 0%, #1e1e1e 100%) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            box-shadow: var(--shadow) !important;
            text-align: center !important;
        }
        
        .metric-container > div {
            color: var(--text-primary) !important;
        }
        
        .metric-container .metric-value {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--accent-primary) !important;
        }
        
        /* Progress bars */
        .stProgress > div > div > div {
            background: var(--bg-tertiary) !important;
            border-radius: 10px !important;
            height: 12px !important;
        }
        
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 4px rgba(255, 107, 53, 0.3) !important;
        }
        
        /* Tables */
        .stDataFrame, .dataframe {
            background: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }
        
        .stDataFrame th, .dataframe th {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            padding: 1rem !important;
        }
        
        .stDataFrame td, .dataframe td {
            color: var(--text-secondary) !important;
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid var(--border-color) !important;
        }
        
        .stDataFrame tr:nth-child(even), .dataframe tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02) !important;
        }
        
        /* Alerts et notifications */
        .stAlert {
            background: var(--bg-tertiary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            box-shadow: var(--shadow) !important;
        }
        
        .stSuccess {
            background: linear-gradient(145deg, #1e3a1e 0%, #2d4a2d 100%) !important;
            border-color: #4caf50 !important;
            color: #e8f5e8 !important;
        }
        
        .stError {
            background: linear-gradient(145deg, #3a1e1e 0%, #4a2e2e 100%) !important;
            border-color: #f44336 !important;
            color: #ffe8e8 !important;
        }
        
        .stWarning {
            background: linear-gradient(145deg, #3a2e1e 0%, #4a3e2e 100%) !important;
            border-color: #ff9800 !important;
            color: #fff8e1 !important;
        }
        
        .stInfo {
            background: linear-gradient(145deg, #1e2a3a 0%, #2e3a4a 100%) !important;
            border-color: #2196f3 !important;
            color: #e3f2fd !important;
        }
        
        /* Expanders */
        .streamlit-expander {
            background: var(--bg-tertiary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            margin: 1rem 0 !important;
        }
        
        .streamlit-expander .streamlit-expanderHeader {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            padding: 1rem !important;
        }
        
        .streamlit-expander .streamlit-expanderContent {
            color: var(--text-secondary) !important;
            padding: 0 1rem 1rem 1rem !important;
        }
        
        /* Tabs */
        .stTabs > div > div > div {
            background: var(--bg-tertiary) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 500 !important;
        }
        
        .stTabs > div > div > div[aria-selected="true"] {
            background: linear-gradient(45deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
            color: white !important;
            border-color: var(--accent-primary) !important;
            box-shadow: 0 2px 4px rgba(255, 107, 53, 0.3) !important;
        }
        
        /* Boutons sidebar */
        .css-1d391kg .stButton > button,
        .css-1cypcdb .stButton > button {
            background: transparent !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            margin: 0.25rem 0 !important;
            transition: all 0.3s ease !important;
        }
        
        .css-1d391kg .stButton > button:hover,
        .css-1cypcdb .stButton > button:hover {
            background: var(--bg-tertiary) !important;
            border-color: var(--accent-primary) !important;
            color: var(--accent-primary) !important;
            transform: translateX(4px) !important;
        }
        
        /* Liens */
        a {
            color: var(--accent-primary) !important;
            text-decoration: none !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        a:hover {
            color: var(--accent-secondary) !important;
            text-shadow: 0 0 8px rgba(255, 107, 53, 0.5) !important;
        }
        
        /* Code blocks */
        .stCodeBlock, pre {
            background: #000000 !important;
            color: #00ff00 !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            font-family: 'Courier New', monospace !important;
        }
        
        /* Graphiques Plotly */
        .js-plotly-plot {
            background: var(--bg-tertiary) !important;
            border-radius: 8px !important;
        }
        
        /* Scrollbar personnalisée */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
            border-radius: 6px;
            border: 2px solid var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #ff5722 0%, #ff7043 100%);
        }
        
        /* Animations subtiles */
        .stCard, .css-1y4p8pa {
            transition: all 0.3s ease !important;
        }
        
        .stCard:hover, .css-1y4p8pa:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4) !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
            }
            
            h1 { font-size: 2rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.25rem !important; }
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "Auto":
        # Thème automatique basé sur l'heure
        from datetime import datetime
        hour = datetime.now().hour
        if 6 <= hour < 18:  # Jour
            # Thème clair par défaut avec suppression complète du sélecteur
            st.markdown("""
            <style>
            /* ===== SUPPRIMER COMPLÈTEMENT LE SÉLECTEUR DE PAGES STREAMLIT ===== */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            /* Masquer tous les éléments de navigation automatique */
            .css-1d391kg,
            .css-1cypcdb,
            .stSelectbox[data-testid="stSidebarNav"],
            [data-testid="stSidebarNav"] > div:first-child,
            .css-1d391kg > div:first-child,
            .css-1cypcdb > div:first-child {
                display: none !important;
            }
            
            /* Masquer spécifiquement le composant "launch ultra simple" */
            .stSelectbox,
            .stSelectbox > div,
            .stSelectbox > div > div,
            .stSelectbox > div > div > div {
                display: none !important;
            }
            
            /* Masquer les suggestions et options */
            .stSelectbox label,
            .stSelectbox [role="combobox"],
            .stSelectbox [aria-expanded] {
                display: none !important;
            }
            
            /* Masquer complètement la section redondante */
            .css-1d391kg > div:first-child > div:first-child,
            .css-1cypcdb > div:first-child > div:first-child,
            .css-1d391kg > div:first-child > div:first-child > div,
            .css-1cypcdb > div:first-child > div:first-child > div {
                display: none !important;
            }
            
            /* Masquer les éléments de sélection de page */
            .css-1d391kg .stSelectbox,
            .css-1cypcdb .stSelectbox,
            .css-1d391kg .stSelectbox > div,
            .css-1cypcdb .stSelectbox > div {
                display: none !important;
            }
            
            /* Masquer les textes "launch ultra simple", "analyse", "comparaison" */
            .css-1d391kg div:contains("launch ultra simple"),
            .css-1cypcdb div:contains("launch ultra simple"),
            .css-1d391kg div:contains("analyse"),
            .css-1cypcdb div:contains("analyse"),
            .css-1d391kg div:contains("comparaison"),
            .css-1cypcdb div:contains("comparaison") {
                display: none !important;
            }
            
            /* Masquer complètement la section redondante */
            .css-1d391kg > div:first-child > div:first-child,
            .css-1cypcdb > div:first-child > div:first-child,
            .css-1d391kg > div:first-child > div:first-child > div,
            .css-1cypcdb > div:first-child > div:first-child > div {
                display: none !important;
            }
            
            /* Masquer les éléments de sélection de page */
            .css-1d391kg .stSelectbox,
            .css-1cypcdb .stSelectbox,
            .css-1d391kg .stSelectbox > div,
            .css-1cypcdb .stSelectbox > div {
                display: none !important;
            }
            
            /* Masquer les textes "launch ultra simple", "analyse", "comparaison" */
            .css-1d391kg div:contains("launch ultra simple"),
            .css-1cypcdb div:contains("launch ultra simple"),
            .css-1d391kg div:contains("analyse"),
            .css-1cypcdb div:contains("analyse"),
            .css-1d391kg div:contains("comparaison"),
            .css-1cypcdb div:contains("comparaison") {
                display: none !important;
            }
            </style>
            """, unsafe_allow_html=True)
        else:  # Nuit - Appliquer le thème sombre complet
            st.markdown("""
            <style>
            /* Thème sombre automatique (nuit) */
            .stApp {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            
            h1, h2, h3, h4, h5, h6, p, span, div {
                color: #fafafa !important;
            }
            
            .main .block-container {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            
            .stCard, .css-1y4p8pa {
                background-color: #262730 !important;
                color: #fafafa !important;
                border: 1px solid #404040 !important;
            }
            
            .stButton > button {
                background-color: #ff4b4b !important;
                color: white !important;
                border: 1px solid #ff4b4b !important;
            }
            
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div {
                background-color: #262730 !important;
                color: #fafafa !important;
                border: 1px solid #404040 !important;
            }
            
            .stCheckbox > div > label {
                color: #fafafa !important;
            }
            
            .stProgress > div > div > div {
                background-color: #404040 !important;
            }
            
            .stProgress > div > div > div > div {
                background-color: #ff4b4b !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Thème clair par défaut avec suppression complète du sélecteur
        st.markdown("""
        <style>
        /* ===== SUPPRIMER COMPLÈTEMENT LE SÉLECTEUR DE PAGES STREAMLIT ===== */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Masquer tous les éléments de navigation automatique */
        .css-1d391kg,
        .css-1cypcdb,
        .stSelectbox[data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] > div:first-child,
        [data-testid="stSidebarNav"] > div,
        [data-testid="stSidebarNav"] ul,
        [data-testid="stSidebarNav"] li,
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] span,
        .css-1d391kg > div:first-child,
        .css-1cypcdb > div:first-child {
            display: none !important;
        }
        
        /* Masquer spécifiquement le composant "launch ultra simple" */
        .stSelectbox,
        .stSelectbox > div,
        .stSelectbox > div > div,
        .stSelectbox > div > div > div {
            display: none !important;
        }
        
        /* Masquer les suggestions et options */
        .stSelectbox label,
        .stSelectbox [role="combobox"],
        .stSelectbox [aria-expanded] {
            display: none !important;
        }
        
        /* Masquer complètement la section redondante */
        .css-1d391kg > div:first-child > div:first-child,
        .css-1cypcdb > div:first-child > div:first-child,
        .css-1d391kg > div:first-child > div:first-child > div,
        .css-1cypcdb > div:first-child > div:first-child > div {
            display: none !important;
        }
        
        /* Masquer les éléments de sélection de page */
        .css-1d391kg .stSelectbox,
        .css-1cypcdb .stSelectbox,
        .css-1d391kg .stSelectbox > div,
        .css-1cypcdb .stSelectbox > div {
            display: none !important;
        }
        
        /* Masquer les textes "launch ultra simple", "analyse", "comparaison" */
        .css-1d391kg div:contains("launch ultra simple"),
        .css-1cypcdb div:contains("launch ultra simple"),
        .css-1d391kg div:contains("analyse"),
        .css-1cypcdb div:contains("analyse"),
        .css-1d391kg div:contains("comparaison"),
        .css-1cypcdb div:contains("comparaison") {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

def render_main_content():
    """Affiche le contenu principal de l'application"""
    # Initialiser les états si pas définis
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    if 'show_processed_cvs' not in st.session_state:
        st.session_state.show_processed_cvs = False
    if 'show_configuration' not in st.session_state:
        st.session_state.show_configuration = False
    if 'show_home' not in st.session_state:
        st.session_state.show_home = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    
    # Afficher le contenu selon la sélection
    if st.session_state.show_profile:
        render_profile_page()
    elif st.session_state.show_dashboard:
        from dashboard_analytics import render_dashboard
        render_dashboard()
    elif st.session_state.show_processed_cvs:
        render_processed_cvs_page()
    elif st.session_state.show_configuration:
        render_configuration_page()
    elif st.session_state.show_home:
        render_home_page()
    else:
        from components.main_interface import render_main_interface
        render_main_interface()

def render_profile_page():
    """Page de profil utilisateur"""
    st.markdown(f"# 👤 {t('profile.title')}")
    st.markdown("---")
    
    # Informations utilisateur
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### 📸 {t('profile.photo')}")
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👤</div>
            <p style="margin: 0; font-size: 1.2rem; font-weight: 600;">{t('profile.photo')}</p>
            <p style="margin: 0; opacity: 0.8;">Cliquez pour changer</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📷 {t('profile.change_photo')}", use_container_width=True):
            st.info("Fonctionnalité de changement de photo en cours de développement")
    
    with col2:
        st.markdown(f"### ℹ️ {t('profile.personal_info')}")
        
        # Formulaire de profil
        with st.form("profile_form"):
            col_email, col_phone = st.columns(2)
            
            with col_email:
                email = st.text_input(
                    f"📧 {t('label.email')}",
                    value=st.session_state.get('user_email', ''),
                    disabled=True,
                    help="L'adresse e-mail ne peut pas être modifiée"
                )
            
            with col_phone:
                phone = st.text_input(
                    "📱 Téléphone",
                    placeholder="Entrez votre numéro de téléphone"
                )
            
            full_name = st.text_input(
                f"👤 {t('profile.full_name')}",
                placeholder="Entrez votre nom complet"
            )
            
            department = st.selectbox(
                f"🏢 {t('profile.department')}",
                [t("dept.hr"), t("dept.it"), t("dept.finance"), t("dept.admin"), t("dept.other")]
            )
            
            position = st.text_input(
                f"💼 {t('profile.position')}",
                placeholder="Entrez votre poste actuel"
            )
            
            bio = st.text_area(
                f"📝 {t('profile.bio')}",
                placeholder="Parlez-nous de vous...",
                height=100
            )
            
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                if st.form_submit_button(f"💾 {t('profile.save')}", use_container_width=True):
                    st.success("Profil mis à jour avec succès !")
            
            with col_cancel:
                if st.form_submit_button(f"❌ {t('profile.cancel')}", use_container_width=True):
                    st.session_state.show_profile = False
                    st.rerun()
    
    st.markdown("---")
    
    # Statistiques personnelles
    st.markdown(f"### 📊 {t('profile.stats')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            f"📝 {t('profile.analyses_done')}",
            "24",
            "+3 cette semaine"
        )
    
    with col2:
        st.metric(
            f"⭐ {t('profile.avg_score')}",
            "82.5%",
            "+1.2%"
        )
    
    with col3:
        st.metric(
            f"🏆 {t('profile.excellent_cvs')}",
            "8",
            "+2"
        )
    
    with col4:
        st.metric(
            f"📅 {t('profile.last_login')}",
            "Aujourd'hui",
            "14:30"
        )
    
    # Actions rapides
    st.markdown(f"### ⚡ {t('profile.quick_actions')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🔒 {t('profile.change_password')}", use_container_width=True):
            st.info("Fonctionnalité de changement de mot de passe en cours de développement")
    
    with col2:
        if st.button(f"📧 {t('profile.notifications')}", use_container_width=True):
            st.info("Fonctionnalité de gestion des notifications en cours de développement")
    
    with col3:
        if st.button(f"⚙️ {t('profile.advanced_settings')}", use_container_width=True):
            st.session_state.show_configuration = True
            st.session_state.show_profile = False
            st.rerun()

def render_home_page():
    """Page d'accueil avec dashboard rapide et actions"""
    # Rediriger automatiquement vers le tableau de bord
    st.session_state.show_dashboard = True
    st.session_state.show_home = False
    st.rerun()
    
    # Métriques rapides modernes
    st.markdown(f"### 📊 {t('home.overview')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: #DBEAFE; padding: 0.75rem; border-radius: 0.75rem;">
                    <span style="font-size: 1.25rem;">📈</span>
                </div>
                <div class="metric-trend positive">
                    <span>↗</span>
                    <span>+12 cette semaine</span>
                </div>
            </div>
            <div class="metric-value">156</div>
            <div class="metric-label">CVs Analysés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: #DCFCE7; padding: 0.75rem; border-radius: 0.75rem;">
                    <span style="font-size: 1.25rem;">🎯</span>
                </div>
                <div class="metric-trend positive">
                    <span>↗</span>
                    <span>+2.3%</span>
                </div>
            </div>
            <div class="metric-value">78.5%</div>
            <div class="metric-label">Score Moyen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: #FEF3C7; padding: 0.75rem; border-radius: 0.75rem;">
                    <span style="font-size: 1.25rem;">⭐</span>
                </div>
                <div class="metric-trend positive">
                    <span>↗</span>
                    <span>+5</span>
                </div>
            </div>
            <div class="metric-value">23</div>
            <div class="metric-label">CVs Excellents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: #FEE2E2; padding: 0.75rem; border-radius: 0.75rem;">
                    <span style="font-size: 1.25rem;">⚡</span>
                </div>
                <div class="metric-trend positive">
                    <span>↗</span>
                    <span>+3</span>
                </div>
            </div>
            <div class="metric-value">8</div>
            <div class="metric-label">Analyses Aujourd'hui</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions rapides modernes
    st.markdown(f"### 🚀 {t('home.quick_actions')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🚀 {t('nav.new_analysis')} (Moderne)", use_container_width=True, type="primary"):
            # Rediriger vers l'interface d'analyse moderne
            st.markdown("""
            <script>
                window.open('http://localhost:9000', '_blank');
            </script>
            """, unsafe_allow_html=True)
            st.success("🚀 Ouverture de l'interface d'analyse moderne ultra-optimisée...")
            st.info("💡 L'interface moderne s'ouvre dans un nouvel onglet avec des performances maximales !")
    
    with col2:
        if st.button(f"📊 {t('nav.dashboard')}", use_container_width=True):
            st.session_state.show_home = False
            st.session_state.show_dashboard = True
            st.rerun()
    
    with col3:
        if st.button(f"📁 {t('nav.processed_cvs')}", use_container_width=True):
            st.session_state.show_home = False
            st.session_state.show_processed_cvs = True
            st.rerun()
    
    st.markdown("---")
    
    # Graphique des tendances
    st.markdown(f"### 📈 {t('home.trends')}")
    
    import plotly.graph_objects as go
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Données simulées
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
    analyses = [12, 15, 8, 20, 18, 14, 16]
    scores = [75, 78, 72, 82, 79, 76, 80]
    
    fig = go.Figure()
    
    # Graphique des analyses
    fig.add_trace(go.Scatter(
        x=dates,
        y=analyses,
        mode='lines+markers',
        name='Analyses',
        line=dict(color='#1976D2', width=3),
        marker=dict(size=8)
    ))
    
    # Graphique des scores moyens
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Score Moyen (%)',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Évolution des Analyses et Scores",
        xaxis_title="Date",
        yaxis=dict(title="Nombre d'analyses", side="left"),
        yaxis2=dict(title="Score moyen (%)", side="right", overlaying="y"),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Dernières analyses
    st.markdown(f"### 📋 {t('home.recent_analyses')}")
    
    # Données simulées des dernières analyses
    recent_analyses = [
        {"CV": "cv_Hamza.pdf", "Poste": "Data Scientist", "Score": "91.3%", "Statut": "Excellent", "Date": "Aujourd'hui"},
        {"CV": "cv_Sophia.pdf", "Poste": "Développeur Python", "Score": "76.1%", "Statut": "Très bon", "Date": "Aujourd'hui"},
        {"CV": "cv_Adam.pdf", "Poste": "Analyste Data", "Score": "85.2%", "Statut": "Excellent", "Date": "Hier"},
        {"CV": "cv_Ali.pdf", "Poste": "Ingénieur ML", "Score": "72.8%", "Statut": "Bon", "Date": "Hier"},
        {"CV": "cv_Hafsa.pdf", "Poste": "Data Analyst", "Score": "68.5%", "Statut": "Moyen", "Date": "Il y a 2 jours"}
    ]
    
    for analysis in recent_analyses:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{analysis['CV']}**")
            st.markdown(f"*{analysis['Poste']}*")
        
        with col2:
            st.markdown(f"**{analysis['Score']}**")
            st.progress(float(analysis['Score'].replace('%', '')) / 100)
        
        with col3:
            status_color = {
                "Excellent": "#4CAF50",
                "Très bon": "#8BC34A", 
                "Bon": "#FFC107",
                "Moyen": "#FF9800"
            }.get(analysis['Statut'], "#9E9E9E")
            st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{analysis['Statut']}</span>", unsafe_allow_html=True)
        
        with col4:
            st.markdown(analysis['Date'])
        
        with col5:
            if st.button("👁️", key=f"view_{analysis['CV']}", help="Voir détails"):
                st.info(f"Détails de {analysis['CV']}")
    
    st.markdown("---")
    
    # Compétences les plus demandées
    st.markdown(f"### 🎯 {t('home.skills_demanded')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skills_data = {
            'Compétence': ['Python', 'Machine Learning', 'SQL', 'React', 'Docker', 'AWS', 'JavaScript', 'Git'],
            'Demande': [85, 78, 72, 68, 65, 60, 55, 50]
        }
        
        import plotly.express as px
        fig = px.bar(
            skills_data,
            x='Demande',
            y='Compétence',
            orientation='h',
            title="Top Compétences",
            color='Demande',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"#### 💡 {t('home.optimization_tips')}")
        
        tips = [
            "🎯 **Mots-clés pertinents** : Utilisez des termes techniques précis",
            "📊 **Quantifiez vos résultats** : Mentionnez des chiffres concrets",
            "🔧 **Compétences techniques** : Listez les technologies maîtrisées",
            "📈 **Expérience récente** : Mettez en avant vos projets récents",
            "🎓 **Formations** : Incluez vos certifications et diplômes"
        ]
        
        for tip in tips:
            st.markdown(tip)
    
    st.markdown("---")
    
    # Informations système
    st.markdown(f"### ℹ️ {t('home.system_info')}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Version:** 1.0.0\n\n**Dernière mise à jour:** 17/09/2024")
    
    with col2:
        st.success("**Statut:** 🟢 Opérationnel\n\n**Performance:** Excellente")
    
    with col3:
        st.warning("**Maintenance:** Programmée\n\n**Prochaine:** 25/09/2024")

def render_dashboard_page():
    """Page dashboard avec métriques détaillées"""
    st.markdown(f"# 📊 {t('dashboard.title')}")
    st.markdown("---")
    
    # Métriques détaillées
    st.markdown(f"### 📈 {t('dashboard.metrics')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Total CVs",
            value="156",
            delta="+12 cette semaine"
        )
    
    with col2:
        st.metric(
            label="🎯 Score Moyen",
            value="78.5%",
            delta="+2.3%"
        )
    
    with col3:
        st.metric(
            label="⭐ CVs Excellents",
            value="23",
            delta="+5"
        )
    
    with col4:
        st.metric(
            label="⚡ Analyses Aujourd'hui",
            value="8",
            delta="+3"
        )
    
    st.markdown("---")
    
    # Graphiques de tendances
    st.markdown(f"### 📈 {t('dashboard.trends')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Évolution des Analyses")
        # Données simulées
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(start='2024-09-01', end='2024-09-18', freq='D')
        analyses = np.random.randint(5, 20, len(dates))
        
        df = pd.DataFrame({
            'Date': dates,
            'Analyses': analyses
        })
        
        st.line_chart(df.set_index('Date'))
    
    with col2:
        st.markdown("#### Distribution des Scores")
        scores = np.random.normal(75, 15, 100)
        scores = np.clip(scores, 0, 100)
        
        st.bar_chart(pd.DataFrame({'Scores': scores}))
    
    st.markdown("---")
    
    # Dernières analyses
    st.markdown(f"### 📋 {t('dashboard.recent_analyses')}")
    
    # Données simulées
    cv_data = [
        {"nom": "cv_Hamza.pdf", "score": 91.3, "status": "Excellent", "poste": "Data Scientist"},
        {"nom": "cv_Sophia.pdf", "score": 76.1, "status": "Très bon", "poste": "Développeur Python"},
        {"nom": "cv_Adam.pdf", "score": 85.2, "status": "Excellent", "poste": "Analyste Data"},
        {"nom": "cv_Ali.pdf", "score": 72.8, "status": "Bon", "poste": "Ingénieur ML"},
    ]
    
    for cv in cv_data:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"📄 {cv['nom']}")
        with col2:
            st.write(f"{cv['score']}%")
        with col3:
            st.write(cv['status'])
        with col4:
            st.write(cv['poste'])

def render_processed_cvs_page():
    """Page des CVs traités"""
    st.markdown(f"# 📁 {t('processed.title')}")
    st.markdown("---")
    
    st.markdown(f"### 📋 {t('processed.history')}")
    
    # Tableau des CVs traités
    import pandas as pd
    
    data = {
        'CV': ['cv_Adam.pdf', 'cv_Ali.pdf', 'cv_Hafsa.pdf', 'cv_Hamza.pdf', 'cv_Sophia.pdf', 'cv_Yassine.pdf'],
        'Date d\'analyse': ['2024-01-15', '2024-01-15', '2024-01-14', '2024-01-14', '2024-01-13', '2024-01-13'],
        'Score': [85.2, 72.8, 68.5, 91.3, 76.1, 63.2],
        'Statut': ['Excellent', 'Bon', 'Moyen', 'Excellent', 'Très bon', 'Moyen'],
        'Poste': ['Data Scientist', 'Data Scientist', 'Data Scientist', 'Data Scientist', 'Data Scientist', 'Data Scientist']
    }
    
    df = pd.DataFrame(data)
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        statut_filter = st.selectbox(t("processed.filter_status"), ["Tous", t("status.excellent"), t("status.very_good"), t("status.good"), t("status.average")])
    
    with col2:
        date_filter = st.date_input(t("processed.filter_date"), value=None)
    
    with col3:
        score_filter = st.slider(t("processed.min_score"), 0, 100, 0)
    
    # Appliquer les filtres
    if statut_filter != "Tous":
        df = df[df['Statut'] == statut_filter]
    
    if date_filter:
        df = df[df['Date d\'analyse'] >= str(date_filter)]
    
    df = df[df['Score'] >= score_filter]
    
    # Afficher le tableau
    st.dataframe(df, use_container_width=True)
    
    # Statistiques
    st.markdown(f"### 📊 {t('processed.stats')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(t("processed.total_cvs"), len(df))
    
    with col2:
        st.metric(t("processed.avg_score"), f"{df['Score'].mean():.1f}%")
    
    with col3:
        st.metric(t("processed.best_score"), f"{df['Score'].max():.1f}%")
    
    with col4:
        excellent_count = len(df[df['Statut'] == 'Excellent'])
        st.metric(t("processed.excellent_cvs"), excellent_count)

def render_configuration_page():
    """Page de configuration"""
    st.markdown(f"# ⚙️ {t('config.title')}")
    st.markdown("---")
    
    # Initialiser les paramètres dans session_state
    if 'config_technical_weight' not in st.session_state:
        st.session_state.config_technical_weight = 0.50
    if 'config_experience_weight' not in st.session_state:
        st.session_state.config_experience_weight = 0.30
    if 'config_education_weight' not in st.session_state:
        st.session_state.config_education_weight = 0.20
    if 'config_excellent_threshold' not in st.session_state:
        st.session_state.config_excellent_threshold = 0.8
    if 'config_good_threshold' not in st.session_state:
        st.session_state.config_good_threshold = 0.6
    if 'config_average_threshold' not in st.session_state:
        st.session_state.config_average_threshold = 0.4
    if 'config_theme' not in st.session_state:
        st.session_state.config_theme = "Clair"
    if 'config_language' not in st.session_state:
        st.session_state.config_language = "Français"
    if 'config_show_progress' not in st.session_state:
        st.session_state.config_show_progress = True
    if 'config_show_details' not in st.session_state:
        st.session_state.config_show_details = True
    if 'config_auto_save' not in st.session_state:
        st.session_state.config_auto_save = True
    if 'config_export_format' not in st.session_state:
        st.session_state.config_export_format = "PDF"
    if 'config_include_charts' not in st.session_state:
        st.session_state.config_include_charts = True
    if 'config_email_reports' not in st.session_state:
        st.session_state.config_email_reports = False
    
    st.markdown(f"### 🔧 {t('config.app_settings')}")
    
    # Paramètres de l'algorithme
    st.markdown(f"#### 🤖 {t('config.algorithm')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{t('config.criteria_weights')}**")
        technical_weight = st.slider(
            t("config.technical_skills"), 
            0.0, 1.0, 
            st.session_state.config_technical_weight, 
            0.05,
            key="slider_technical"
        )
        experience_weight = st.slider(
            t("config.experience"), 
            0.0, 1.0, 
            st.session_state.config_experience_weight, 
            0.05,
            key="slider_experience"
        )
        education_weight = st.slider(
            t("config.education"), 
            0.0, 1.0, 
            st.session_state.config_education_weight, 
            0.05,
            key="slider_education"
        )
    
    with col2:
        st.markdown(f"**{t('config.classification_thresholds')}**")
        excellent_threshold = st.slider(
            t("config.excellent"), 
            0.0, 1.0, 
            st.session_state.config_excellent_threshold, 
            0.05,
            key="slider_excellent"
        )
        good_threshold = st.slider(
            t("config.very_good"), 
            0.0, 1.0, 
            st.session_state.config_good_threshold, 
            0.05,
            key="slider_good"
        )
        average_threshold = st.slider(
            t("config.good"), 
            0.0, 1.0, 
            st.session_state.config_average_threshold, 
            0.05,
            key="slider_average"
        )
    
    # Sauvegarder automatiquement les changements
    st.session_state.config_technical_weight = technical_weight
    st.session_state.config_experience_weight = experience_weight
    st.session_state.config_education_weight = education_weight
    st.session_state.config_excellent_threshold = excellent_threshold
    st.session_state.config_good_threshold = good_threshold
    st.session_state.config_average_threshold = average_threshold
    
    st.markdown("---")
    
    # Paramètres d'affichage
    st.markdown(f"#### 🎨 {t('config.ui_settings')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme_options = ["Clair", "Sombre", "Auto"]
        current_theme = st.session_state.config_theme
        try:
            theme_index = theme_options.index(current_theme)
        except ValueError:
            theme_index = 0  # Clair par défaut
        
        theme = st.selectbox(
            t("config.theme"), 
            theme_options,
            index=theme_index,
            key="select_theme"
        )
        language_options = ["Français", "Anglais"]
        current_lang = st.session_state.config_language
        try:
            current_index = language_options.index(current_lang)
        except ValueError:
            current_index = 0  # Français par défaut
        
        language = st.selectbox(
            t("config.language"), 
            language_options,
            index=current_index,
            key="select_language"
        )
    
    with col2:
        show_progress = st.checkbox(
            t("config.show_progress"), 
            value=st.session_state.config_show_progress,
            key="checkbox_progress"
        )
        show_details = st.checkbox(
            t("config.show_details"), 
            value=st.session_state.config_show_details,
            key="checkbox_details"
        )
    
    # Sauvegarder les paramètres d'affichage
    st.session_state.config_theme = theme
    st.session_state.config_language = language
    st.session_state.config_show_progress = show_progress
    st.session_state.config_show_details = show_details
    
    # Mettre à jour la langue immédiatement pour que t() fonctionne
    st.session_state.language = language
    
    st.markdown("---")
    
    # Paramètres d'export
    # Configuration automatique - pas d'interface utilisateur
    st.session_state.config_auto_save = True  # Toujours activé
    st.session_state.config_export_format = "PDF"  # Toujours PDF
    st.session_state.config_include_charts = True  # Toujours activé
    st.session_state.config_email_reports = False  # Toujours désactivé
    
    st.markdown("---")
    
    # Boutons d'action simplifiés
    st.markdown(f"#### 🎛️ {t('config.actions')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💾 {t('config.save_config')}", use_container_width=True):
            # Sauvegarder dans un fichier JSON
            import json
            config_data = {
                "technical_weight": technical_weight,
                "experience_weight": experience_weight,
                "education_weight": education_weight,
                "excellent_threshold": excellent_threshold,
                "good_threshold": good_threshold,
                "average_threshold": average_threshold,
                "theme": theme,
                "language": language,
                "show_progress": show_progress,
                "show_details": show_details,
                "auto_save": True,  # Toujours activé
                "export_format": "PDF",  # Toujours PDF
                "include_charts": True,  # Toujours activé
                "email_reports": False  # Toujours désactivé
            }
            
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Mettre à jour la session state immédiatement AVANT d'afficher les messages
            st.session_state.language = language
            st.session_state.config_theme = theme
            st.session_state.config_language = language
            st.session_state.config_show_progress = show_progress
            st.session_state.config_show_details = show_details
            st.session_state.config_auto_save = True  # Toujours activé
            st.session_state.config_export_format = "PDF"  # Toujours PDF
            st.session_state.config_include_charts = True  # Toujours activé
            st.session_state.config_email_reports = False  # Toujours désactivé
            
            # Message de succès dans la langue appropriée
            if language == "Anglais":
                st.success("✅ Configuration saved successfully!")
            else:
                st.success("✅ Configuration sauvegardée avec succès!")
            st.balloons()
            
            # Forcer le rechargement pour appliquer les changements
            if language == "Anglais":
                st.markdown("🔄 **Restarting application to apply changes...**")
            else:
                st.markdown("🔄 **Redémarrage de l'application pour appliquer les changements...**")
            
            # Attendre un peu pour que l'utilisateur voie le message
            import time
            time.sleep(2)
            
            # Ajouter un timestamp pour forcer le rechargement
            st.session_state.language_timestamp = time.time()
            
            # Forcer un rechargement complet de la page
            try:
                st.experimental_rerun()
            except:
                st.rerun()
    
    with col2:
        if st.button(f"🔄 {t('config.reset')}", use_container_width=True):
            # Réinitialiser aux valeurs par défaut
            st.session_state.config_technical_weight = 0.50
            st.session_state.config_experience_weight = 0.30
            st.session_state.config_education_weight = 0.20
            st.session_state.config_excellent_threshold = 0.8
            st.session_state.config_good_threshold = 0.6
            st.session_state.config_average_threshold = 0.4
            st.session_state.config_theme = "Clair"
            st.session_state.config_language = "Français"
            st.session_state.config_show_progress = True
            st.session_state.config_show_details = True
            st.session_state.config_auto_save = True
            st.session_state.config_export_format = "PDF"
            st.session_state.config_include_charts = True
            st.session_state.config_email_reports = False
            
            # Réinitialiser la langue dans session state
            st.session_state.language = "Français"
            
            st.warning("⚠️ Configuration réinitialisée aux valeurs par défaut!")
            st.rerun()
    
    
    # Afficher un résumé des paramètres actuels
    st.markdown("---")
    st.markdown("#### 📋 Résumé de la Configuration Actuelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🤖 Algorithme:**")
        st.markdown(f"- Compétences: {technical_weight:.1%}")
        st.markdown(f"- Expérience: {experience_weight:.1%}")
        st.markdown(f"- Éducation: {education_weight:.1%}")
        st.markdown(f"- **Total:** {technical_weight + experience_weight + education_weight:.1%}")
    
    with col2:
        st.markdown("**🎨 Interface:**")
        st.markdown(f"- Thème: {theme}")
        st.markdown(f"- Langue: {language}")
        st.markdown(f"- Progression: {'✅' if show_progress else '❌'}")
        st.markdown(f"- Détails: {'✅' if show_details else '❌'}")
    
    # Validation des paramètres
    total_weights = technical_weight + experience_weight + education_weight
    if abs(total_weights - 1.0) > 0.01:
        st.warning(f"⚠️ **Attention:** La somme des poids des critères ({total_weights:.1%}) n'est pas égale à 100%")
    
    if excellent_threshold <= good_threshold:
        st.error("❌ **Erreur:** Le seuil 'Excellent' doit être supérieur au seuil 'Très bon'")
    
    if good_threshold <= average_threshold:
        st.error("❌ **Erreur:** Le seuil 'Très bon' doit être supérieur au seuil 'Bon'")

def main():
    """Point d'entrée principal de l'application"""
    set_page_config()
    
    # Vérification de l'authentification
    # Vérifier les paramètres URL pour l'authentification depuis le serveur HTML
    query_params = st.query_params
    if query_params.get('auth') == 'success':
        st.session_state.authenticated = True
        st.session_state.show_home = True
        # Nettoyer les paramètres URL
        st.query_params.clear()
        st.rerun()
    
    # Vérifier si l'utilisateur vient de l'interface d'authentification
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        # Vérifier si l'utilisateur vient de l'interface d'authentification
        # Si l'utilisateur accède directement à localhost:8501, on considère qu'il est authentifié
        # (car il vient de l'interface d'authentification)
        st.session_state.authenticated = True
        st.session_state.logged_in = True
        st.session_state.show_home = False
        st.session_state.show_dashboard = True
        st.session_state.user_name = "Administrateur"
        st.session_state.user_department = "Ministère des Finances"
    
    # Rediriger vers le menu principal après authentification
    if 'show_home' not in st.session_state:
        st.session_state.show_home = True
    
    # En-tête avec bouton de profil
    st.markdown("""
    <style>
    .profile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .profile-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .profile-button {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .profile-button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .profile-icon {
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête avec bouton de profil
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🏛️ {t('app.title')} - {t('app.subtitle')}")
    
    with col2:
        if st.button(f"👤 {t('nav.profile')}", key="profile_button", help="Gérer mon profil utilisateur"):
            st.session_state.show_home = False
            st.session_state.show_dashboard = False
            st.session_state.show_processed_cvs = False
            st.session_state.show_configuration = False
            st.session_state.show_profile = True
            st.session_state.show_analysis = False
            st.rerun()
    
    st.markdown("---")

    # Afficher la sidebar pour l'interface principale
    with st.sidebar:
        st.markdown(f"## 🏛️ {t('app.title')}")
        st.markdown("---")
        st.markdown("### 📊 Navigation")
        
        # CSS moderne pour la navigation
        st.markdown("""
        <style>
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: var(--radius);
            transition: var(--transition);
            cursor: pointer;
            text-decoration: none;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.875rem;
        }
        
        .nav-item:hover {
            background: var(--primary-light);
            color: var(--primary);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: var(--primary);
            color: var(--text-white);
            box-shadow: var(--shadow-sm);
        }
        
        .nav-item.active:hover {
            background: var(--primary-hover);
            transform: translateX(4px);
        }
        
        .nav-icon {
            font-size: 1.125rem;
            width: 1.25rem;
            text-align: center;
        }
        
        .nav-badge {
            margin-left: auto;
            background: var(--success);
            color: white;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: var(--radius-full);
            font-weight: 500;
        }
        
        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }
        
        .sidebar-logo {
            width: 2rem;
            height: 2rem;
            background: var(--primary);
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.875rem;
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Déterminer quelle page est active
        home_active = st.session_state.get('show_home', True)
        dashboard_active = st.session_state.get('show_dashboard', False)
        processed_cvs_active = st.session_state.get('show_processed_cvs', False)
        configuration_active = st.session_state.get('show_configuration', False)
        profile_active = st.session_state.get('show_profile', False)
        analysis_active = st.session_state.get('show_analysis', False)
        
        # Navigation moderne - Suppression des éléments "analyse" et "comparaison"
        nav_items = [
            {
                "key": "nav_home",
                "icon": "🏠",
                "label": t('nav.home'),
                "active": home_active,
                "action": lambda: set_nav_state('home')
            },
            {
                "key": "nav_dashboard", 
                "icon": "📊",
                "label": t('nav.dashboard'),
                "active": dashboard_active,
                "action": lambda: set_nav_state('dashboard')
            },
            {
                "key": "nav_processed_cvs",
                "icon": "📁",
                "label": t('nav.processed_cvs'),
                "active": processed_cvs_active,
                "action": lambda: set_nav_state('processed_cvs')
            },
            {
                "key": "nav_configuration",
                "icon": "⚙️",
                "label": t('nav.configuration'),
                "active": configuration_active,
                "action": lambda: set_nav_state('configuration')
            },
            {
                "key": "nav_new_analysis",
                "icon": "📝",
                "label": t('nav.new_analysis'),
                "active": analysis_active,
                "action": lambda: set_nav_state('analysis'),
                "badge": "Nouveau"
            }
        ]
        
        def set_nav_state(page):
            # Réinitialiser tous les états
            for state in ['show_home', 'show_dashboard', 'show_processed_cvs', 'show_configuration', 'show_profile', 'show_analysis']:
                st.session_state[state] = False
            
            if page == 'home':
                st.session_state.show_home = True
            elif page == 'dashboard':
                st.session_state.show_dashboard = True
            elif page == 'processed_cvs':
                st.session_state.show_processed_cvs = True
            elif page == 'configuration':
                st.session_state.show_configuration = True
            elif page == 'analysis':
                st.session_state.current_page = 1
                st.session_state.job_description = ""
                st.session_state.uploaded_cvs = []
                st.session_state.analysis_complete = False
                st.session_state.ml_results = None
                st.session_state.cv_data = {}
                st.session_state.show_analysis = True
            
            st.rerun()
        
        # Afficher les éléments de navigation
        for item in nav_items:
            if st.button(f"{item['icon']} {item['label']}", use_container_width=True, key=item['key']):
                item['action']()
        
        st.markdown("---")
        st.markdown("### ℹ️ Informations")
        st.markdown("**Version:** 1.0.0")
        st.markdown(f"**{t('app.subtitle')}**")
        
        st.markdown("---")
        if st.button(f"🚪 {t('nav.logout')}", use_container_width=True):
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
    
    render_main_content()

def render_main_content():
    """Rendu du contenu principal selon l'état de l'application"""
    if st.session_state.get('show_analysis', False):
        # Afficher l'interface d'analyse des CVs
        from components.main_interface import render_main_interface
        render_main_interface()
    elif st.session_state.get('show_home', False):
        render_home_page()
    elif st.session_state.get('show_dashboard', False):
        render_dashboard_page()
    elif st.session_state.get('show_processed_cvs', False):
        render_processed_cvs_page()
    elif st.session_state.get('show_configuration', False):
        render_configuration_page()
    elif st.session_state.get('show_profile', False):
        render_profile_page()
    else:
        # Par défaut, afficher la page d'accueil
        render_home_page()

if __name__ == "__main__":
    main()
    if 'config_auto_save' not in st.session_state:
        st.session_state.config_auto_save = True
    if 'config_export_format' not in st.session_state:
        st.session_state.config_export_format = "PDF"
    if 'config_include_charts' not in st.session_state:
        st.session_state.config_include_charts = True
    if 'config_email_reports' not in st.session_state:
        st.session_state.config_email_reports = False
    
    st.markdown(f"### 🔧 {t('config.app_settings')}")
    
    # Paramètres de l'algorithme
    st.markdown(f"#### 🤖 {t('config.algorithm')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{t('config.criteria_weights')}**")
        technical_weight = st.slider(
            t("config.technical_skills"), 
            0.0, 1.0, 
            st.session_state.config_technical_weight, 
            0.05,
            key="slider_technical"
        )
        experience_weight = st.slider(
            t("config.experience"), 
            0.0, 1.0, 
            st.session_state.config_experience_weight, 
            0.05,
            key="slider_experience"
        )
        education_weight = st.slider(
            t("config.education"), 
            0.0, 1.0, 
            st.session_state.config_education_weight, 
            0.05,
            key="slider_education"
        )
    
    with col2:
        st.markdown(f"**{t('config.classification_thresholds')}**")
        excellent_threshold = st.slider(
            t("config.excellent"), 
            0.0, 1.0, 
            st.session_state.config_excellent_threshold, 
            0.05,
            key="slider_excellent"
        )
        good_threshold = st.slider(
            t("config.very_good"), 
            0.0, 1.0, 
            st.session_state.config_good_threshold, 
            0.05,
            key="slider_good"
        )
        average_threshold = st.slider(
            t("config.good"), 
            0.0, 1.0, 
            st.session_state.config_average_threshold, 
            0.05,
            key="slider_average"
        )
    
    # Sauvegarder automatiquement les changements
    st.session_state.config_technical_weight = technical_weight
    st.session_state.config_experience_weight = experience_weight
    st.session_state.config_education_weight = education_weight
    st.session_state.config_excellent_threshold = excellent_threshold
    st.session_state.config_good_threshold = good_threshold
    st.session_state.config_average_threshold = average_threshold
    
    st.markdown("---")
    
    # Paramètres d'affichage
    st.markdown(f"#### 🎨 {t('config.ui_settings')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme_options = ["Clair", "Sombre", "Auto"]
        current_theme = st.session_state.config_theme
        try:
            theme_index = theme_options.index(current_theme)
        except ValueError:
            theme_index = 0  # Clair par défaut
        
        theme = st.selectbox(
            t("config.theme"), 
            theme_options,
            index=theme_index,
            key="select_theme"
        )
        language_options = ["Français", "Anglais"]
        current_lang = st.session_state.config_language
        try:
            current_index = language_options.index(current_lang)
        except ValueError:
            current_index = 0  # Français par défaut
        
        language = st.selectbox(
            t("config.language"), 
            language_options,
            index=current_index,
            key="select_language"
        )
    
    with col2:
        show_progress = st.checkbox(
            t("config.show_progress"), 
            value=st.session_state.config_show_progress,
            key="checkbox_progress"
        )
        show_details = st.checkbox(
            t("config.show_details"), 
            value=st.session_state.config_show_details,
            key="checkbox_details"
        )
    
    # Sauvegarder les paramètres d'affichage
    st.session_state.config_theme = theme
    st.session_state.config_language = language
    st.session_state.config_show_progress = show_progress
    st.session_state.config_show_details = show_details
    
    # Mettre à jour la langue immédiatement pour que t() fonctionne
    st.session_state.language = language
    
    st.markdown("---")
    
    # Paramètres d'export
    # Configuration automatique - pas d'interface utilisateur
    st.session_state.config_auto_save = True  # Toujours activé
    st.session_state.config_export_format = "PDF"  # Toujours PDF
    st.session_state.config_include_charts = True  # Toujours activé
    st.session_state.config_email_reports = False  # Toujours désactivé
    
    st.markdown("---")
    
    # Boutons d'action simplifiés
    st.markdown(f"#### 🎛️ {t('config.actions')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💾 {t('config.save_config')}", use_container_width=True):
            # Sauvegarder dans un fichier JSON
            import json
            config_data = {
                "technical_weight": technical_weight,
                "experience_weight": experience_weight,
                "education_weight": education_weight,
                "excellent_threshold": excellent_threshold,
                "good_threshold": good_threshold,
                "average_threshold": average_threshold,
                "theme": theme,
                "language": language,
                "show_progress": show_progress,
                "show_details": show_details,
                "auto_save": True,  # Toujours activé
                "export_format": "PDF",  # Toujours PDF
                "include_charts": True,  # Toujours activé
                "email_reports": False  # Toujours désactivé
            }
            
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Mettre à jour la session state immédiatement AVANT d'afficher les messages
            st.session_state.language = language
            st.session_state.config_theme = theme
            st.session_state.config_language = language
            st.session_state.config_show_progress = show_progress
            st.session_state.config_show_details = show_details
            st.session_state.config_auto_save = True  # Toujours activé
            st.session_state.config_export_format = "PDF"  # Toujours PDF
            st.session_state.config_include_charts = True  # Toujours activé
            st.session_state.config_email_reports = False  # Toujours désactivé
            
            # Message de succès dans la langue appropriée
            if language == "Anglais":
                st.success("✅ Configuration saved successfully!")
            else:
                st.success("✅ Configuration sauvegardée avec succès!")
            st.balloons()
            
            # Forcer le rechargement pour appliquer les changements
            if language == "Anglais":
                st.markdown("🔄 **Restarting application to apply changes...**")
            else:
                st.markdown("🔄 **Redémarrage de l'application pour appliquer les changements...**")
            
            # Attendre un peu pour que l'utilisateur voie le message
            import time
            time.sleep(2)
            
            # Ajouter un timestamp pour forcer le rechargement
            st.session_state.language_timestamp = time.time()
            
            # Forcer un rechargement complet de la page
            try:
                st.experimental_rerun()
            except:
                st.rerun()
    
    with col2:
        if st.button(f"🔄 {t('config.reset')}", use_container_width=True):
            # Réinitialiser aux valeurs par défaut
            st.session_state.config_technical_weight = 0.50
            st.session_state.config_experience_weight = 0.30
            st.session_state.config_education_weight = 0.20
            st.session_state.config_excellent_threshold = 0.8
            st.session_state.config_good_threshold = 0.6
            st.session_state.config_average_threshold = 0.4
            st.session_state.config_theme = "Clair"
            st.session_state.config_language = "Français"
            st.session_state.config_show_progress = True
            st.session_state.config_show_details = True
            st.session_state.config_auto_save = True
            st.session_state.config_export_format = "PDF"
            st.session_state.config_include_charts = True
            st.session_state.config_email_reports = False
            
            # Réinitialiser la langue dans session state
            st.session_state.language = "Français"
            
            st.warning("⚠️ Configuration réinitialisée aux valeurs par défaut!")
            st.rerun()
    
    
    # Afficher un résumé des paramètres actuels
    st.markdown("---")
    st.markdown("#### 📋 Résumé de la Configuration Actuelle")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🤖 Algorithme:**")
        st.markdown(f"- Compétences: {technical_weight:.1%}")
        st.markdown(f"- Expérience: {experience_weight:.1%}")
        st.markdown(f"- Éducation: {education_weight:.1%}")
        st.markdown(f"- **Total:** {technical_weight + experience_weight + education_weight:.1%}")
    
    with col2:
        st.markdown("**🎨 Interface:**")
        st.markdown(f"- Thème: {theme}")
        st.markdown(f"- Langue: {language}")
        st.markdown(f"- Progression: {'✅' if show_progress else '❌'}")
        st.markdown(f"- Détails: {'✅' if show_details else '❌'}")
    
    # Validation des paramètres
    total_weights = technical_weight + experience_weight + education_weight
    if abs(total_weights - 1.0) > 0.01:
        st.warning(f"⚠️ **Attention:** La somme des poids des critères ({total_weights:.1%}) n'est pas égale à 100%")
    
    if excellent_threshold <= good_threshold:
        st.error("❌ **Erreur:** Le seuil 'Excellent' doit être supérieur au seuil 'Très bon'")
    
    if good_threshold <= average_threshold:
        st.error("❌ **Erreur:** Le seuil 'Très bon' doit être supérieur au seuil 'Bon'")

def main():
    """Point d'entrée principal de l'application"""
    set_page_config()
    
    # Vérification de l'authentification
    # Vérifier les paramètres URL pour l'authentification depuis le serveur HTML
    query_params = st.query_params
    if query_params.get('auth') == 'success':
        st.session_state.authenticated = True
        st.session_state.show_home = True
        # Nettoyer les paramètres URL
        st.query_params.clear()
        st.rerun()
    
    # Vérifier si l'utilisateur vient de l'interface d'authentification
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        # Vérifier si l'utilisateur vient de l'interface d'authentification
        # Si l'utilisateur accède directement à localhost:8501, on considère qu'il est authentifié
        # (car il vient de l'interface d'authentification)
        st.session_state.authenticated = True
        st.session_state.logged_in = True
        st.session_state.show_home = False
        st.session_state.show_dashboard = True
        st.session_state.user_name = "Administrateur"
        st.session_state.user_department = "Ministère des Finances"
    
    # Rediriger vers le menu principal après authentification
    if 'show_home' not in st.session_state:
        st.session_state.show_home = True
    
    # En-tête avec bouton de profil
    st.markdown("""
    <style>
    .profile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .profile-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .profile-button {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .profile-button:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .profile-icon {
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête avec bouton de profil
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🏛️ {t('app.title')} - {t('app.subtitle')}")
    
    with col2:
        if st.button(f"👤 {t('nav.profile')}", key="profile_button", help="Gérer mon profil utilisateur"):
            st.session_state.show_home = False
            st.session_state.show_dashboard = False
            st.session_state.show_processed_cvs = False
            st.session_state.show_configuration = False
            st.session_state.show_profile = True
            st.session_state.show_analysis = False
            st.rerun()
    
    st.markdown("---")

    # Afficher la sidebar pour l'interface principale
    with st.sidebar:
        st.markdown(f"## 🏛️ {t('app.title')}")
        st.markdown("---")
        st.markdown("### 📊 Navigation")
        
        # CSS moderne pour la navigation
        st.markdown("""
        <style>
        .nav-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: var(--radius);
            transition: var(--transition);
            cursor: pointer;
            text-decoration: none;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.875rem;
        }
        
        .nav-item:hover {
            background: var(--primary-light);
            color: var(--primary);
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: var(--primary);
            color: var(--text-white);
            box-shadow: var(--shadow-sm);
        }
        
        .nav-item.active:hover {
            background: var(--primary-hover);
            transform: translateX(4px);
        }
        
        .nav-icon {
            font-size: 1.125rem;
            width: 1.25rem;
            text-align: center;
        }
        
        .nav-badge {
            margin-left: auto;
            background: var(--success);
            color: white;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: var(--radius-full);
            font-weight: 500;
        }
        
        .sidebar-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }
        
        .sidebar-logo {
            width: 2rem;
            height: 2rem;
            background: var(--primary);
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.875rem;
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Déterminer quelle page est active
        home_active = st.session_state.get('show_home', True)
        dashboard_active = st.session_state.get('show_dashboard', False)
        processed_cvs_active = st.session_state.get('show_processed_cvs', False)
        configuration_active = st.session_state.get('show_configuration', False)
        profile_active = st.session_state.get('show_profile', False)
        analysis_active = st.session_state.get('show_analysis', False)
        
        # Navigation moderne - Suppression des éléments "analyse" et "comparaison"
        nav_items = [
            {
                "key": "nav_home",
                "icon": "🏠",
                "label": t('nav.home'),
                "active": home_active,
                "action": lambda: set_nav_state('home')
            },
            {
                "key": "nav_dashboard", 
                "icon": "📊",
                "label": t('nav.dashboard'),
                "active": dashboard_active,
                "action": lambda: set_nav_state('dashboard')
            },
            {
                "key": "nav_processed_cvs",
                "icon": "📁",
                "label": t('nav.processed_cvs'),
                "active": processed_cvs_active,
                "action": lambda: set_nav_state('processed_cvs')
            },
            {
                "key": "nav_configuration",
                "icon": "⚙️",
                "label": t('nav.configuration'),
                "active": configuration_active,
                "action": lambda: set_nav_state('configuration')
            },
            {
                "key": "nav_new_analysis",
                "icon": "📝",
                "label": t('nav.new_analysis'),
                "active": analysis_active,
                "action": lambda: set_nav_state('analysis'),
                "badge": "Nouveau"
            }
        ]
        
        def set_nav_state(page):
            # Réinitialiser tous les états
            for state in ['show_home', 'show_dashboard', 'show_processed_cvs', 'show_configuration', 'show_profile', 'show_analysis']:
                st.session_state[state] = False
            
            if page == 'home':
                st.session_state.show_home = True
            elif page == 'dashboard':
                st.session_state.show_dashboard = True
            elif page == 'processed_cvs':
                st.session_state.show_processed_cvs = True
            elif page == 'configuration':
                st.session_state.show_configuration = True
            elif page == 'analysis':
                st.session_state.current_page = 1
                st.session_state.job_description = ""
                st.session_state.uploaded_cvs = []
                st.session_state.analysis_complete = False
                st.session_state.ml_results = None
                st.session_state.cv_data = {}
                st.session_state.show_analysis = True
            
            st.rerun()
        
        # Afficher les éléments de navigation
        for item in nav_items:
            if st.button(f"{item['icon']} {item['label']}", use_container_width=True, key=item['key']):
                item['action']()
        
        st.markdown("---")
        st.markdown("### ℹ️ Informations")
        st.markdown("**Version:** 1.0.0")
        st.markdown(f"**{t('app.subtitle')}**")
        
        st.markdown("---")
        if st.button(f"🚪 {t('nav.logout')}", use_container_width=True):
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
    
    render_main_content()

def render_main_content():
    """Rendu du contenu principal selon l'état de l'application"""
    if st.session_state.get('show_analysis', False):
        # Afficher l'interface d'analyse des CVs
        from components.main_interface import render_main_interface
        render_main_interface()
    elif st.session_state.get('show_home', False):
        render_home_page()
    elif st.session_state.get('show_dashboard', False):
        render_dashboard_page()
    elif st.session_state.get('show_processed_cvs', False):
        render_processed_cvs_page()
    elif st.session_state.get('show_configuration', False):
        render_configuration_page()
    elif st.session_state.get('show_profile', False):
        render_profile_page()
    else:
        # Par défaut, afficher la page d'accueil
        render_home_page()

if __name__ == "__main__":
    main()