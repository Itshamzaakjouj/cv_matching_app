"""
Composants de la barre latérale
"""
import streamlit as st
from firebase_config import firebase_auth

def render_configuration_modal():
    """Affiche le modal de configuration"""
    if st.session_state.get('show_config', False):
        with st.sidebar:
            st.subheader("⚙️ Configuration")
            
            # Configuration des seuils
            st.write("Seuils de correspondance")
            
            # Seuil global
            global_threshold = st.slider(
                "Seuil global",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get('global_threshold', 0.6),
                step=0.1,
                help="Seuil minimal de correspondance pour considérer un CV comme pertinent"
            )
            
            # Seuils par critère
            st.write("Seuils par critère")
            
            education_threshold = st.slider(
                "Formation",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get('education_threshold', 0.5),
                step=0.1
            )
            
            experience_threshold = st.slider(
                "Expérience",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get('experience_threshold', 0.5),
                step=0.1
            )
            
            skills_threshold = st.slider(
                "Compétences",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get('skills_threshold', 0.5),
                step=0.1
            )
            
            # Sauvegarder les configurations
            if st.button("Sauvegarder", type="primary"):
                st.session_state['global_threshold'] = global_threshold
                st.session_state['education_threshold'] = education_threshold
                st.session_state['experience_threshold'] = experience_threshold
                st.session_state['skills_threshold'] = skills_threshold
                st.success("✅ Configuration sauvegardée")
                st.session_state['show_config'] = False
                st.rerun()
            
            # Bouton pour fermer le modal
            if st.button("Fermer"):
                st.session_state['show_config'] = False
                st.rerun()

def render_sidebar():
    """Affiche la barre latérale"""
    with st.sidebar:
        st.title("🎯 TalentScope")
        
        # Menu principal
        st.subheader("📋 Menu")
        
        # Tableau de bord
        if st.button("📊 Tableau de bord", use_container_width=True):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
        
        # Comparaison de CV
        if st.button("🔍 Comparaison de CV", use_container_width=True):
            st.session_state['current_page'] = 'cv_comparison'
            st.rerun()
        
        # Configuration
        if st.button("⚙️ Configuration", use_container_width=True):
            st.session_state['show_config'] = True
            st.rerun()
        
        st.markdown("---")
        
        # Profil utilisateur
        render_user_profile_section()
        
        st.markdown("---")
        
        # Déconnexion
        if st.button("🚪 Se déconnecter", use_container_width=True):
            # Réinitialiser la session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def render_user_profile_section():
    """Affiche la section profil utilisateur"""
    if st.session_state.get('authenticated', False):
        # Récupérer les informations utilisateur depuis la session
        user_info = st.session_state.get('user', {})
        user_email = st.session_state.get('user_email', 'Utilisateur')
        
        # Afficher les informations utilisateur
        st.subheader("👤 Profil")
        st.write(f"📧 {user_email}")
        
        # Rôle utilisateur
        role = "Administrateur" if user_email == "admin@mef.gov.ma" else "Utilisateur"
        st.write(f"🎭 Rôle : {role}")
    else:
        st.warning("Non connecté")