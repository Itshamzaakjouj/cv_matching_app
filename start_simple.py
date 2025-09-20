#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

class TalentScopeHandler(SimpleHTTPRequestHandler):
    """Handler personnalisé pour TalentScope"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Ajouter les en-têtes CORS et de cache
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        """Gérer les requêtes GET avec redirections personnalisées"""
        if self.path == '/':
            self.path = '/auth_interface.html'
        elif self.path == '/dashboard':
            self.path = '/modern_dashboard.html'
        elif self.path == '/analysis':
            self.path = '/analysis_interface.html'
        
        return super().do_GET()
    
    def log_message(self, format, *args):
        """Personnaliser les logs du serveur"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def check_port(port):
    """Vérifier si un port est disponible"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

def find_available_port(start_port=8080, max_attempts=10):
    """Trouver un port disponible"""
    for port in range(start_port, start_port + max_attempts):
        if check_port(port):
            return port
    return None

def start_server():
    """Démarrer le serveur HTTP"""
    print("🏛️ TALENTSCOPE - LANCEMENT SIMPLE")
    print("=" * 50)
    print("🔐 Interface d'authentification")
    print("🎨 Dashboard moderne")
    print("🚀 Interface d'analyse")
    print("=" * 50)
    
    # Trouver un port disponible
    port = find_available_port()
    if port is None:
        print("❌ Aucun port disponible trouvé")
        return False
    
    try:
        # Créer et démarrer le serveur
        server_address = ('localhost', port)
        httpd = HTTPServer(server_address, TalentScopeHandler)
        
        print(f"✅ Serveur démarré sur http://localhost:{port}")
        print(f"🌐 Interface d'authentification: http://localhost:{port}/auth_interface.html")
        print(f"📊 Dashboard: http://localhost:{port}/modern_dashboard.html")
        print(f"🔍 Analyse: http://localhost:{port}/analysis_interface.html")
        print("\n🔄 Le serveur est en cours d'exécution...")
        print("📝 Appuyez sur Ctrl+C pour arrêter")
        
        # Ouvrir automatiquement le navigateur
        try:
            import webbrowser
            time.sleep(1)
            webbrowser.open(f"http://localhost:{port}/auth_interface.html")
        except Exception as e:
            print(f"⚠️ Impossible d'ouvrir le navigateur automatiquement: {e}")
        
        # Démarrer le serveur
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du serveur demandé par l'utilisateur")
        httpd.shutdown()
        return True
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return False

def main():
    """Fonction principale"""
    try:
        # Vérifier que nous sommes dans le bon répertoire
        required_files = ['auth_interface.html', 'modern_dashboard.html', 'analysis_interface.html']
        missing_files = [f for f in required_files if not os.path.exists(f)]
        
        if missing_files:
            print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
            print("📁 Assurez-vous d'être dans le répertoire correct")
            return False
        
        # Démarrer le serveur
        return start_server()
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)

