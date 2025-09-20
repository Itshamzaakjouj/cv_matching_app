#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur de test pour la migration
"""

import http.server
import socketserver
import os

PORT = 8088

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = self.path
        print(f"🌐 Requête: {parsed_path}")
        
        if parsed_path == '/migrate':
            print("📄 Servir migrate_accounts.html")
            self.serve_html_file('migrate_accounts.html')
        elif parsed_path == '/auth' or parsed_path == '/':
            print("📄 Servir auth_interface.html")
            self.serve_html_file('auth_interface.html')
        elif parsed_path == '/dashboard':
            print("📄 Servir modern_dashboard.html")
            self.serve_html_file('modern_dashboard.html')
        elif parsed_path == '/profile':
            print("📄 Servir profile_management.html")
            self.serve_html_file('profile_management.html')
        elif parsed_path == '/analysis':
            print("📄 Servir analysis_interface_optimized.html")
            self.serve_html_file('analysis_interface_optimized.html')
        else:
            # Servir le fichier directement
            filename = parsed_path.lstrip('/')
            if not filename:
                filename = 'index.html'
            
            if os.path.exists(filename):
                print(f"📁 Servir fichier: {filename}")
                self.serve_file(filename)
            else:
                print(f"❌ Fichier non trouvé: {filename}")
                self.send_error(404, f"File not found: {filename}")

    def serve_html_file(self, filename):
        if os.path.exists(filename):
            print(f"✅ Fichier trouvé: {filename}")
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
                print(f"✅ Fichier servi: {filename}")
            else:
                print(f"❌ Fichier non trouvé: {filename}")
                self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            self.send_error(500, f"Server error: {e}")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🧪 SERVEUR DE TEST - MIGRATION")
    print("================================")
    print(f"✅ Serveur démarré sur http://localhost:{PORT}")
    print(f"🔄 Migration: http://localhost:{PORT}/migrate")
    print(f"🔐 Auth: http://localhost:{PORT}/auth")
    print("================================")

    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté.")

if __name__ == "__main__":
    main()


