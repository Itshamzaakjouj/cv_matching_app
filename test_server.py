from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

def run_server(port=8000):
    try:
        # Afficher le répertoire actuel
        current_dir = os.getcwd()
        print(f"Répertoire actuel : {current_dir}")
        
        # Lister les fichiers
        print("\nFichiers disponibles :")
        for file in os.listdir(current_dir):
            print(f"- {file}")
        
        # Créer et démarrer le serveur
        server_address = ('', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        
        print(f"\n✅ Serveur démarré sur http://localhost:{port}")
        print(f"📄 Test page: http://localhost:{port}/test.html")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
        
        httpd.serve_forever()
        
    except Exception as e:
        print(f"\n❌ Erreur : {str(e)}")
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

