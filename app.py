from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class ModernAppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Gérer les routes principales
        routes = {
            '/': 'auth_interface.html',
            '/auth': 'auth_interface.html',
            '/dashboard': 'modern_dashboard.html',
            '/analysis': 'analysis_interface.html'
        }
        
        # Si c'est une route connue, servir le fichier correspondant
        if self.path in routes:
            self.path = routes[self.path]
        
        # Gérer les fichiers statiques
        try:
            return SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            print(f"Erreur lors du traitement de la requête GET: {e}")
            self.send_error(500, f"Erreur serveur: {str(e)}")

    def do_POST(self):
        if self.path == '/api/login':
            try:
                # Lire les données du corps de la requête
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                credentials = json.loads(post_data.decode('utf-8'))

                # Vérifier les identifiants
                valid_users = {
                    "akjouj17@gmail.com": {
                        "password": "Hamza12345",
                        "name": "Akjouj Hamza",
                        "role": "admin"
                    },
                    "elhafsaghazouani@gmail.com": {
                        "password": "Hafsa2003",
                        "name": "Hafsa El Ghazouani",
                        "role": "user"
                    }
                }

                email = credentials.get('email')
                password = credentials.get('password')

                if email in valid_users and valid_users[email]['password'] == password:
                    response = {
                        'success': True,
                        'user': {
                            'name': valid_users[email]['name'],
                            'role': valid_users[email]['role'],
                            'email': email
                        },
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
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                print(f"Erreur lors du traitement de la requête POST: {e}")
                self.send_error(500, f"Erreur serveur: {str(e)}")
        else:
            self.send_error(404, "Route non trouvée")

def run_server(port=8080):
    try:
        # S'assurer que nous sommes dans le bon répertoire
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Démarrer le serveur
        server_address = ('', port)
        httpd = HTTPServer(server_address, ModernAppHandler)
        
        print(f"🚀 Serveur démarré sur http://localhost:{port}")
        print("=" * 50)
        print("📱 Interfaces disponibles:")
        print(f"   🔐 Authentification: http://localhost:{port}/auth")
        print(f"   📊 Dashboard: http://localhost:{port}/dashboard")
        print(f"   🔍 Analyse: http://localhost:{port}/analysis")
        print("=" * 50)
        print("💡 Utilisez Ctrl+C pour arrêter")
        
        httpd.serve_forever()
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()

