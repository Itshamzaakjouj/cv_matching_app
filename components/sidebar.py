"""
Composant Sidebar pour TalentScope
"""
import streamlit as st
from i18n import t

def render_user_profile():
    """Affiche le profil de l'utilisateur"""
    st.markdown("""
    <style>
    .user-profile {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .user-profile-header {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .user-initial {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #0077B6, #00B4D8);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 1rem;
    }
    .user-status {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        background-color: #4CAF50;
        color: white;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'user' in st.session_state:
        user_info = st.session_state.user['users'][0]
        display_name = user_info.get('displayName', user_info['email'].split('@')[0])
        initial = display_name[0].upper() if display_name else 'U'
        
        st.markdown(f"""
        <div class="user-profile">
            <div class="user-profile-header">
                <div class="user-initial">{initial}</div>
                <div>
                    <h3 style="margin: 0; color: #0077B6;">{display_name}</h3>
                    <small style="color: #666;">{user_info['email']}</small>
                </div>
            </div>
            <div class="user-status">{t('btn.login')}</div>
        </div>
        """, unsafe_allow_html=True)

def render_usage_guide():
    """Affiche le guide d'utilisation"""
    with st.expander("📖 User guide", expanded=False):
        st.markdown("""
        ### How to use TalentScope

        1. **Job description** 📝
           - Enter a detailed job description
           - Include required skills
           - Specify desired experience level

        2. **CV analysis** 📊
           - Upload one or more CVs (PDF)
           - The system will automatically analyze matches
           - View scores and rankings

        3. **Results and comparison** 🎯
           - View the detailed dashboard
           - Compare profiles side by side
           - Export results to PDF or Excel

        4. **Customization** ⚙️
           - Adjust criteria weights
           - Refine searched keywords
           - Save your preferences
        """)

def render_criteria_weights():
    """Affiche les contrôles de pondération des critères"""
    with st.expander("⚖️ Criteria weighting", expanded=False):
        st.markdown("""
        Adjust the relative importance of each criterion for CV analysis.
        The sum of weights must equal 100%.
        """)
        
        # Valeurs par défaut
        if 'weights' not in st.session_state:
            st.session_state.weights = {
                'technical_skills': 40,
                'experience': 30,
                'education': 20,
                'soft_skills': 10
            }
        
        # Sliders pour chaque critère
        st.session_state.weights['technical_skills'] = st.slider(
            "Technical skills",
            0, 100, st.session_state.weights['technical_skills'],
            help="Importance of technical skills and tools mastered"
        )
        
        st.session_state.weights['experience'] = st.slider(
            "Professional experience",
            0, 100, st.session_state.weights['experience'],
            help="Importance of experience and completed projects"
        )
        
        st.session_state.weights['education'] = st.slider(
            "Education",
            0, 100, st.session_state.weights['education'],
            help="Importance of education level and certifications"
        )
        
        st.session_state.weights['soft_skills'] = st.slider(
            "Soft skills",
            0, 100, st.session_state.weights['soft_skills'],
            help="Importance of interpersonal skills"
        )
        
        # Calcul et affichage du total
        total = sum(st.session_state.weights.values())
        if total != 100:
            st.warning(f"⚠️ Total weights must equal 100% (currently {total}%)")
        else:
            st.success("✅ Valid weighting (total = 100%)")

def render_sidebar():
    """Affiche la sidebar complète"""
    with st.sidebar:
        # Logo et titre
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("Logos/MEF2.png", width=50)
        with col2:
            st.markdown(f"### {t('app.title')}")
        
        st.markdown("---")
        
        # Profil utilisateur
        render_user_profile()
        
        st.markdown("---")
        
        # Navigation
        st.subheader("📍 Navigation")
        
        # Onglets de navigation
        tabs = {
            "📄 CV Analysis": "analyse_cv",
            "📊 Dashboard": "dashboard",
            "🔍 Comparison": "comparaison",
            "📁 Processed CVs": "cvs_traites",
            "⚙️ Settings": "configuration"
        }
        
        for label, value in tabs.items():
            if st.button(label, key=f"nav_{value}", use_container_width=True):
                st.session_state.current_tab = value
                st.rerun()
        
        st.markdown("---")
        
        # Guide d'utilisation
        render_usage_guide()
        
        # Pondération des critères
        render_criteria_weights()
        
        st.markdown("---")
        
        # Bouton de déconnexion
        if st.button("🚪 Log out", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def get_current_tab():
    """Retourne l'onglet actuel"""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 'analyse_cv'
    return st.session_state.current_tab