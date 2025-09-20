#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 TALENTSCOPE - SERVEUR OPTIMISÉ COMPLET
Application complète avec tous les modules intégrés
"""

import http.server
import socketserver
import os
import urllib.parse
import json
import subprocess
import threading
import time
from datetime import datetime
import sys

# Configuration
PORT = 8094  # Port optimisé
ML_API_PORT = 8095  # Port pour l'API ML

class OptimizedTalentScopeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = parsed_path.query
        
        print(f"🌐 Requête: {path}")
        
        # Routes principales optimisées
        if path == '/' or path == '/auth' or path == '/login':
            self.serve_html_file('auth_interface.html')
        elif path == '/dashboard' or path == '/home':
            self.serve_html_file('modern_dashboard.html')
        elif path == '/analysis':
            if 'step=verification' in query:
                self.serve_html_file('analysis_interface_verification_optimized.html')
            else:
                self.serve_html_file('analysis_interface_ml_integrated.html')
        elif path == '/profile':
            self.serve_html_file('profile_management.html')
        elif path == '/config':
            self.serve_html_file('modern_dashboard.html')
        elif path == '/users' or path == '/user-management':
            self.serve_html_file('user_management.html')
        elif path == '/diagnostic':
            self.serve_html_file('diagnostic_complet.html')
        elif path == '/test':
            self.serve_html_file('test_user_data.html')
        elif path == '/migrate':
            self.serve_html_file('migrate_accounts.html')
        else:
            # Servir les fichiers statiques
            self.serve_static_file(path)
    
    def do_POST(self):
        """Gestion des requêtes POST pour l'API"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            print(f"📨 POST reçu: {data}")
            
            # Rediriger vers l'API ML si nécessaire
            if self.path.startswith('/api/'):
                self.handle_ml_api_request(data)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "success", "message": "Requête traitée"}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            print(f"❌ Erreur POST: {e}")
            self.send_error(500, f"Erreur serveur: {str(e)}")
    
    def handle_ml_api_request(self, data):
        """Rediriger les requêtes ML vers l'API dédiée"""
        try:
            import requests
            ml_url = f"http://localhost:{ML_API_PORT}/analyze"
            response = requests.post(ml_url, json=data, timeout=30)
            
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            print(f"❌ Erreur API ML: {e}")
            self.send_error(500, f"Erreur API ML: {str(e)}")
    
    def serve_html_file(self, filename):
        """Servir un fichier HTML avec optimisations"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Optimisations automatiques
                content = self.optimize_html_content(content)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
                print(f"✅ HTML servi: {filename}")
            else:
                self.send_error(404, f"Fichier non trouvé: {filename}")
                print(f"❌ Fichier non trouvé: {filename}")
                
        except Exception as e:
            print(f"❌ Erreur serveur HTML: {e}")
            self.send_error(500, f"Erreur serveur: {str(e)}")
    
    def serve_static_file(self, path):
        """Servir les fichiers statiques avec optimisations"""
        try:
            filename = path.lstrip('/')
            
            # Mapper les extensions
            content_types = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon',
                '.json': 'application/json',
                '.pdf': 'application/pdf'
            }
            
            if os.path.exists(filename):
                ext = os.path.splitext(filename)[1].lower()
                content_type = content_types.get(ext, 'application/octet-stream')
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
                
                print(f"📁 Fichier servi: {filename}")
            else:
                self.send_error(404, f"Fichier non trouvé: {filename}")
                print(f"❌ Fichier non trouvé: {filename}")
                
        except Exception as e:
            print(f"❌ Erreur serveur fichier: {e}")
            self.send_error(500, f"Erreur serveur: {str(e)}")
    
    def optimize_html_content(self, content):
        """Optimiser le contenu HTML"""
        # Ajouter des métadonnées d'optimisation
        if '<head>' in content:
            optimization_meta = '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="TalentScope - Application de matching CV">
    <meta name="author" content="Ministère de l'Économie et des Finances">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    '''
            content = content.replace('<head>', f'<head>{optimization_meta}')
        
        return content
    
    def log_message(self, format, *args):
        """Log personnalisé avec timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def start_ml_api():
    """Démarrer l'API ML en arrière-plan"""
    try:
        print("🤖 Démarrage de l'API ML...")
        # Démarrer l'API ML sur un port différent
        ml_process = subprocess.Popen([
            sys.executable, 'talent_scope_ml_api.py',
            '--port', str(ML_API_PORT),
            '--host', '127.0.0.1'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(2)  # Attendre que l'API démarre
        print(f"✅ API ML démarrée sur le port {ML_API_PORT}")
        return ml_process
        
    except Exception as e:
        print(f"❌ Erreur démarrage API ML: {e}")
        return None

def check_dependencies():
    """Vérifier les dépendances"""
    print("🔍 Vérification des dépendances...")
    
    required_files = [
        'auth_interface.html',
        'modern_dashboard.html',
        'profile_management.html',
        'analysis_interface_optimized.html',
        'user_database.js',
        'themes.css',
        'direct-translation.js',
        'talent_scope_ml_api.py'
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

def main():
    """Fonction principale"""
    print("🚀 TALENTSCOPE - SERVEUR OPTIMISÉ COMPLET")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Dépendances manquantes. Arrêt du serveur.")
        return
    
    # Démarrer l'API ML
    ml_process = start_ml_api()
    
    try:
        # Créer le serveur
        with socketserver.TCPServer(("", PORT), OptimizedTalentScopeHandler) as httpd:
            print(f"✅ Serveur principal démarré sur http://localhost:{PORT}")
            print(f"🤖 API ML sur http://localhost:{ML_API_PORT}")
            print("=" * 50)
            print("🎯 Modules disponibles:")
            print("   • 🔐 Authentification: /auth")
            print("   • 📊 Dashboard: /dashboard")
            print("   • 👤 Profil: /profile")
            print("   • 🔍 Analyse: /analysis")
            print("   • ⚙️ Configuration: /config")
            print("   • 👥 Gestion utilisateurs: /users")
            print("   • 🧪 Diagnostic: /diagnostic")
            print("=" * 50)
            print("🔄 Le serveur est en cours d'exécution...")
            print("📝 Appuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            
            # Démarrer le serveur
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
    except OSError as e:
        if e.errno == 10048:  # Port déjà utilisé
            print(f"❌ Port {PORT} déjà utilisé. Essayez un autre port.")
        else:
            print(f"❌ Erreur serveur: {e}")
    finally:
        # Arrêter l'API ML
        if ml_process:
            print("🛑 Arrêt de l'API ML...")
            ml_process.terminate()
            ml_process.wait()

if __name__ == "__main__":
    main()


