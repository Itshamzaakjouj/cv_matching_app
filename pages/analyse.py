"""
Page d'analyse des CVs - TalentScope
"""
import streamlit as st
import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.ui_elements import HeaderComponent
from components.metrics import ProgressIndicator, CVCard, get_sample_cv_data
from i18n import t

# Configuration de la page
st.set_page_config(
    page_title="TalentScope - Analyse",
    page_icon="🔍",
    layout="wide"
)

def render_analysis_interface():
    """Interface d'analyse des CVs"""
    HeaderComponent.render()
    
    st.markdown("## 🔍 Analyse des CVs")
    
    # Indicateur de progression
    steps = ["Saisie de l'offre", "Importation des CVs", "Vérification", "Résultats"]
    current_step = st.session_state.get('current_page', 1)
    progress = ProgressIndicator(steps, current_step)
    progress.render()
    
    # Interface selon l'étape
    if current_step == 1:
        render_step_1()
    elif current_step == 2:
        render_step_2()
    elif current_step == 3:
        render_step_3()
    elif current_step == 4:
        render_step_4()

def render_step_1():
    """Étape 1: Saisie de l'offre d'emploi"""
    st.markdown("### 📝 Saisie de l'offre d'emploi")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_description = st.text_area(
            "Description du poste",
            placeholder="Exemple: Développeur Python senior avec 5 ans d'expérience en machine learning...",
            height=200,
            key="job_description"
        )
        
        # Critères de sélection
        st.markdown("#### 🎯 Critères de sélection")
        col_a, col_b = st.columns(2)
        
        with col_a:
            technical_weight = st.slider("Poids des compétences techniques", 0.0, 1.0, 0.4)
            experience_weight = st.slider("Poids de l'expérience", 0.0, 1.0, 0.3)
        
        with col_b:
            education_weight = st.slider("Poids de l'éducation", 0.0, 1.0, 0.2)
            soft_skills_weight = st.slider("Poids des compétences douces", 0.0, 1.0, 0.1)
    
    with col2:
        st.markdown("#### 💡 Conseils")
        st.info("""
        **Pour de meilleurs résultats :**
        - Soyez spécifique sur les technologies
        - Mentionnez les années d'expérience requises
        - Précisez le niveau d'études souhaité
        - Ajoutez des compétences particulières
        """)
        
        st.markdown("#### 📊 Aperçu")
        if job_description:
            word_count = len(job_description.split())
            st.metric("Mots", word_count)
            st.metric("Caractères", len(job_description))
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Suivant →", type="primary", use_container_width=True):
            if job_description.strip():
                st.session_state.current_page = 2
                st.session_state.job_description = job_description
                st.session_state.weights = {
                    'technical': technical_weight,
                    'experience': experience_weight,
                    'education': education_weight,
                    'soft_skills': soft_skills_weight
                }
                st.rerun()
            else:
                st.error("Veuillez saisir une description du poste")

def render_step_2():
    """Étape 2: Importation des CVs"""
    st.markdown("### 📁 Importation des CVs")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Choisir les fichiers CV",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Formats supportés: PDF, DOCX, TXT"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} fichier(s) importé(s)")
            
            # Aperçu des fichiers
            st.markdown("#### 📋 Fichiers sélectionnés")
            for i, file in enumerate(uploaded_files):
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.write(f"📄 {file.name}")
                with col_b:
                    st.write(f"{file.size / 1024:.1f} KB")
                with col_c:
                    if st.button("❌", key=f"remove_{i}"):
                        # Logique de suppression
                        pass
        
        # Options d'importation
        st.markdown("#### ⚙️ Options d'importation")
        auto_process = st.checkbox("Traiter automatiquement après import", value=True)
        extract_keywords = st.checkbox("Extraire les mots-clés automatiquement", value=True)
    
    with col2:
        st.markdown("#### 📊 Statistiques")
        if uploaded_files:
            total_size = sum(f.size for f in uploaded_files)
            st.metric("Fichiers", len(uploaded_files))
            st.metric("Taille totale", f"{total_size / 1024:.1f} KB")
        
        st.markdown("#### 💡 Conseils")
        st.info("""
        **Formats recommandés :**
        - PDF : Meilleure qualité
        - DOCX : Facile à traiter
        - TXT : Rapide mais basique
        """)
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Précédent", use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()
    with col3:
        if st.button("Suivant →", type="primary", use_container_width=True):
            if uploaded_files:
                st.session_state.current_page = 3
                st.session_state.uploaded_files = uploaded_files
                st.rerun()
            else:
                st.error("Veuillez importer au moins un CV")

def render_step_3():
    """Étape 3: Vérification des données"""
    st.markdown("### ✅ Vérification des données")
    
    # Simulation de la vérification
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Analyse des fichiers...",
        "Extraction du texte...",
        "Identification des compétences...",
        "Calcul des scores...",
        "Génération des résultats..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        import time
        time.sleep(0.5)
    
    st.success("✅ Vérification terminée!")
    
    # Résumé de la vérification
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("CVs traités", len(st.session_state.get('uploaded_files', [])))
    with col2:
        st.metric("Compétences identifiées", 45)
    with col3:
        st.metric("Temps de traitement", "2.3s")
    
    # Aperçu des données extraites
    st.markdown("#### 📋 Aperçu des données extraites")
    sample_data = get_sample_cv_data()
    preview_df = pd.DataFrame(sample_data[:3])
    st.dataframe(preview_df[['name', 'score', 'status', 'position']], use_container_width=True)
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Précédent", use_container_width=True):
            st.session_state.current_page = 2
            st.rerun()
    with col3:
        if st.button("Voir les résultats →", type="primary", use_container_width=True):
            st.session_state.current_page = 4
            st.rerun()

def render_step_4():
    """Étape 4: Résultats de l'analyse"""
    st.markdown("### 📊 Résultats de l'analyse")
    
    # Filtres et tri
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sort_by = st.selectbox("Trier par", ["Score", "Nom", "Statut"])
    with col2:
        min_score = st.slider("Score minimum", 0, 100, 0)
    with col3:
        status_filter = st.multiselect("Statut", ["Excellent", "Très bon", "Bon", "Moyen"])
    
    # Résultats
    cv_data = get_sample_cv_data()
    
    # Filtrage
    filtered_data = [cv for cv in cv_data if cv['score'] >= min_score]
    if status_filter:
        filtered_data = [cv for cv in filtered_data if cv['status'] in status_filter]
    
    # Tri
    if sort_by == "Score":
        filtered_data.sort(key=lambda x: x['score'], reverse=True)
    elif sort_by == "Nom":
        filtered_data.sort(key=lambda x: x['name'])
    elif sort_by == "Statut":
        filtered_data.sort(key=lambda x: x['status'])
    
    # Affichage des résultats
    for cv in filtered_data:
        with st.expander(f"📄 {cv['name']} - {cv['score']}% ({cv['status']})", expanded=False):
            CVCard(
                name=cv['name'],
                score=cv['score'],
                status=cv['status'],
                position=cv['position'],
                skills=cv['skills'],
                date=cv['date']
            ).render(show_skills=True)
            
            # Détails supplémentaires
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Compétences techniques", f"{cv['score'] * 0.8:.1f}%")
            with col2:
                st.metric("Expérience", f"{cv['score'] * 0.6:.1f}%")
            with col3:
                st.metric("Éducation", f"{cv['score'] * 0.7:.1f}%")
    
    # Actions
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Nouvelle analyse", use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()
    with col2:
        if st.button("📊 Comparer", use_container_width=True):
            st.session_state.show_comparison = True
            st.rerun()
    with col3:
        if st.button("💾 Exporter", use_container_width=True):
            st.success("Export en cours...")

def main():
    """Fonction principale"""
    render_analysis_interface()

if __name__ == "__main__":
    main()
