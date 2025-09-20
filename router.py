#!/usr/bin/env python3
"""
Système de routage simple pour masquer les extensions de fichiers
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.parse

class RouterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parser l'URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        print(f"🌐 Requête reçue: {path}")
        
        # Routes propres (sans extension)
        routes = {
            '/': 'auth_interface.html',
            '/auth': 'auth_interface.html',
            '/login': 'auth_interface.html',
            '/dashboard': 'modern_dashboard.html',
            '/home': 'modern_dashboard.html',
            '/analysis': 'analysis_interface.html',
            '/profile': 'profile_management.html',
            '/config': 'modern_dashboard.html#config-section'
        }
        
        # Vérifier si c'est une route propre
        if path in routes:
            target_file = routes[path]
            print(f"✅ Route trouvée: {path} -> {target_file}")
            self.serve_file(target_file)
        else:
            # Essayer de servir le fichier directement
            direct_file = path.lstrip('/')
            print(f"🔍 Tentative de servir directement: {direct_file}")
            self.serve_file(direct_file)
    
    def serve_file(self, filename):
        try:
            # Vérifier si le fichier existe
            if os.path.exists(filename):
                # Déterminer le type de contenu
                content_type = self.get_content_type(filename)
                
                # Lire le fichier
                with open(filename, 'rb') as f:
                    content = f.read()
                
                # Envoyer la réponse
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                print(f"❌ Fichier non trouvé: {filename}")
                self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            print(f"❌ Erreur serveur: {str(e)}")
            self.send_error(500, f"Server error: {str(e)}")
    
    def get_content_type(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            '.html': 'text/html',
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
        return content_types.get(ext, 'text/plain')
    
    def log_message(self, format, *args):
        # Log personnalisé
        print(f"[{self.date_time_string()}] {format % args}")

def run_server(port=8082):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RouterHandler)
    
    print("🏛️ TALENTSCOPE - SERVEUR AVEC ROUTAGE")
    print("=" * 50)
    print("🔐 Interface d'authentification")
    print("🎨 Dashboard moderne")
    print("🚀 Interface d'analyse")
    print("=" * 50)
    print(f"✅ Serveur démarré sur http://localhost:{port}")
    print("🌐 Interface d'authentification: http://localhost:8082/auth")
    print("📊 Dashboard: http://localhost:8082/dashboard")
    print("🔍 Analyse: http://localhost:8082/analysis")
    print("👤 Profil: http://localhost:8082/profile")
    print("⚙️ Configuration: http://localhost:8082/config")
    print("🔄 Le serveur est en cours d'exécution...")
    print("📝 Appuyez sur Ctrl+C pour arrêter")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
