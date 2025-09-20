"""
Interface principale de l'application TalentScope
"""
import streamlit as st
import pandas as pd
from processing import rank_cvs
from export_utils import render_export_buttons
from i18n import t

# La configuration de la page est gérée dans launch_ultra_simple.py

def init_session_state():
    """Initialise l'état de la session"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'uploaded_cvs' not in st.session_state:
        st.session_state.uploaded_cvs = []

def render_progress_bar():
    """Affiche la barre de progression"""
    current_page = int(st.session_state.current_page) if isinstance(st.session_state.current_page, str) else st.session_state.current_page
    
    # Calculer le pourcentage de progression (0% à 100%)
    if current_page == 1:
        progress = 25  # 25% pour la page 1
    elif current_page == 2:
        progress = 50  # 50% pour la page 2
    elif current_page == 3:
        progress = 75  # 75% pour la page 3
    elif current_page == 4:
        progress = 100  # 100% pour la page 4
    else:
        progress = 0
    
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
            font-size: 0.875rem;">
            <span style="color: {'#1976D2' if current_page >= 1 else '#64748b'}">{t('step.verify.job')}</span>
            <span style="color: {'#1976D2' if current_page >= 2 else '#64748b'}">CVs</span>
            <span style="color: {'#1976D2' if current_page >= 3 else '#64748b'}">{t('step.verify.title')}</span>
            <span style="color: {'#1976D2' if current_page >= 4 else '#64748b'}">{t('step.results.title')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_1():
    """Page 1: Saisie de l'offre d'emploi - Optimisée"""
    st.markdown(f"### 📝 {t('step.job.title')}")
    st.markdown(t('step.job.help'))
    
    # Zone de saisie optimisée
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    ">
    """, unsafe_allow_html=True)
    
    job_description = st.text_area(
        t('step.job.text'),
        value=st.session_state.job_description,
        height=200,
        placeholder=t('step.job.placeholder'),
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.session_state.job_description = job_description
    
    # Bouton optimisé
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(t('btn.next'), key="next_page_1", use_container_width=True, type="primary"):
            if job_description.strip():
                st.session_state.current_page = 2
                st.rerun()
            else:
                st.error(t('error.job_required'))

def page_2():
    """Page 2: Importation des CVs - Optimisée"""
    st.markdown(f"### 📁 {t('step.upload.title')}")
    st.markdown(t('step.upload.help'))
    
    # Zone d'upload optimisée
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #2196f3;
        margin: 1rem 0;
        text-align: center;
    ">
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        t('step.upload.input'),
        type=['pdf'],
        accept_multiple_files=True,
        help=t('step.upload.help_input'),
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_files:
        st.session_state.uploaded_cvs = uploaded_files
        st.success(f"✅ {len(uploaded_files)} {t('step.upload.success')}")
        
        # Afficher la liste des fichiers
        st.markdown(f"**{t('step.upload.selected')}**")
        for i, file in enumerate(uploaded_files, 1):
            st.write(f"{i}. {file.name}")
    
    # Boutons de navigation optimisés
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button(t('btn.prev'), key="prev_page_2", use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()
    
    with col3:
        if st.button(t('btn.next'), key="next_page_2", use_container_width=True, type="primary"):
            if uploaded_files:
                st.session_state.current_page = 3
                st.rerun()
            else:
                st.error(t('error.upload_required'))

def page_3():
    """Page 3: Vérification des données - Optimisée côte à côte"""
    st.markdown(f"### ✅ {t('step.verify.title')}")
    st.markdown(t("step.verify.help"))
    
    # Layout côte à côte optimisé
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        # Offre d'emploi - Côté gauche
        st.markdown(f"#### 📝 {t('step.verify.job')}")
        
        # Card moderne pour l'offre d'emploi
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #2196f3;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.1);
            margin-bottom: 1rem;
        ">
        """, unsafe_allow_html=True)
        
        st.text_area(
            t('step.job.text'), 
            value=st.session_state.job_description, 
            height=200, 
            disabled=True,
            label_visibility="collapsed"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        # CVs sélectionnés - Côté droit
        st.markdown(f"#### 📁 {t('step.verify.cv')}")
        
        if st.session_state.uploaded_cvs:
            # Card moderne pour les CVs
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 5px solid #9c27b0;
                box-shadow: 0 4px 15px rgba(156, 39, 176, 0.1);
                margin-bottom: 1rem;
            ">
            """, unsafe_allow_html=True)
            
            # Liste des CVs avec icônes
            for i, file in enumerate(st.session_state.uploaded_cvs, 1):
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: center;
                    padding: 0.75rem;
                    background: white;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                ">
                    <span style="
                        background: #9c27b0;
                        color: white;
                        border-radius: 50%;
                        width: 30px;
                        height: 30px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 1rem;
                        font-weight: bold;
                    ">{i}</span>
                    <span style="font-weight: 500; color: #333;">{file.name}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Statistiques des CVs
            st.markdown(f"""
            <div style="
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-top: 1rem;
            ">
                <h4 style="margin: 0; color: #6c757d;">📊 Résumé</h4>
                <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold; color: #9c27b0;">
                    {len(st.session_state.uploaded_cvs)} CV(s) sélectionné(s)
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(t('step.verify.none'))
    
    # Boutons de navigation optimisés
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button(f"← {t('btn.prev')}", key="prev_page_3", use_container_width=True, type="secondary"):
            st.session_state.current_page = 2
            st.rerun()
    
    with col2:
        # Indicateur de statut
        if st.session_state.job_description and st.session_state.uploaded_cvs:
            st.success("✅ Prêt pour l'analyse")
        else:
            st.error("❌ Données incomplètes")
    
    with col3:
        if st.button(f"🚀 {t('btn.start')}", key="start_analysis", use_container_width=True, type="primary"):
            if st.session_state.job_description and st.session_state.uploaded_cvs:
                st.session_state.current_page = 4
                st.rerun()
            else:
                st.error(t('error.incomplete'))

def page_4():
    """Page 4: Résultats de l'analyse - Optimisée"""
    st.markdown(f"### 📊 {t('step.results.title')}")
    
    # Vérifier que nous avons des données
    if not st.session_state.job_description or not st.session_state.uploaded_cvs:
        st.error(t('error.no_data'))
        return
    
    # Simulation d'analyse avec indicateur de progression moderne
    progress_container = st.container()
    with progress_container:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        ">
            <h3 style="margin: 0 0 1rem 0;">🤖 Analyse en cours avec IA...</h3>
            <p style="margin: 0; opacity: 0.9;">Traitement des CVs avec algorithmes de Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Barre de progression animée
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        import time
        steps = [
            "📄 Extraction du contenu des CVs...",
            "🔍 Analyse des compétences techniques...",
            "💼 Évaluation de l'expérience professionnelle...",
            "🎓 Vérification du niveau d'éducation...",
            "🧠 Calcul des scores avec IA...",
            "📊 Génération des résultats..."
        ]
        
        for i, step in enumerate(steps):
            status_text.markdown(f"**{step}**")
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.3)
        
        st.success("✅ Analyse terminée avec succès !")
    
    # Résultats avec design moderne
    st.markdown(f"#### 🏆 {t('results.classification')}")
    
    # Données simulées pour la démo
    sample_results = [
        {"name": "cv_Hamza.pdf", "score": 91.3, "status": "Excellent", "color": "#4CAF50", "icon": "🥇"},
        {"name": "cv_Adam.pdf", "score": 85.2, "status": "Excellent", "color": "#4CAF50", "icon": "🥇"},
        {"name": "cv_Sophia.pdf", "score": 76.1, "status": "Très bon", "color": "#8BC34A", "icon": "🥈"},
        {"name": "cv_Ali.pdf", "score": 72.8, "status": "Très bon", "color": "#8BC34A", "icon": "🥈"},
        {"name": "cv_Hafsa.pdf", "score": 68.5, "status": "Bon", "color": "#FFC107", "icon": "🥉"},
        {"name": "cv_Yassine.pdf", "score": 63.2, "status": "Bon", "color": "#FFC107", "icon": "🥉"}
    ]
    
    # Affichage des résultats en cartes modernes
    for i, result in enumerate(sample_results, 1):
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid {result['color']};
            transition: transform 0.3s ease;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="
                        background: {result['color']};
                        color: white;
                        border-radius: 50%;
                        width: 40px;
                        height: 40px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 1rem;
                        font-weight: bold;
                        font-size: 1.2rem;
                    ">{i}</span>
                    <div>
                        <h4 style="margin: 0; color: #333;">{result['icon']} {result['name']}</h4>
                        <p style="margin: 0.25rem 0; color: #666; font-size: 0.9rem;">Score de compatibilité</p>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="
                        background: {result['color']};
                        color: white;
                        padding: 0.5rem 1rem;
                        border-radius: 20px;
                        font-weight: bold;
                        font-size: 1.1rem;
                        margin-bottom: 0.5rem;
                    ">{result['score']}%</div>
                    <div style="
                        color: {result['color']};
                        font-weight: 600;
                        font-size: 0.9rem;
                    ">{result['status']}</div>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <div style="
                    width: 100%;
                    height: 8px;
                    background: #e0e0e0;
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {result['score']}%;
                        height: 100%;
                        background: linear-gradient(90deg, {result['color']} 0%, {result['color']}80 100%);
                        border-radius: 4px;
                        transition: width 0.5s ease;
                    "></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistiques globales modernes
    st.markdown("---")
    st.markdown("#### 📈 Statistiques Globales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h3 style="margin: 0; font-size: 2rem;">6</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">CVs Analysés</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h3 style="margin: 0; font-size: 2rem;">76.2%</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Score Moyen</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h3 style="margin: 0; font-size: 2rem;">91.3%</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Meilleur Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
        ">
            <h3 style="margin: 0; font-size: 2rem;">2</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Excellent</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Boutons de navigation optimisés
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Précédent", key="prev_page_4", use_container_width=True, type="secondary"):
            st.session_state.current_page = 3
            st.rerun()
    
    with col2:
        if st.button("📊 Voir Comparaison", key="view_comparison", use_container_width=True):
            st.info("Fonctionnalité de comparaison en cours de développement")
    
    with col3:
        if st.button("🔄 Nouvelle Analyse", key="new_analysis", use_container_width=True, type="primary"):
            st.session_state.current_page = 1
            st.session_state.job_description = ""
            st.session_state.uploaded_cvs = []
            st.rerun()

def render_cv_analysis_tab():
    """Affiche l'onglet d'analyse des CVs avec un processus en 4 étapes"""
    render_progress_bar()
    
    current_page = int(st.session_state.current_page) if isinstance(st.session_state.current_page, str) else st.session_state.current_page
    if current_page == 1:
        page_1()
    elif current_page == 2:
        page_2()
    elif current_page == 3:
        page_3()
    elif current_page == 4:
        page_4()

def render_main_interface():
    """Affiche l'interface principale de l'application"""
    init_session_state()
    
    # CSS pour l'interface
    st.markdown("""
    <style>
    .main-content {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-title {
        color: #1976D2;
        font-size: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .stCard {
        /* Supprimé - plus de rectangle blanc */
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">CV Analysis</h2>', unsafe_allow_html=True)
    render_cv_analysis_tab()
    st.markdown('</div>', unsafe_allow_html=True)
