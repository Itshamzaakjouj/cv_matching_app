"""
Utilitaires pour le chargement et l'affichage du logo MEF
"""
import base64
import os

def load_logo_base64():
    """Charge le logo MEF et le convertit en base64"""
    try:
        logo_path = os.path.join("Logos", "MEF.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as logo_file:
                logo_data = base64.b64encode(logo_file.read()).decode()
                return logo_data
        else:
            # Fallback vers MEF2.png si MEF.png n'existe pas
            logo_path = os.path.join("Logos", "MEF2.png")
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as logo_file:
                    logo_data = base64.b64encode(logo_file.read()).decode()
                    return logo_data
    except Exception as e:
        print(f"Erreur lors du chargement du logo: {e}")
        return None

def get_logo_html(style="width: 100%; height: 100%; object-fit: contain;"):
    """Retourne le HTML du logo MEF ou un fallback"""
    logo_data = load_logo_base64()
    if logo_data:
        return f'<img src="data:image/png;base64,{logo_data}" style="{style}" alt="Logo MEF" />'
    else:
        return '🎯'  # Fallback vers l'ancien logo

