#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 TALENTSCOPE - SERVEUR STABLE
Serveur simple et stable avec comptes existants
"""

import http.server
import socketserver
import os
import urllib.parse
import json
from datetime import datetime

PORT = 8096

class StableHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        print(f"🌐 Requête: {path}")
        
        # Routes principales
        if path == '/' or path == '/auth' or path == '/login':
            self.serve_auth_page()
        elif path == '/dashboard' or path == '/home':
            self.serve_file('modern_dashboard.html')
        elif path == '/analysis':
            self.serve_file('analysis_interface_ml_integrated.html')
        elif path == '/profile':
            self.serve_file('profile_management.html')
        elif path == '/config':
            self.serve_file('modern_dashboard.html')
        else:
            # Servir les fichiers statiques
            super().do_GET()
    
    def serve_auth_page(self):
        """Servir la page d'authentification avec comptes existants"""
        try:
            with open('auth_interface.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Injecter le script pour créer les comptes existants
            accounts_script = """
            <script>
            // Créer automatiquement les comptes existants
            document.addEventListener('DOMContentLoaded', function() {
                console.log('🔧 Configuration des comptes existants...');
                
                if (window.userDatabase) {
                    // Vérifier si les comptes existent déjà
                    const users = window.userDatabase.getAllUsers();
                    
                    // Créer le compte akjouj17@gmail.com s'il n'existe pas
                    if (!users['akjouj17@gmail.com']) {
                        window.userDatabase.createUser(
                            'akjouj17@gmail.com',
                            'Hamza12345',
                            'Akjouj Hamza',
                            'Développement',
                            'Développeur Senior',
                            '+212 6 12 34 56 78'
                        );
                        console.log('✅ Compte akjouj17@gmail.com créé');
                    }
                    
                    // Créer le compte elhafsaghazouani@gmail.com s'il n'existe pas
                    if (!users['elhafsaghazouani@gmail.com']) {
                        window.userDatabase.createUser(
                            'elhafsaghazouani@gmail.com',
                            'Hafsa2003',
                            'Hafsa El Ghazouani',
                            'Ressources Humaines',
                            'Analyste RH',
                            '+212 6 87 65 43 21'
                        );
                        console.log('✅ Compte elhafsaghazouani@gmail.com créé');
                    }
                    
                    console.log('🎯 Comptes existants configurés automatiquement');
                    console.log('📋 Comptes disponibles:');
                    console.log('   • akjouj17@gmail.com / Hamza12345');
                    console.log('   • elhafsaghazouani@gmail.com / Hafsa2003');
                } else {
                    console.log('❌ userDatabase non disponible');
                }
            });
            </script>
            """
            
            # Injecter le script avant la fermeture du body
            if '</body>' in content:
                content = content.replace('</body>', accounts_script + '</body>')
            else:
                content += accounts_script
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
            print("✅ Page d'authentification servie avec comptes existants")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            self.send_error(500, f"Erreur: {str(e)}")
    
    def serve_file(self, filename):
        """Servir un fichier HTML"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                
                print(f"✅ {filename} servi")
            else:
                self.send_error(404, f"Fichier non trouvé: {filename}")
                print(f"❌ Fichier non trouvé: {filename}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            self.send_error(500, f"Erreur: {str(e)}")
    
    def log_message(self, format, *args):
        """Log personnalisé"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {format % args}")

def main():
    """Fonction principale"""
    print("🚀 TALENTSCOPE - SERVEUR STABLE")
    print("=" * 50)
    print("🎯 Comptes existants inclus automatiquement:")
    print("   • akjouj17@gmail.com / Hamza12345")
    print("   • elhafsaghazouani@gmail.com / Hafsa2003")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), StableHandler) as httpd:
            print(f"✅ Serveur démarré sur http://localhost:{PORT}")
            print("=" * 50)
            print("🌐 URLs disponibles:")
            print(f"   • Authentification: http://localhost:{PORT}/auth")
            print(f"   • Dashboard: http://localhost:{PORT}/dashboard")
            print(f"   • Analyse: http://localhost:{PORT}/analysis")
            print(f"   • Profil: http://localhost:{PORT}/profile")
            print("=" * 50)
            print("🔄 Le serveur est en cours d'exécution...")
            print("📝 Appuyez sur Ctrl+C pour arrêter")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
    except OSError as e:
        if e.errno == 10048:
            print(f"❌ Port {PORT} déjà utilisé.")
        else:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()


