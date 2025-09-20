#!/usr/bin/env python3
"""
TALENTSCOPE - APPLICATION MODERNE FINALE
Ministère de l'Économie et des Finances
Version: 7.0 - Interface Moderne Complète
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def main():
    """Fonction principale de lancement de l'application moderne"""
    print("TALENTSCOPE - APPLICATION MODERNE FINALE")
    print("=" * 60)
    print("Interface d'authentification moderne")
    print("Dashboard moderne inspiré de l'interface d'auth")
    print("=" * 60)
    
    # Vérifier que les fichiers existent
    if not Path("auth_interface.html").exists():
        print("Fichier auth_interface.html non trouvé")
        return
    
    if not Path("modern_dashboard.html").exists():
        print("Fichier modern_dashboard.html non trouvé")
        return
    
    print("Démarrage de l'application moderne...")
    
    try:
        # Démarrer le serveur d'authentification
        print("Démarrage du serveur d'authentification...")
        process = subprocess.Popen([
            sys.executable, "auth_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre que le serveur démarre
        time.sleep(3)
        
        print("=" * 60)
        print("APPLICATION MODERNE DEMARREE AVEC SUCCES !")
        print("=" * 60)
        print("Interfaces disponibles:")
        print("   Authentification: http://localhost:8080")
        print("   Dashboard Moderne: http://localhost:8080/modern_dashboard.html")
        print("=" * 60)
        print("Ouverture de l'interface d'authentification...")
        
        # Ouvrir l'interface d'authentification
        webbrowser.open("http://localhost:8080")
        
        print("=" * 60)
        print("Application TalentScope Moderne disponible !")
        print("Utilisez Ctrl+C pour arrêter l'application")
        print("=" * 60)
        
        # Garder l'application en cours d'exécution
        try:
            print("Serveur en cours d'exécution...")
            process.wait()  # Attendre que le processus se termine
        except KeyboardInterrupt:
            print("\nArrêt de l'application...")
        finally:
            # Arrêter le processus
            if process:
                process.terminate()
                process.wait()
                print("Serveur arrêté")
            
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
