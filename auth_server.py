
#!/usr/bin/env python3
"""
Serveur d'authentification pour TalentScope
Sert l'interface d'authentification HTML et redirige vers Streamlit après connexion
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

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/auth':
            # Servir la page d'authentification
            self.path = '/auth_interface.html'
        elif self.path == '/login':
            # Traitement de la connexion
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': 'Connexion réussie',
                'redirect': 'http://localhost:8501'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        elif self.path == '/register':
            # Traitement de l'inscription
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': 'Compte créé avec succès',
                'redirect': 'http://localhost:8501'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/login' or self.path == '/register':
            # Traitement des données de formulaire
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': 'Opération réussie',
                'redirect': 'http://localhost:8501'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        return super().do_POST()

def start_streamlit():
    """Démarre l'application Streamlit en arrière-plan"""
    try:
        # Attendre un peu pour que le serveur d'auth démarre
        time.sleep(2)
        
        # Démarrer Streamlit
        subprocess.run([
            'python', '-m', 'streamlit', 'run', 'launch_ultra_simple.py',
            '--server.port', '8501', '--server.headless', 'true'
        ], cwd=os.getcwd())
    except Exception as e:
        print(f"Erreur lors du démarrage de Streamlit: {e}")

def main():
    PORT = 8080
    
    # Démarrer Streamlit en arrière-plan
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Démarrer le serveur d'authentification
    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        print(f"🚀 Serveur d'authentification démarré sur http://localhost:{PORT}")
        print(f"📱 Interface d'authentification: http://localhost:{PORT}")
        print(f"🔧 Application Streamlit: http://localhost:8501")
        print("=" * 60)
        print("✨ Interface d'authentification moderne disponible !")
        print("=" * 60)
        
        # Ouvrir automatiquement le navigateur
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur d'authentification...")
            httpd.shutdown()

if __name__ == "__main__":
    main()

