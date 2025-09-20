#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - SERVEUR SIMPLE
Ministère de l'Économie et des Finances
Version: 2.0 Simple et Efficace
"""

import http.server
import socketserver
import webbrowser
import time
import os
from pathlib import Path

class TalentScopeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/simple_app.html'
        return super().do_GET()

def start_server():
    """Démarrer le serveur simple"""
    PORT = 8080
    
    print("🏛️ TALENTSCOPE - APPLICATION SIMPLE ET EFFICACE")
    print("=" * 60)
    print("🚀 Démarrage du serveur...")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), TalentScopeHandler) as httpd:
            print(f"✅ Serveur démarré sur http://localhost:{PORT}")
            print("🌐 Ouverture de l'application...")
            
            # Ouvrir l'application dans le navigateur
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
            
            print("=" * 60)
            print("✨ Application TalentScope disponible !")
            print("💡 Utilisez Ctrl+C pour arrêter l'application")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Le port {PORT} est déjà utilisé")
            print("🔄 Tentative avec le port 8081...")
            start_server_alt()
        else:
            print(f"❌ Erreur: {e}")

def start_server_alt():
    """Démarrer le serveur sur un port alternatif"""
    PORT = 8081
    
    try:
        with socketserver.TCPServer(("", PORT), TalentScopeHandler) as httpd:
            print(f"✅ Serveur démarré sur http://localhost:{PORT}")
            print("🌐 Ouverture de l'application...")
            
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
            
            print("=" * 60)
            print("✨ Application TalentScope disponible !")
            print("💡 Utilisez Ctrl+C pour arrêter l'application")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    start_server()
