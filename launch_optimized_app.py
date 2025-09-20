#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 TALENTSCOPE - LANCEUR OPTIMISÉ
Script de lancement pour l'application complète optimisée
"""

import subprocess
import sys
import time
import os
import signal
import threading
from datetime import datetime

class OptimizedAppLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_ml_api(self):
        """Démarrer l'API ML"""
        try:
            print("🤖 Démarrage de l'API ML...")
            process = subprocess.Popen([
                sys.executable, 'optimized_ml_api.py',
                '--host', '127.0.0.1',
                '--port', '8095'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes.append(('ML API', process))
            time.sleep(3)  # Attendre que l'API démarre
            
            # Vérifier si l'API est démarrée
            if process.poll() is None:
                print("✅ API ML démarrée sur http://localhost:8095")
                return True
            else:
                print("❌ Erreur lors du démarrage de l'API ML")
                return False
                
        except Exception as e:
            print(f"❌ Erreur démarrage API ML: {e}")
            return False
    
    def start_main_server(self):
        """Démarrer le serveur principal"""
        try:
            print("🌐 Démarrage du serveur principal...")
            process = subprocess.Popen([
                sys.executable, 'optimized_complete_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes.append(('Serveur Principal', process))
            time.sleep(2)
            
            if process.poll() is None:
                print("✅ Serveur principal démarré sur http://localhost:8094")
                return True
            else:
                print("❌ Erreur lors du démarrage du serveur principal")
                return False
                
        except Exception as e:
            print(f"❌ Erreur démarrage serveur principal: {e}")
            return False
    
    def check_dependencies(self):
        """Vérifier les dépendances"""
        print("🔍 Vérification des dépendances...")
        
        required_files = [
            'optimized_complete_server.py',
            'optimized_ml_api.py',
            'auth_interface.html',
            'modern_dashboard.html',
            'profile_management.html',
            'analysis_interface_optimized.html',
            'user_database.js',
            'themes.css',
            'direct-translation.js'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Fichiers manquants: {missing_files}")
            return False
        
        print("✅ Toutes les dépendances sont présentes")
        return True
    
    def install_dependencies(self):
        """Installer les dépendances Python"""
        print("📦 Installation des dépendances...")
        
        try:
            # Installer les dépendances FastAPI
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'fastapi', 'uvicorn', 'python-multipart', 'requests'
            ], check=True, capture_output=True)
            
            # Installer les dépendances ML
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'scikit-learn', 'nltk', 'pandas', 'numpy'
            ], check=True, capture_output=True)
            
            print("✅ Dépendances installées avec succès")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur installation dépendances: {e}")
            return False
    
    def monitor_processes(self):
        """Surveiller les processus"""
        while self.running:
            for name, process in self.processes:
                if process.poll() is not None:
                    print(f"⚠️ Processus {name} s'est arrêté")
                    self.running = False
                    break
            time.sleep(1)
    
    def cleanup(self):
        """Nettoyer les processus"""
        print("\n🛑 Arrêt des processus...")
        self.running = False
        
        for name, process in self.processes:
            try:
                print(f"🛑 Arrêt de {name}...")
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ Tous les processus ont été arrêtés")
    
    def launch(self):
        """Lancer l'application complète"""
        print("🚀 TALENTSCOPE - LANCEUR OPTIMISÉ")
        print("=" * 50)
        print(f"⏰ Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Vérifier les dépendances
        if not self.check_dependencies():
            print("❌ Dépendances manquantes. Arrêt du lanceur.")
            return False
        
        # Installer les dépendances si nécessaire
        try:
            import fastapi
            import uvicorn
            import sklearn
        except ImportError:
            print("📦 Installation des dépendances manquantes...")
            if not self.install_dependencies():
                print("❌ Impossible d'installer les dépendances. Arrêt du lanceur.")
                return False
        
        # Démarrer l'API ML
        if not self.start_ml_api():
            print("❌ Impossible de démarrer l'API ML. Arrêt du lanceur.")
            return False
        
        # Démarrer le serveur principal
        if not self.start_main_server():
            print("❌ Impossible de démarrer le serveur principal. Arrêt du lanceur.")
            return False
        
        print("=" * 50)
        print("🎯 APPLICATION DÉMARRÉE AVEC SUCCÈS!")
        print("=" * 50)
        print("🌐 Interface principale: http://localhost:8094")
        print("🤖 API ML: http://localhost:8095")
        print("📚 Documentation API: http://localhost:8095/docs")
        print("=" * 50)
        print("📋 Modules disponibles:")
        print("   • 🔐 Authentification: http://localhost:8094/auth")
        print("   • 📊 Dashboard: http://localhost:8094/dashboard")
        print("   • 👤 Profil: http://localhost:8094/profile")
        print("   • 🔍 Analyse: http://localhost:8094/analysis")
        print("   • ⚙️ Configuration: http://localhost:8094/config")
        print("=" * 50)
        print("🔄 L'application est en cours d'exécution...")
        print("📝 Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        # Démarrer la surveillance des processus
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Attendre indéfiniment
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur...")
        finally:
            self.cleanup()
        
        return True

def main():
    """Fonction principale"""
    launcher = OptimizedAppLauncher()
    
    # Gestionnaire de signaux pour un arrêt propre
    def signal_handler(signum, frame):
        print("\n🛑 Signal d'arrêt reçu...")
        launcher.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Lancer l'application
    success = launcher.launch()
    
    if success:
        print("✅ Application arrêtée proprement")
    else:
        print("❌ Erreur lors du lancement de l'application")
        sys.exit(1)

if __name__ == "__main__":
    main()