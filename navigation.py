import streamlit as st
from i18n import t

def render_navigation():
    # CSS pour la barre de navigation
    st.markdown("""
    <style>
        /* Style de la barre de navigation */
        .navigation-container {
            background-color: white;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            height: 60px;
        }
        
        /* Style des liens de navigation */
        .nav-link {
            padding: 0.5rem 1rem;
            text-decoration: none;
            color: #333;
            border-radius: 5px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }
        
        .nav-link:hover {
            background-color: #f0f2f6;
        }
        
        .nav-link.active {
            background-color: #e6e9ef;
            color: #1e3a8a;
            font-weight: 600;
        }
        
        /* Style des icônes */
        .nav-icon {
            width: 20px;
            height: 20px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # Barre de navigation
    st.markdown("""
    <div class="navigation-container">
        <a href="#" class="nav-link active">
            <span class="nav-icon">📊</span>
            Dashboard
        </a>
        <a href="#" class="nav-link">
            <span class="nav-icon">🔍</span>
            Comparison
        </a>
        <a href="#" class="nav-link">
            <span class="nav-icon">📄</span>
            Processed CVs
        </a>
        <a href="#" class="nav-link">
            <span class="nav-icon">⚙️</span>
            Settings
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        # Logo et titre
        st.image("Logos/TalentScope.png", width=150)
        st.title(t("app.title"))
        
        st.markdown("---")
        
        # Menu de navigation
        st.markdown("### Menu")
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()
            
        if st.button("🔍 Comparison", use_container_width=True):
            st.session_state['current_page'] = 'comparison'
            st.rerun()
            
        if st.button("📄 Processed CVs", use_container_width=True):
            st.session_state['current_page'] = 'processed_cvs'
            st.rerun()
            
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state['current_page'] = 'config'
            st.rerun()
            
        st.markdown("---")
        
        # Profil utilisateur
        st.markdown("### Profile")
        if 'user_email' in st.session_state:
            st.markdown(f"👤 {st.session_state['user_email']}")
            if st.button("🚪 Log out", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()



