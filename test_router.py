#!/usr/bin/env python3
"""
Serveur de test simple pour vérifier le routage
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Requête: {self.path}")
        
        # Routes de test
        if self.path == '/auth' or self.path == '/':
            self.serve_file('auth_interface.html')
        elif self.path == '/dashboard':
            self.serve_file('modern_dashboard.html')
        elif self.path == '/analysis':
            self.serve_file('analysis_interface.html')
        elif self.path == '/profile':
            self.serve_file('profile_management.html')
        else:
            # Essayer de servir le fichier directement
            filename = self.path.lstrip('/')
            if filename == '':
                filename = 'auth_interface.html'
            self.serve_file(filename)
    
    def serve_file(self, filename):
        print(f"Tentative de servir: {filename}")
        
        if os.path.exists(filename):
            print(f"✅ Fichier trouvé: {filename}")
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                print(f"✅ Fichier servi avec succès: {filename}")
            except Exception as e:
                print(f"❌ Erreur lors de la lecture: {e}")
                self.send_error(500, str(e))
        else:
            print(f"❌ Fichier non trouvé: {filename}")
            self.send_error(404, f"File not found: {filename}")
    
    def log_message(self, format, *args):
        print(f"[{self.date_time_string()}] {format % args}")

if __name__ == "__main__":
    server = HTTPServer(('', 8082), TestHandler)
    print("🧪 Serveur de test démarré sur http://localhost:8082")
    print("📝 Testez: http://localhost:8082/auth")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur de test...")
        server.shutdown()

