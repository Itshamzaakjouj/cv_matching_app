#!/usr/bin/env python3
"""
TalentScope - Serveur Simple et Fonctionnel
Ministère de l'Économie et des Finances
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time
from pathlib import Path

class TalentScopeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parser l'URL
        path = self.path.split('?')[0]  # Enlever les paramètres de requête
        
        # Routes principales
        routes = {
            '/': 'auth_interface.html',
            '/auth': 'auth_interface.html',
            '/acceuil': 'auth_interface.html',  # Route manquante
            '/home': 'auth_interface.html',     # Alias
            '/dashboard': 'modern_dashboard.html',
            '/analysis': 'analysis_interface.html',
            '/analysis/step1': 'analysis_interface.html',
            '/analysis/step2': 'analysis_interface.html', 
            '/analysis/step3': 'analysis_interface.html',
            '/analysis/step4': 'analysis_interface.html',
            '/profile': 'profile_management.html',
            '/settings': 'settings.html',
            '/processed': 'treated_cvs.html',
            '/ministry': 'ministry_page.html',  # Page du ministère
            '/config': 'modern_dashboard.html'  # Configuration via dashboard
        }
        
        # Si c'est une route connue, servir le fichier correspondant
        if path in routes:
            self.path = routes[path]
            print(f"🌐 Route: {path} -> {routes[path]}")
        else:
            # Vérifier si c'est un fichier existant
            if os.path.exists(path[1:]) and not path.startswith('/api/'):
                print(f"🌐 Fichier direct: {path}")
            else:
                # Rediriger vers la page d'accueil pour les routes inconnues
                print(f"❌ Route inconnue: {path} -> Redirection vers /auth")
                self.send_response(302)
                self.send_header('Location', '/auth')
                self.end_headers()
                return
        
        # Servir le fichier
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        # Simuler les réponses API pour la démo
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if self.path == '/api/auth/login':
                # Lire les données POST
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                # Parser les données (format: email=...&password=...)
                data = {}
                for pair in post_data.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        data[key] = value
                
                email = data.get('email', '')
                password = data.get('password', '')
                
                # Vérifier les identifiants
                if email == 'akjouj17@gmail.com' and password == 'Hamza12345':
                    response = {
                        'success': True,
                        'user': {
                            'id': 1,
                            'name': 'Akjouj Hamza',
                            'email': 'akjouj17@gmail.com',
                            'role': 'admin'
                        }
                    }
                elif email == 'elhafsaghazouani@gmail.com' and password == 'Hafsa2003':
                    response = {
                        'success': True,
                        'user': {
                            'id': 2,
                            'name': 'Hafsa El Ghazouani',
                            'email': 'elhafsaghazouani@gmail.com',
                            'role': 'user'
                        }
                    }
                else:
                    response = {
                        'success': False,
                        'detail': 'Identifiants incorrects'
                    }
            elif self.path == '/api/auth/register':
                response = {
                    'success': True,
                    'message': 'Compte créé avec succès'
                }
            else:
                response = {'success': True, 'message': 'OK'}
            
            import json
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, "Route non trouvée")

def start_server():
    """Démarre le serveur"""
    PORT = 8080
    
    print("=" * 70)
    print("🏛️  TALENTSCOPE - SERVEUR SIMPLE")
    print("=" * 70)
    print("🚀 Interface d'authentification moderne")
    print("🔍 Pages d'analyse complètes (5 étapes)")
    print("🎨 Design responsive et animations fluides")
    print("=" * 70)
    
    # Vérifier que les fichiers existent
    required_files = [
        'auth_interface.html',
        'modern_dashboard.html', 
        'analysis_interface.html',
        'profile_management.html',
        'settings.html',
        'treated_cvs.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return
    
    print("✅ Tous les fichiers requis sont présents")
    
    try:
        with socketserver.TCPServer(("", PORT), TalentScopeHandler) as httpd:
            print(f"✅ Serveur démarré sur http://localhost:{PORT}")
            print("\n🌐 Interfaces disponibles:")
            print("   🔐 Authentification: http://localhost:8080/auth")
            print("   🏛️  Dashboard: http://localhost:8080/dashboard")
            print("   🔍 Analyse (Étape 1): http://localhost:8080/analysis")
            print("   📁 CVs Traités: http://localhost:8080/processed")
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
            print("✨ Application TalentScope disponible !")
            print("💡 Utilisez Ctrl+C pour arrêter l'application")
            print("=" * 70)
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 10048:  # Port déjà utilisé
            print(f"❌ Le port {PORT} est déjà utilisé")
            print("💡 Arrêtez les autres serveurs ou changez le port")
        else:
            print(f"❌ Erreur serveur: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        print("✅ Serveur arrêté proprement")

if __name__ == "__main__":
    start_server()
