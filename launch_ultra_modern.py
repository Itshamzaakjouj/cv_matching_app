"""
Lanceur ultra-moderne pour TalentScope
Intègre Streamlit avec une interface d'analyse HTML/CSS/JS ultra-optimisée
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def print_banner():
    """Affiche la bannière de l'application ultra-moderne"""
    print("=" * 70)
    print("🏛️  TALENTSCOPE - VERSION ULTRA-MODERNE")
    print("=" * 70)
    print("🚀 Interface d'analyse HTML/CSS/JS ultra-optimisée")
    print("⚡ Performance maximale avec technologies modernes")
    print("🎨 Design responsive et animations fluides")
    print("=" * 70)

def start_auth_server():
    """Démarre le serveur d'authentification"""
    print("🔐 Démarrage du serveur d'authentification...")
    try:
        import http.server
        import socketserver
        import os
        
        os.chdir(Path(__file__).parent)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 8080), handler) as httpd:
            print("✅ Serveur d'authentification démarré sur http://localhost:8080")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Erreur serveur d'authentification: {e}")

def start_modern_analysis_server():
    """Démarre le serveur d'analyse moderne"""
    print("🚀 Démarrage du serveur d'analyse moderne...")
    try:
        subprocess.run([sys.executable, "modern_analysis_server.py"], check=True)
    except Exception as e:
        print(f"❌ Erreur serveur d'analyse moderne: {e}")

def start_streamlit_app():
    """Démarre l'application Streamlit"""
    print("🏛️ Démarrage de l'application Streamlit...")
    try:
        # Configuration optimisée pour Streamlit
        env = os.environ.copy()
        env['STREAMLIT_SERVER_HEADLESS'] = 'true'
        env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'launch_ultra_simple.py',
            '--server.port', '8501',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ], env=env)
    except Exception as e:
        print(f"❌ Erreur application Streamlit: {e}")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier les dépendances
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ Dépendances vérifiées")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez les dépendances avec: pip install -r requirements.txt")
        return
    
    # Démarrer les serveurs
    print("\n🚀 Démarrage des serveurs...")
    
    # Thread pour le serveur d'authentification
    auth_thread = threading.Thread(target=start_auth_server, daemon=True)
    auth_thread.start()
    
    # Attendre que le serveur d'auth démarre
    time.sleep(2)
    
    # Thread pour le serveur d'analyse moderne
    analysis_thread = threading.Thread(target=start_modern_analysis_server, daemon=True)
    analysis_thread.start()
    
    # Attendre que le serveur d'analyse démarre
    time.sleep(2)
    
    # Thread pour l'application Streamlit
    streamlit_thread = threading.Thread(target=start_streamlit_app, daemon=True)
    streamlit_thread.start()
    
    # Attendre que Streamlit démarre
    time.sleep(5)
    
    print("\n✅ Application ultra-moderne démarrée avec succès!")
    print("🌐 Interfaces disponibles:")
    print("   🔐 Authentification: http://localhost:8080/auth_interface.html")
    print("   🏛️  Application: http://localhost:8501")
    print("   🚀 Analyse Moderne: http://localhost:9000")
    print("\n📱 Ouverture automatique de l'interface d'authentification...")
    
    # Ouvrir l'interface d'authentification
    try:
        webbrowser.open('http://localhost:8080/auth_interface.html')
    except:
        print("⚠️  Impossible d'ouvrir automatiquement le navigateur")
        print("   Veuillez ouvrir manuellement: http://localhost:8080/auth_interface.html")
    
    print("\n" + "=" * 70)
    print("✨ Interface d'analyse moderne ultra-optimisée disponible !")
    print("💡 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 70)
    
    try:
        # Attendre indéfiniment
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        print("✅ Application arrêtée proprement")

if __name__ == "__main__":
    main()
