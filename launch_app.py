#!/usr/bin/env python3
"""
Script de lancement pour TalentScope
Démarre le serveur d'authentification HTML et l'application Streamlit
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path

def start_streamlit():
    """Démarre l'application Streamlit"""
    try:
        print("🚀 Démarrage de l'application Streamlit...")
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'launch_ultra_simple.py',
            '--server.port', '8501', '--server.headless', 'true'
        ], cwd=os.getcwd())
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de Streamlit: {e}")

def start_auth_server():
    """Démarre le serveur d'authentification HTML"""
    try:
        print("🔐 Démarrage du serveur d'authentification...")
        subprocess.run([
            sys.executable, '-m', 'http.server', '8080'
        ], cwd=os.getcwd())
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur d'auth: {e}")

def main():
    print("=" * 60)
    print("🏛️  TALENTSCOPE - MINISTÈRE DE L'ÉCONOMIE ET DES FINANCES")
    print("=" * 60)
    print("🚀 Démarrage de l'application...")
    print()
    
    # Vérifier que les fichiers existent
    if not Path("auth_interface.html").exists():
        print("❌ Fichier auth_interface.html introuvable!")
        return
    
    if not Path("launch_ultra_simple.py").exists():
        print("❌ Fichier launch_ultra_simple.py introuvable!")
        return
    
    # Démarrer Streamlit en arrière-plan
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Attendre un peu pour que Streamlit démarre
    time.sleep(3)
    
    # Démarrer le serveur d'authentification
    auth_thread = threading.Thread(target=start_auth_server, daemon=True)
    auth_thread.start()
    
    # Attendre un peu pour que le serveur d'auth démarre
    time.sleep(2)
    
    print("✅ Application démarrée avec succès!")
    print()
    print("🌐 Interfaces disponibles:")
    print("   🔐 Authentification: http://localhost:8080/auth_interface.html")
    print("   🏛️  Application: http://localhost:8501")
    print()
    print("📱 Ouverture automatique de l'interface d'authentification...")
    
    # Ouvrir l'interface d'authentification
    webbrowser.open('http://localhost:8080/auth_interface.html')
    
    print()
    print("=" * 60)
    print("✨ Interface d'authentification moderne disponible !")
    print("=" * 60)
    print("💡 Utilisez Ctrl+C pour arrêter l'application")
    print()
    
    try:
        # Garder le script en vie
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        print("✅ Application arrêtée avec succès!")

if __name__ == "__main__":
    main()

