import streamlit as st
import json
import os
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="TalentScope",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des variables de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Configuration des utilisateurs valides
VALID_USERS = {
    "akjouj17@gmail.com": {
        "password": "Hamza12345",
        "name": "Akjouj Hamza",
        "role": "admin"
    },
    "elhafsaghazouani@gmail.com": {
        "password": "Hafsa2003",
        "name": "Hafsa El Ghazouani",
        "role": "user"
    }
}

def login_page():
    st.title("TalentScope")
    st.markdown("### Ministère de l'Économie et des Finances")
    st.markdown("#### Plateforme de gestion des talents")

    with st.form("login_form"):
        email = st.text_input("Adresse e-mail")
        password = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")

        if submit:
            if email in VALID_USERS and VALID_USERS[email]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = {
                    "name": VALID_USERS[email]["name"],
                    "role": VALID_USERS[email]["role"],
                    "email": email
                }
                st.success("Connexion réussie!")
                st.rerun()
            else:
                st.error("Identifiants incorrects")

def dashboard_page():
    st.sidebar.title(f"Bienvenue, {st.session_state.current_user['name']}")
    
    # Menu de navigation
    menu = st.sidebar.radio(
        "NAVIGATION",
        ["Accueil", "Tableau de Bord", "Nouvelle Analyse", "CVs Traités", "Configuration"]
    )

    if menu == "Accueil":
        st.title("Accueil")
        st.write("Bienvenue sur TalentScope")
        
    elif menu == "Tableau de Bord":
        st.title("Tableau de Bord")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CVs Analysés", "150")
        with col2:
            st.metric("Correspondances", "45")
        with col3:
            st.metric("Taux de réussite", "85%")
            
    elif menu == "Nouvelle Analyse":
        st.title("Nouvelle Analyse")
        st.file_uploader("Déposer un CV", type=["pdf", "docx"])
        
    elif menu == "CVs Traités":
        st.title("Historique des analyses")
        st.write("Liste des CVs traités")
        
    elif menu == "Configuration":
        st.title("Paramètres")
        language = st.selectbox("Langue", ["Français", "English"])
        theme = st.selectbox("Thème", ["Clair", "Sombre"])
        st.checkbox("Notifications par email", value=True)
        st.checkbox("Notifications push", value=True)

    # Bouton de déconnexion dans la sidebar
    if st.sidebar.button("Déconnexion"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
