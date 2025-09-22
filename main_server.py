#!/usr/bin/env python3
"""
TalentScope - Serveur Principal Intégré
Ministère de l'Économie et des Finances
"""

import asyncio
import threading
import time
import webbrowser
import os
import sys
from pathlib import Path
import subprocess
import signal

class TalentScopeServer:
    def __init__(self):
        self.api_process = None
        self.http_process = None
        self.running = False
        
    def start_api_server(self):
        """Démarre le serveur API FastAPI"""
        print("🚀 Démarrage du serveur API...")
        try:
            self.api_process = subprocess.Popen([
                sys.executable, "api_server.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Serveur API démarré sur http://localhost:8000")
        except Exception as e:
            print(f"❌ Erreur serveur API: {e}")
    
    def start_http_server(self):
        """Démarre le serveur HTTP pour les fichiers statiques"""
        print("🌐 Démarrage du serveur HTTP...")
        try:
            import http.server
            import socketserver
            
            class ModernHandler(http.server.SimpleHTTPRequestHandler):
                def do_GET(self):
                    # Routes principales
                    routes = {
                        '/': 'auth_interface_modern.html',
                        '/auth': 'auth_interface_modern.html',
                        '/dashboard': 'modern_dashboard.html',
                        '/analysis': 'analysis_interface.html',
                        '/analysis/step1': 'analysis_interface.html',
                        '/analysis/step2': 'analysis_interface_optimized.html',
                        '/analysis/step3': 'analysis_interface_verification_optimized.html',
                        '/analysis/step4': 'analysis_interface.html',
                        '/profile': 'profile_management.html',
                        '/settings': 'settings.html',
                        '/processed': 'treated_cvs.html'
                    }
                    
                    if self.path in routes:
                        self.path = routes[self.path]
                    
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)
                
                def do_POST(self):
                    # Rediriger les requêtes API vers le serveur FastAPI
                    if self.path.startswith('/api/'):
                        # Pour la démo, on simule les réponses
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        
                        if self.path == '/api/auth/login':
                            response = {
                                'success': True,
                                'user': {
                                    'id': 1,
                                    'name': 'Akjouj Hamza',
                                    'email': 'akjouj17@gmail.com',
                                    'role': 'admin'
                                }
                            }
                        else:
                            response = {'success': True, 'message': 'OK'}
                        
                        self.wfile.write(str(response).replace("'", '"').encode())
                    else:
                        self.send_error(404, "Route non trouvée")
            
            with socketserver.TCPServer(("", 8080), ModernHandler) as httpd:
                print("✅ Serveur HTTP démarré sur http://localhost:8080")
                self.http_process = httpd
                httpd.serve_forever()
                
        except Exception as e:
            print(f"❌ Erreur serveur HTTP: {e}")
    
    def start(self):
        """Démarre tous les serveurs"""
        print("=" * 70)
        print("🏛️  TALENTSCOPE - APPLICATION MODERNE INTÉGRÉE")
        print("=" * 70)
        print("🚀 Interface d'authentification moderne avec animations")
        print("⚡ Base de données SQLite intégrée")
        print("🎨 Design responsive et animations fluides")
        print("=" * 70)
        
        # Vérifier les dépendances
        try:
            import fastapi
            import uvicorn
            import sqlite3
            print("✅ Dépendances vérifiées")
        except ImportError as e:
            print(f"❌ Dépendance manquante: {e}")
            print("💡 Installez les dépendances avec: pip install fastapi uvicorn")
            return
        
        self.running = True
        
        # Démarrer le serveur API en arrière-plan
        api_thread = threading.Thread(target=self.start_api_server, daemon=True)
        api_thread.start()
        
        # Attendre que l'API démarre
        time.sleep(3)
        
        # Démarrer le serveur HTTP
        http_thread = threading.Thread(target=self.start_http_server, daemon=True)
        http_thread.start()
        
        # Attendre que le serveur HTTP démarre
        time.sleep(2)
        
        print("\n✅ Application TalentScope démarrée avec succès!")
        print("🌐 Interfaces disponibles:")
        print("   🔐 Authentification: http://localhost:8080/auth")
        print("   🏛️  Dashboard: http://localhost:8080/dashboard")
        print("   🔍 Analyse: http://localhost:8080/analysis")
        print("   👤 Profil: http://localhost:8080/profile")
        print("   ⚙️  Paramètres: http://localhost:8080/settings")
        print("\n📱 Ouverture automatique de l'interface d'authentification...")
        
        # Ouvrir l'interface d'authentification
        try:
            webbrowser.open('http://localhost:8080/auth')
        except:
            print("⚠️  Impossible d'ouvrir automatiquement le navigateur")
            print("   Veuillez ouvrir manuellement: http://localhost:8080/auth")
        
        print("\n" + "=" * 70)
        print("✨ Application moderne avec base de données disponible !")
        print("💡 Utilisez Ctrl+C pour arrêter l'application")
        print("=" * 70)
        
        try:
            # Attendre indéfiniment
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Arrête tous les serveurs"""
        print("\n🛑 Arrêt de l'application...")
        self.running = False
        
        if self.api_process:
            self.api_process.terminate()
            self.api_process.wait()
            print("✅ Serveur API arrêté")
        
        if self.http_process:
            self.http_process.shutdown()
            print("✅ Serveur HTTP arrêté")
        
        print("✅ Application arrêtée proprement")

def main():
    """Fonction principale"""
    server = TalentScopeServer()
    
    # Gestion des signaux pour un arrêt propre
    def signal_handler(signum, frame):
        server.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    server.start()

if __name__ == "__main__":
    main()
