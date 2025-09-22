#!/usr/bin/env python3
"""
Script de test pour vérifier que toutes les pages sont accessibles
"""

import requests
import time

def test_server():
    base_url = "http://localhost:8080"
    
    # Pages à tester
    pages = [
        ("/", "Page d'accueil"),
        ("/auth", "Page d'authentification"),
        ("/dashboard", "Dashboard"),
        ("/analysis", "Page d'analyse"),
        ("/profile", "Gestion du profil"),
        ("/settings", "Paramètres"),
        ("/processed", "CVs traités")
    ]
    
    print("🧪 Test des pages du serveur TalentScope")
    print("=" * 50)
    
    for path, description in pages:
        try:
            url = base_url + path
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: {url} - OK")
            else:
                print(f"❌ {description}: {url} - Erreur {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {url} - Erreur de connexion: {e}")
    
    print("=" * 50)
    print("🎉 Test terminé !")

if __name__ == "__main__":
    test_server()
