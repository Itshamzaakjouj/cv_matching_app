#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TalentScope - Serveur Multi-Utilisateurs Final
Serveur HTTP complet avec gestion multi-utilisateurs
"""

import http.server
import socketserver
import os
import urllib.parse
import json
from datetime import datetime

PORT = 8087  # Port final pour éviter les conflits

class TalentScopeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        print(f"🌐 Requête: {path}")

        # Routes principales
        if path == '/' or path == '/auth' or path == '/login':
            self.serve_html_file('auth_interface.html')
        elif path == '/dashboard' or path == '/home':
            self.serve_html_file('modern_dashboard.html')
        elif path == '/analysis':
            # Vérifier si c'est l'étape de vérification
            if 'step=verification' in parsed_path.query:
                self.serve_html_file('analysis_interface_verification_optimized.html')
            else:
                self.serve_html_file('analysis_interface_optimized.html')
        elif path == '/profile':
            self.serve_html_file('profile_management.html')
        elif path == '/users' or path == '/user-management':
            self.serve_html_file('user_management.html')
        elif path == '/config':
            self.serve_html_file('modern_dashboard.html')
        elif path == '/diagnostic':
            self.serve_html_file('diagnostic_complet.html')
        elif path == '/test':
            self.serve_html_file('test_user_data.html')
        elif path == '/migrate' or path == '/migration':
            self.serve_html_file('migrate_accounts.html')
        else:
            # Essayer de servir le fichier directement
            filename = path.lstrip('/')
            if not filename:
                filename = 'index.html'
            
            if os.path.exists(filename):
                print(f"📁 Servir statique: {filename}")
                self.serve_file(filename)
            elif os.path.exists(os.path.join('Logos', filename)):
                print(f"📁 Servir logo: {os.path.join('Logos', filename)}")
                self.serve_file(os.path.join('Logos', filename))
            else:
                print(f"❌ Fichier non trouvé: {filename}")
                self.send_error(404, f"File not found: {filename}")

    def serve_html_file(self, filename):
        if os.path.exists(filename):
            print(f"📄 Servir HTML: {filename}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(filename, 'rb') as f:
                self.wfile.write(f.read())
            print(f"✅ HTML servi: {filename}")
        else:
            print(f"❌ Fichier HTML non trouvé: {filename}")
            self.send_error(404, f"HTML file not found: {filename}")

    def serve_file(self, filename):
        try:
            if os.path.exists(filename):
                content_type = self.guess_type(filename)
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
                print(f"✅ Statique servi: {filename}")
            else:
                print(f"❌ Fichier non trouvé: {filename}")
                self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            print(f"❌ Erreur lors du service du fichier {filename}: {e}")
            self.send_error(500, f"Server error: {e}")

    def log_message(self, format, *args):
        """Log personnalisé"""
        print(f"[{self.date_time_string()}] {format % args}")

def main():
    # Changer vers le répertoire du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 TALENTSCOPE - SERVEUR MULTI-UTILISATEURS FINAL")
    print("==================================================")
    print("🔐 Interface d'authentification")
    print("🎨 Dashboard moderne")
    print("🚀 Interface d'analyse")
    print("👤 Gestion de profil")
    print("👥 Gestion des utilisateurs")
    print("🔍 Outils de diagnostic")
    print("==================================================")

    with socketserver.TCPServer(("", PORT), TalentScopeHandler) as httpd:
        print(f"✅ Serveur démarré sur http://localhost:{PORT}")
        print(f"🌐 Page d'accueil: http://localhost:{PORT}/auth")
        print(f"📊 Dashboard: http://localhost:{PORT}/dashboard")
        print(f"🔍 Analyse: http://localhost:{PORT}/analysis")
        print(f"👤 Profil: http://localhost:{PORT}/profile")
        print(f"👥 Gestion utilisateurs: http://localhost:{PORT}/users")
        print(f"🔍 Diagnostic: http://localhost:{PORT}/diagnostic")
        print(f"🧪 Test données: http://localhost:{PORT}/test")
        print("==================================================")
        print("🔄 Le serveur est en cours d'exécution...")
        print("📝 Appuyez sur Ctrl+C pour arrêter")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté.")

if __name__ == "__main__":
    main()


