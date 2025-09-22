#!/usr/bin/env python3
"""
Lanceur pour les pages d'analyse des CVs
"""

import subprocess
import sys
import time
import webbrowser
import os

def start_simple_server():
    """Démarre le serveur simple."""
    print("🚀 Démarrage du serveur simple...")
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)
        
        process = subprocess.Popen([sys.executable, "simple_server.py"])
        print(f"✅ Serveur simple démarré (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur simple: {e}")
        return None

def main():
    print("TALENTSCOPE - ANALYSE DES CVs")
    print("=" * 60)
    print("Initialisation et démarrage du serveur...")
    print("=" * 60)

    simple_server_process = start_simple_server()
    if not simple_server_process:
        print("Impossible de démarrer l'application. Veuillez vérifier les logs d'erreur.")
        return

    time.sleep(3)  # Attendre un court instant pour que le serveur démarre

    print("\n🎉 Application TalentScope Démarrée !")
    print("🌐 Pages d'analyse disponibles:")
    print("   🏛️  Dashboard: http://localhost:8080/dashboard")
    print("   🔍 Analyse (4 étapes): http://localhost:8080/analysis")
    print("   📁 CVs Traités: http://localhost:8080/processed")
    print("   👤 Profil: http://localhost:8080/profile")
    print("   ⚙️ Configuration: http://localhost:8080/settings")
    print("=" * 60)
    print("📱 Ouverture automatique du dashboard...")

    try:
        webbrowser.open('http://localhost:8080/dashboard')
    except Exception as e:
        print(f"⚠️ Impossible d'ouvrir automatiquement le navigateur: {e}")
        print("   Veuillez ouvrir manuellement: http://localhost:8080/dashboard")

    print("\n💡 Instructions:")
    print("   1. Dans le dashboard, cliquez sur 'Commencer l'analyse'")
    print("   2. Vous serez redirigé vers la page d'analyse avec 4 étapes")
    print("   3. Suivez les étapes pour analyser vos CVs")
    print("\n💡 Utilisez Ctrl+C pour arrêter l'application")
    print("=" * 60)

    try:
        simple_server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
    finally:
        if simple_server_process.poll() is None:
            simple_server_process.terminate()
            simple_server_process.wait(timeout=5)
            print("Serveur simple arrêté.")
        print("✅ Application arrêtée proprement.")

if __name__ == "__main__":
    main()
