import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8888

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    time.sleep(2)
    webbrowser.open(f'http://127.0.0.1:{PORT}/test.html')

try:
    # Créer le serveur qui écoute sur toutes les interfaces
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Serveur démarré sur le port {PORT}")
        print(f"📱 Testez ces URLs:")
        print(f"   http://localhost:{PORT}/test.html")
        print(f"   http://127.0.0.1:{PORT}/test.html")
        print(f"   http://0.0.0.0:{PORT}/test.html")
        print("=" * 50)
        
        # Ouvrir automatiquement le navigateur
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("💡 Appuyez sur Ctrl+C pour arrêter")
        httpd.serve_forever()
        
except OSError as e:
    if e.errno == 10048:  # Port déjà utilisé
        print(f"❌ Le port {PORT} est déjà utilisé. Essayons le port {PORT + 1}")
        PORT += 1
        with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Serveur démarré sur le port {PORT}")
            print(f"📱 Testez: http://localhost:{PORT}/test.html")
            httpd.serve_forever()
    else:
        print(f"❌ Erreur: {e}")
except KeyboardInterrupt:
    print("\n🛑 Arrêt du serveur...")
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")

