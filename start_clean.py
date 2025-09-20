#!/usr/bin/env python3
"""
Lanceur avec URLs propres (sans extensions)
"""

import subprocess
import sys
import time
import webbrowser
import threading

def start_server():
    """Démarrer le serveur avec routage"""
    try:
        subprocess.run([sys.executable, "router.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")

def open_browser():
    """Ouvrir le navigateur après un délai"""
    time.sleep(2)
    webbrowser.open("http://localhost:8082/auth")

def main():
    print("🚀 Démarrage de TalentScope avec URLs propres...")
    
    # Démarrer le serveur dans un thread séparé
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Ouvrir le navigateur
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Attendre que le serveur se termine
        server_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")

if __name__ == "__main__":
    main()

