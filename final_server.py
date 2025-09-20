#!/usr/bin/env python3
"""
Serveur final pour TalentScope - Interface d'analyse complète
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse

class TalentScopeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parser l'URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
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
        elif path == '/config':
            self.serve_html_file('modern_dashboard.html')
        else:
            # Essayer de servir le fichier directement
            filename = path.lstrip('/')
            if not filename:
                filename = 'auth_interface.html'
            
            # Vérifier si c'est un fichier statique
            if self.is_static_file(filename):
                self.serve_static_file(filename)
            else:
                # Essayer de servir comme HTML
                if not filename.endswith('.html'):
                    filename += '.html'
                self.serve_html_file(filename)
    
    def is_static_file(self, filename):
        """Vérifier si c'est un fichier statique (CSS, JS, images, etc.)"""
        static_extensions = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.json']
        return any(filename.lower().endswith(ext) for ext in static_extensions)
    
    def serve_html_file(self, filename):
        """Servir un fichier HTML"""
        print(f"📄 Servir HTML: {filename}")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                print(f"✅ HTML servi: {filename}")
            except Exception as e:
                print(f"❌ Erreur HTML: {e}")
                self.send_error(500, f"Erreur serveur: {str(e)}")
        else:
            print(f"❌ HTML non trouvé: {filename}")
            self.send_error(404, f"Fichier non trouvé: {filename}")
    
    def serve_static_file(self, filename):
        """Servir un fichier statique"""
        print(f"📁 Servir statique: {filename}")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                
                # Déterminer le type de contenu
                content_type = self.get_content_type(filename)
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                print(f"✅ Statique servi: {filename}")
            except Exception as e:
                print(f"❌ Erreur statique: {e}")
                self.send_error(500, f"Erreur serveur: {str(e)}")
        else:
            print(f"❌ Statique non trouvé: {filename}")
            self.send_error(404, f"Fichier non trouvé: {filename}")
    
    def get_content_type(self, filename):
        """Déterminer le type de contenu"""
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def log_message(self, format, *args):
        """Log personnalisé"""
        print(f"[{self.date_time_string()}] {format % args}")

def main():
    PORT = 8084  # Nouveau port pour éviter les conflits
    
    # Changer vers le répertoire du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Créer le serveur
    with socketserver.TCPServer(("", PORT), TalentScopeHandler) as httpd:
        print("🚀 TALENTSCOPE - SERVEUR FINAL")
        print("=" * 50)
        print("🔐 Interface d'authentification")
        print("🎨 Dashboard moderne")
        print("🚀 Interface d'analyse (4 étapes)")
        print("=" * 50)
        print(f"✅ Serveur démarré sur http://localhost:{PORT}")
        print(f"🌐 Page d'accueil: http://localhost:{PORT}/auth")
        print(f"📊 Dashboard: http://localhost:{PORT}/dashboard")
        print(f"🔍 Analyse: http://localhost:{PORT}/analysis")
        print(f"👤 Profil: http://localhost:{PORT}/profile")
        print("=" * 50)
        print("🔄 Le serveur est en cours d'exécution...")
        print("📝 Appuyez sur Ctrl+C pour arrêter")
        
        # Ouvrir le navigateur
        try:
            webbrowser.open(f'http://localhost:{PORT}/auth')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
