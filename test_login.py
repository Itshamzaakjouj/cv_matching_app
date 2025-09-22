#!/usr/bin/env python3
"""
Test de la fonctionnalité de connexion
"""

import requests
import time

def test_login():
    base_url = "http://localhost:8080"
    
    print("🧪 Test de la fonctionnalité de connexion")
    print("=" * 50)
    
    # Test 1: Connexion avec identifiants corrects
    print("Test 1: Connexion avec identifiants corrects...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            data={
                'email': 'akjouj17@gmail.com',
                'password': 'Hamza12345'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Connexion réussie !")
                print(f"   Utilisateur: {data['user']['name']}")
                print(f"   Rôle: {data['user']['role']}")
            else:
                print(f"❌ Échec de connexion: {data.get('detail', 'Erreur inconnue')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print()
    
    # Test 2: Connexion avec identifiants incorrects
    print("Test 2: Connexion avec identifiants incorrects...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            data={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if not data.get('success'):
                print("✅ Rejet correct des identifiants incorrects")
                print(f"   Message: {data.get('detail', 'Erreur inconnue')}")
            else:
                print("❌ Problème: Les identifiants incorrects ont été acceptés")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print()
    
    # Test 3: Vérification de l'interface d'authentification
    print("Test 3: Vérification de l'interface d'authentification...")
    try:
        response = requests.get(f"{base_url}/auth", timeout=5)
        if response.status_code == 200:
            print("✅ Interface d'authentification accessible")
        else:
            print(f"❌ Interface d'authentification inaccessible: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print("=" * 50)
    print("🎉 Test terminé !")

if __name__ == "__main__":
    # Attendre que le serveur démarre
    print("⏳ Attente du démarrage du serveur...")
    time.sleep(3)
    test_login()
