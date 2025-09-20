from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class BasicHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Requête reçue pour: {self.path}")  # Log pour le débogage
        
        # Redirection de base
        if self.path == '/' or self.path == '/auth':
            self.path = '/login.html'
        
        try:
            # Tentative d'ouverture du fichier
            return SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            print(f"Erreur lors du traitement de la requête: {e}")
            # En cas d'erreur, servir la page de login
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())

def run_server(port=8080):
    try:
        # S'assurer que nous sommes dans le bon répertoire
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        print(f"Dossier courant: {os.getcwd()}")
        
        # Lister les fichiers disponibles
        print("\nFichiers disponibles:")
        for file in os.listdir():
            print(f"- {file}")
        
        # Démarrer le serveur
        server = HTTPServer(('', port), BasicHandler)
        print(f"\n🚀 Serveur démarré sur http://localhost:{port}")
        print(f"📱 Page de connexion: http://localhost:{port}/login.html")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")

if __name__ == '__main__':
    run_server()

