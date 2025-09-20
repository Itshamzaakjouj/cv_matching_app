from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class SimpleAuthHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Rediriger / vers /auth
        if self.path == '/':
            self.path = '/auth'
            
        # Gérer les routes principales
        if self.path == '/auth':
            self.path = 'auth_interface.html'
        elif self.path == '/dashboard':
            self.path = 'modern_dashboard.html'
        elif self.path == '/analysis':
            self.path = 'analysis_interface.html'
            
        # Servir les fichiers statiques
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            credentials = json.loads(post_data.decode('utf-8'))

            # Données de test
            valid_credentials = {
                'akjouj17@gmail.com': 'Hamza12345',
                'elhafsaghazouani@gmail.com': 'Hafsa2003'
            }

            email = credentials.get('email')
            password = credentials.get('password')

            # Vérifier les identifiants
            if email in valid_credentials and valid_credentials[email] == password:
                response = {
                    'success': True,
                    'message': 'Connexion réussie',
                    'redirect': '/dashboard'
                }
                status_code = 200
            else:
                response = {
                    'success': False,
                    'message': 'Identifiants incorrects'
                }
                status_code = 401

            # Envoyer la réponse
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8080):
    try:
        # S'assurer que nous sommes dans le bon répertoire
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Démarrer le serveur
        server = HTTPServer(('localhost', port), SimpleAuthHandler)
        print(f"🚀 Serveur démarré sur http://localhost:{port}")
        print("=" * 50)
        print("📱 Interfaces disponibles:")
        print(f"   🔐 Authentification: http://localhost:{port}/auth")
        print(f"   📊 Dashboard: http://localhost:{port}/dashboard")
        print(f"   🔍 Analyse: http://localhost:{port}/analysis")
        print("=" * 50)
        print("💡 Utilisez Ctrl+C pour arrêter")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Erreur: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        server.shutdown()

if __name__ == '__main__':
    run_server()

