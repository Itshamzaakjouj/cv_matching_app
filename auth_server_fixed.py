#!/usr/bin/env python3
"""
Serveur d'authentification pour TalentScope
Sert l'interface d'authentification HTML et redirige vers le dashboard moderne après connexion
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import subprocess
import os
import json
from urllib.parse import urlparse, parse_qs

# Configuration
VALID_CREDENTIALS = {
    "akjouj17@gmail.com": "Hamza12345",
    "elhafsaghazouani@gmail.com": "Hafsa2003"
}

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/auth':
            # Servir la page d'authentification
            self.path = '/auth_interface.html'
            return super().do_GET()
        
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            email = data.get('email')
            password = data.get('password')
            
            # Vérifier les identifiants
            if email in VALID_CREDENTIALS and VALID_CREDENTIALS[email] == password:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': True,
                    'message': 'Connexion réussie',
                    'redirect': 'http://localhost:8087/dashboard'
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': False,
                    'message': 'Email ou mot de passe incorrect'
                }
                self.wfile.write(json.dumps(response).encode())
            return
        
        return super().do_POST()

def start_dashboard_server():
    """Démarre le serveur du dashboard en arrière-plan"""
    try:
        time.sleep(2)
        subprocess.Popen(['python', 'final_multi_user_server.py'], 
                        cwd=os.getcwd(),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        print("✅ Serveur dashboard démarré")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur dashboard: {e}")

def main():
    PORT = 8080
    
    # Démarrer le serveur du dashboard en arrière-plan
    dashboard_thread = threading.Thread(target=start_dashboard_server, daemon=True)
    dashboard_thread.start()
    
    # Démarrer le serveur d'authentification
    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        print(f"🚀 Serveur d'authentification démarré sur http://localhost:{PORT}")
        print(f"📱 Interface d'authentification: http://localhost:{PORT}/auth")
        print(f"📊 Dashboard: http://localhost:8087/dashboard")
        print("=" * 60)
        print("✨ Interface d'authentification moderne disponible !")
        print("=" * 60)
        
        # Ouvrir automatiquement le navigateur
        webbrowser.open(f'http://localhost:{PORT}/auth')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt des serveurs...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
