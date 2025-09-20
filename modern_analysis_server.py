"""
Serveur pour l'interface d'analyse moderne
Interface ultra-optimisée avec HTML/CSS/JavaScript
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os
from pathlib import Path

class ModernAnalysisHandler(http.server.SimpleHTTPRequestHandler):
    """Handler pour servir l'interface d'analyse moderne"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=Path(__file__).parent, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/modern_analysis.html'
        return super().do_GET()

def start_modern_analysis_server():
    """Démarre le serveur d'analyse moderne"""
    PORT = 9000
    
    with socketserver.TCPServer(("", PORT), ModernAnalysisHandler) as httpd:
        print("🚀 Serveur d'analyse moderne démarré")
        print(f"🌐 Interface disponible sur: http://localhost:{PORT}")
        print("⚡ Interface ultra-optimisée avec HTML/CSS/JavaScript")
        print("💡 Utilisez Ctrl+C pour arrêter")
        
        # Ouvrir automatiquement dans le navigateur
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Serveur arrêté")

if __name__ == "__main__":
    start_modern_analysis_server()
