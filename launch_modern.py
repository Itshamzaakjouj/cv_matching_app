#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - LANCEUR APPLICATION MODERNE
Ministère de l'Économie et des Finances
Version: 2.0 Ultra-Moderne
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Vérifier les dépendances Python"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'jinja2',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installation des packages manquants: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'requirements_modern.txt'
            ])
            print("✅ Dépendances installées avec succès!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False
    
    return True

def create_directories():
    """Créer les dossiers nécessaires"""
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

def start_application():
    """Démarrer l'application FastAPI"""
    print("\n🚀 Démarrage de l'application moderne...")
    print("=" * 60)
    print("🏛️  TALENTSCOPE - MINISTÈRE DE L'ÉCONOMIE ET DES FINANCES")
    print("=" * 60)
    print("⚡ Technologies: FastAPI + HTML5 + CSS3 + JavaScript ES6")
    print("🎨 Interface moderne et ultra-performante")
    print("=" * 60)
    
    try:
        # Démarrer l'application FastAPI
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'modern_app:app',
            '--host', '0.0.0.0',
            '--port', '3000',
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

def main():
    """Fonction principale"""
    print("🏛️ TALENTSCOPE - APPLICATION MODERNE ULTRA-PERFORMANTE")
    print("=" * 60)
    print("🚀 Démarrage en cours...")
    print("=" * 60)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Impossible de continuer sans les dépendances requises")
        return
    
    # Créer les dossiers
    create_directories()
    
    # Attendre un peu
    print("\n⏳ Préparation de l'application...")
    time.sleep(2)
    
    # Ouvrir le navigateur
    print("🌐 Ouverture du navigateur...")
    time.sleep(1)
    webbrowser.open('http://localhost:3000')
    
    # Démarrer l'application
    start_application()

if __name__ == "__main__":
    main()
