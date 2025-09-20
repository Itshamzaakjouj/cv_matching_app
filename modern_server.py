import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs, urlparse

# Configuration
PORT = 8083
VALID_CREDENTIALS = {
    "akjouj17@gmail.com": "Hamza12345",
    "elhafsaghazouani@gmail.com": "Hafsa2003"
}

class ModernHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Routes principales
        routes = {
            '/': 'auth_interface.html',
            '/auth': 'auth_interface.html',
            '/dashboard': 'modern_dashboard.html',
            '/analysis': 'analysis_interface.html',
            '/home': 'modern_dashboard.html#home-section',
            '/processed': 'modern_dashboard.html#processed-section',
            '/config': 'modern_dashboard.html#config-section'
        }

        # Si c'est une route connue, servir le fichier correspondant
        if path in routes:
            self.path = routes[path]
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            credentials = json.loads(post_data.decode('utf-8'))

            email = credentials.get('email')
            password = credentials.get('password')

            # Vérifier les identifiants
            if email in VALID_CREDENTIALS and VALID_CREDENTIALS[email] == password:
                response = {
                    'success': True,
                    'redirect': '/dashboard',
                    'user': {
                        'email': email,
                        'name': 'Akjouj Hamza' if email == 'akjouj17@gmail.com' else 'Hafsa El Ghazouani'
                    }
                }
                status_code = 200
            else:
                response = {
                    'success': False,
                    'message': 'Identifiants incorrects'
                }
                status_code = 401

            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return

        return http.server.SimpleHTTPRequestHandler.do_POST(self)

def run_server():
    with socketserver.TCPServer(("", PORT), ModernHandler) as httpd:
        print(f"🚀 Serveur démarré sur http://localhost:{PORT}")
        print("=" * 50)
        print("📱 Interfaces disponibles:")
        print(f"   🔐 Authentification: http://localhost:{PORT}/auth")
        print(f"   📊 Dashboard: http://localhost:{PORT}/dashboard")
        print(f"   🔍 Analyse: http://localhost:{PORT}/analysis")
        print("=" * 50)
        print("💡 Utilisez Ctrl+C pour arrêter")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du serveur...")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()

