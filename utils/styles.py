"""
Utilitaire pour charger les styles CSS
"""
import os
import streamlit as st

def load_css_file(css_file_path):
    """Charge un fichier CSS et l'applique à l'interface"""
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_main_styles():
    """Charge les styles de l'interface principale"""
    css_file = os.path.join(".streamlit", "main_styles.css")
    load_css_file(css_file)

def load_auth_styles():
    """Charge les styles de l'interface d'authentification"""
    css_file = os.path.join(".streamlit", "styles.css")
    load_css_file(css_file)











