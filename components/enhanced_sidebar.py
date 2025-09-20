import streamlit as st

def render_enhanced_sidebar():
    with st.sidebar:
        # Logo et titre
        st.image("Logos/Ministere_eco_finances.png", width=200)
        st.title("TalentScope")
        
        st.markdown("---")
        
        # Guide d'utilisation
        st.markdown("### 📖 Guide d'utilisation")
        
        with st.expander("🔍 Analyse des CVs", expanded=False):
            st.markdown("""
            1. **Description du poste**
               - Saisissez la description détaillée
               - Plus la description est précise, meilleure sera l'analyse
            
            2. **Chargement des CVs**
               - Les CVs sont chargés automatiquement
               - Format accepté : PDF
            
            3. **Analyse**
               - L'algorithme compare les CVs avec le poste
               - Utilise l'IA pour extraire les informations pertinentes
            
            4. **Résultats**
               - Score de correspondance pour chaque CV
               - Visualisation détaillée des compétences
            """)
        
        with st.expander("📊 Comparaison", expanded=False):
            st.markdown("""
            - Comparaison visuelle des CVs
            - Graphiques interactifs
            - Analyse des points forts/faibles
            """)
        
        with st.expander("📈 Dashboard", expanded=False):
            st.markdown("""
            - Statistiques globales
            - Historique des analyses
            - Métriques de performance
            """)
        
        st.markdown("---")
        
        # Pondération des critères
        st.markdown("### ⚖️ Pondération actuelle")
        
        # Récupérer les poids personnalisés ou utiliser les valeurs par défaut
        weights = st.session_state.get('custom_weights', {
            'skills_weight': 0.3,
            'experience_weight': 0.25,
            'education_weight': 0.2,
            'certifications_weight': 0.15,
            'languages_weight': 0.1
        })
        
        # Afficher les poids actuels avec des barres de progression
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Compétences**")
        with col2:
            st.markdown(f"**{int(weights['skills_weight']*100)}%**")
        st.progress(weights['skills_weight'])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Expérience**")
        with col2:
            st.markdown(f"**{int(weights['experience_weight']*100)}%**")
        st.progress(weights['experience_weight'])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Formation**")
        with col2:
            st.markdown(f"**{int(weights['education_weight']*100)}%**")
        st.progress(weights['education_weight'])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Certifications**")
        with col2:
            st.markdown(f"**{int(weights['certifications_weight']*100)}%**")
        st.progress(weights['certifications_weight'])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Langues**")
        with col2:
            st.markdown(f"**{int(weights['languages_weight']*100)}%**")
        st.progress(weights['languages_weight'])
        
        st.markdown("---")
        
        # Profil utilisateur
        if st.session_state.get('authenticated', False):
            st.markdown("### 👤 Profil")
            st.markdown(f"**Email:** {st.session_state.get('user_email', 'N/A')}")
            
            if st.button("🚪 Déconnexion", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()



