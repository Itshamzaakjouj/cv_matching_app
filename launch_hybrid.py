#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - LANCEUR APPLICATION HYBRIDE
Ministère de l'Économie et des Finances
Version: 2.0 Hybride (Auth existante + App moderne)
"""

import subprocess
import sys
import os
import time
import webbrowser
import threading
from pathlib import Path

def start_auth_server():
    """Démarrer le serveur d'authentification existant"""
    print("🔐 Démarrage du serveur d'authentification...")
    try:
        subprocess.run([sys.executable, "auth_server.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur serveur d'authentification: {e}")
    except KeyboardInterrupt:
        print("🛑 Arrêt du serveur d'authentification...")

def start_hybrid_app():
    """Démarrer l'application hybride moderne"""
    print("🚀 Démarrage de l'application hybride moderne...")
    try:
        subprocess.run([sys.executable, "hybrid_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur application hybride: {e}")
    except KeyboardInterrupt:
        print("🛑 Arrêt de l'application hybride...")

def main():
    """Fonction principale"""
    print("🏛️ TALENTSCOPE - APPLICATION HYBRIDE MODERNE")
    print("=" * 60)
    print("🚀 Démarrage en cours...")
    print("🔐 Interface d'authentification existante")
    print("⚡ Application moderne après connexion")
    print("=" * 60)
    
    # Créer les dossiers nécessaires
    print("📁 Création des dossiers...")
    directories = [
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'uploads',
        'data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    # Démarrer le serveur d'authentification dans un thread séparé
    auth_thread = threading.Thread(target=start_auth_server, daemon=True)
    auth_thread.start()
    
    # Attendre un peu pour que le serveur d'auth démarre
    print("⏳ Attente du démarrage du serveur d'authentification...")
    time.sleep(3)
    
    # Ouvrir l'interface d'authentification
    print("🌐 Ouverture de l'interface d'authentification...")
    webbrowser.open('http://localhost:8080/auth_interface.html')
    
    # Attendre un peu avant de démarrer l'application hybride
    time.sleep(2)
    
    # Démarrer l'application hybride
    print("🚀 Démarrage de l'application hybride moderne...")
    print("✅ Application hybride démarrée avec succès!")
    print("🌐 Interfaces disponibles:")
    print("   🔐 Authentification: http://localhost:8080/auth_interface.html")
    print("   🏛️  Application Moderne: http://localhost:3000")
    print("=" * 60)
    print("✨ Interface d'authentification familière + Application moderne !")
    print("💡 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 60)
    
    try:
        start_hybrid_app()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")

if __name__ == "__main__":
    main()
