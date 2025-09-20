"""
Serveur HTTP simple pour servir les fichiers statiques et gérer les analyses de CVs
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse
import sys

def find_available_port(start_port=8096):
    """Trouve un port disponible en commençant par start_port"""
    port = start_port
    while port < start_port + 10:  # Essaie 10 ports
        try:
            with socketserver.TCPServer(("", port), None) as test_server:
                return port
        except OSError:
            port += 1
    raise OSError("Aucun port disponible trouvé")

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Gère les requêtes GET"""
        parsed_path = urlparse(self.path)
        
        # Routes principales
        routes = {
            '/': 'auth_interface.html',
            '/auth': 'auth_interface.html',
            '/dashboard': 'modern_dashboard.html',
            '/analysis': 'analysis_interface_ml_integrated.html',
            '/profile': 'profile_management.html'
        }

        if parsed_path.path in routes:
            self.serve_html_file(routes[parsed_path.path])
        else:
            super().do_GET()

    def do_POST(self):
        """Gère les requêtes POST"""
        if self.path == '/analyze_cvs':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Simuler une analyse avec des données de test
                analysis_results = {
                    "averageScore": 0.75,
                    "bestScore": 0.92,
                    "scoreDistribution": [2, 4, 8, 5, 3],
                    "candidates": [
                        {
                            "name": "CV_Senior_Dev.pdf",
                            "score": 0.92,
                            "skillsScore": 0.95,
                            "experienceScore": 0.90,
                            "details": {
                                "matchingSkills": ["Python", "Machine Learning", "SQL"],
                                "missingSkills": ["Spark"],
                                "yearsOfExperience": 5
                            }
                        },
                        {
                            "name": "CV_Data_Engineer.pdf",
                            "score": 0.85,
                            "skillsScore": 0.88,
                            "experienceScore": 0.82,
                            "details": {
                                "matchingSkills": ["Python", "SQL", "Data Visualization"],
                                "missingSkills": ["Machine Learning", "Spark"],
                                "yearsOfExperience": 3
                            }
                        },
                        {
                            "name": "CV_ML_Engineer.pdf",
                            "score": 0.78,
                            "skillsScore": 0.80,
                            "experienceScore": 0.75,
                            "details": {
                                "matchingSkills": ["Python", "Machine Learning"],
                                "missingSkills": ["SQL", "Spark"],
                                "yearsOfExperience": 2
                            }
                        }
                    ],
                    "skillsAnalysis": {
                        "labels": ["Python", "ML", "SQL", "Data Viz", "Cloud"],
                        "required": [1, 1, 1, 0.8, 0.6],
                        "found": [0.9, 0.8, 0.7, 0.6, 0.5]
                    }
                }

                # Envoyer la réponse
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(analysis_results).encode())
                
            except Exception as e:
                print(f"Erreur lors de l'analyse: {e}")
                self.send_error(500, f"Erreur serveur: {str(e)}")
        else:
            self.send_error(404)

    def serve_html_file(self, filename):
        """Sert un fichier HTML avec injection de code si nécessaire"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

                # Injection de code pour auth_interface.html
                if filename == 'auth_interface.html':
                    injection_script = """
                    <script>
                        if (!window.userDatabase.emailExists("akjouj17@gmail.com")) {
                            window.userDatabase.createUser("akjouj17@gmail.com", "Hamza12345", "Akjouj Hamza", "Développement", "Développeur Senior", "0631249765");
                        }
                        if (!window.userDatabase.emailExists("elhafsaghazouani@gmail.com")) {
                            window.userDatabase.createUser("elhafsaghazouani@gmail.com", "Hafsa2003", "Hafsa El Ghazouani", "Ressources Humaines", "Analyste RH", "0600000000");
                        }
                    </script>
                    </body>
                    """
                    content = content.replace('</body>', injection_script)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Cache-Control', 'no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()
                self.wfile.write(content.encode())
                
                if filename == 'auth_interface.html':
                    print("✅ Page d'authentification servie avec comptes existants")
                elif filename == 'modern_dashboard.html':
                    print("✅ modern_dashboard.html servi")
                elif filename == 'analysis_interface_ml_integrated.html':
                    print("✅ analysis_interface_ml_integrated.html servi")

        except FileNotFoundError:
            self.send_error(404, f"File not found: {filename}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

def run_server():
    """Démarre le serveur HTTP"""
    try:
        # Trouve un port disponible
        port = find_available_port()
        
        with socketserver.TCPServer(("", port), RequestHandler) as httpd:
            print("🚀 TALENTSCOPE - SERVEUR STABLE")
            print("="*50)
            print("🎯 Comptes existants inclus automatiquement:")
            print("   • akjouj17@gmail.com / Hamza12345")
            print("   • elhafsaghazouani@gmail.com / Hafsa2003")
            print("="*50)
            print(f"✅ Serveur démarré sur http://localhost:{port}")
            print("="*50)
            print("🌐 URLs disponibles:")
            print(f"   • Authentification: http://localhost:{port}/auth")
            print(f"   • Dashboard: http://localhost:{port}/dashboard")
            print(f"   • Analyse: http://localhost:{port}/analysis")
            print(f"   • Profil: http://localhost:{port}/profile")
            print("="*50)
            print("🔄 Le serveur est en cours d'exécution...")
            print("📝 Appuyez sur Ctrl+C pour arrêter")
            print("="*50)
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        sys.exit(0)

if __name__ == "__main__":
    run_server()