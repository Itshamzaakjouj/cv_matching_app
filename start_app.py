
#!/usr/bin/env python3
"""
Script de démarrage pour l'application TalentScope FastAPI + React
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("=" * 60)
    print("🏛️  TALENTSCOPE - MINISTÈRE DE L'ÉCONOMIE ET DES FINANCES")
    print("=" * 60)
    print("🚀 Démarrage de l'application moderne FastAPI + React...")
    print()

def check_requirements():
    """Vérifier que les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    # Vérifier Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js non installé")
            return False
        print(f"✅ Node.js {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js non trouvé")
        return False
    
    # Vérifier npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ npm non installé")
            return False
        print(f"✅ npm {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npm non trouvé")
        return False
    
    return True

def install_backend_dependencies():
    """Installer les dépendances Python"""
    print("📦 Installation des dépendances backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True)
        print("✅ Dépendances backend installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation backend: {e}")
        return False

def install_frontend_dependencies():
    """Installer les dépendances React"""
    print("📦 Installation des dépendances frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Dossier frontend non trouvé")
        return False
    
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Dépendances frontend installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur installation frontend: {e}")
        return False

def build_frontend():
    """Compiler l'application React"""
    print("🔨 Compilation de l'application React...")
    
    frontend_dir = Path("frontend")
    try:
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
        print("✅ Application React compilée")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur compilation React: {e}")
        return False

def start_backend():
    """Démarrer le serveur FastAPI"""
    print("🚀 Démarrage du serveur FastAPI...")
    
    backend_dir = Path("backend")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd=backend_dir)
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        print("✅ Serveur FastAPI démarré sur http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Erreur démarrage FastAPI: {e}")
        return None

def start_frontend():
    """Démarrer le serveur de développement React"""
    print("🚀 Démarrage du serveur React...")
    
    frontend_dir = Path("frontend")
    try:
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir)
        
        # Attendre que le serveur démarre
        time.sleep(5)
        
        print("✅ Serveur React démarré sur http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Erreur démarrage React: {e}")
        return None

def open_browser():
    """Ouvrir le navigateur"""
    print("🌐 Ouverture du navigateur...")
    time.sleep(2)
    webbrowser.open("http://localhost:3000")
    print("✅ Application ouverte dans le navigateur")

def main():
    print_banner()
    
    # Vérifier les prérequis
    if not check_requirements():
        print("❌ Prérequis manquants. Veuillez installer Node.js et Python 3.8+")
        return
    
    # Installer les dépendances
    if not install_backend_dependencies():
        return
    
    if not install_frontend_dependencies():
        return
    
    # Compiler le frontend
    if not build_frontend():
        return
    
    # Démarrer les serveurs
    backend_process = start_backend()
    if not backend_process:
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print()
    print("=" * 60)
    print("✅ APPLICATION DÉMARRÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("🌐 Interfaces disponibles:")
    print("   🏛️  Application: http://localhost:3000")
    print("   🔧 API Backend: http://localhost:8000")
    print("   📚 Documentation API: http://localhost:8000/docs")
    print("=" * 60)
    print("💡 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 60)
    
    # Ouvrir le navigateur
    open_browser()
    
    try:
        # Attendre que l'utilisateur arrête l'application
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        
        # Arrêter les processus
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ Application arrêtée")

if __name__ == "__main__":
    main()

