#!/usr/bin/env python3
"""
Lanceur pour la page d'authentification TalentScope
"""

import subprocess
import sys
import time
import webbrowser
import os
import threading

def start_server():
    """Démarre le serveur en arrière-plan"""
    try:
        # Changer vers le répertoire du script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)
        
        # Lancer le serveur
        process = subprocess.Popen([sys.executable, "simple_server.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return None

def open_browser():
    """Ouvre le navigateur après un délai"""
    time.sleep(3)  # Attendre que le serveur démarre
    try:
        # Ouvrir directement le fichier d'authentification
        webbrowser.open('http://localhost:8080/auth_interface.html')
        print("🌐 Page d'authentification ouverte dans le navigateur")
    except Exception as e:
        print(f"⚠️ Impossible d'ouvrir le navigateur: {e}")

def main():
    print("=" * 70)
    print("🏛️  TALENTSCOPE - PAGE D'AUTHENTIFICATION")
    print("=" * 70)
    print("🚀 Démarrage du serveur...")
    print("=" * 70)
    
    # Démarrer le serveur
    server_process = start_server()
    if not server_process:
        print("❌ Impossible de démarrer l'application")
        return
    
    # Démarrer l'ouverture du navigateur en arrière-plan
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("✅ Serveur démarré avec succès !")
    print("\n🌐 Page d'authentification:")
    print("   🔐 URL: http://localhost:8080/auth_interface.html")
    print("\n🔑 Identifiants de test:")
    print("   👨‍💼 Admin: akjouj17@gmail.com / Hamza12345")
    print("   👩‍💼 User: elhafsaghazouani@gmail.com / Hafsa2003")
    print("\n" + "=" * 70)
    print("✨ Page d'authentification disponible !")
    print("💡 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 70)
    
    try:
        # Attendre que le processus se termine
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        server_process.terminate()
        server_process.wait()
        print("✅ Application arrêtée proprement")

if __name__ == "__main__":
    main()
