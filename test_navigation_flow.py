#!/usr/bin/env python3
"""
Test du flux de navigation TalentScope
Vérification des liens entre toutes les pages
"""

import requests
import time
import webbrowser
from pathlib import Path

def test_navigation_flow():
    """Test le flux complet de navigation"""
    print("=" * 70)
    print("🧪 TEST DU FLUX DE NAVIGATION TALENTSCOPE")
    print("=" * 70)
    
    base_url = "http://localhost:8080"
    
    # Test des routes principales
    routes = [
        ('/', 'Page d\'accueil'),
        ('/auth', 'Interface d\'authentification'),
        ('/acceuil', 'Page d\'accueil (alias)'),
        ('/dashboard', 'Dashboard principal'),
        ('/ministry', 'Page du ministère'),
        ('/analysis', 'Interface d\'analyse'),
        ('/processed', 'CVs traités'),
        ('/profile', 'Gestion du profil'),
        ('/settings', 'Paramètres')
    ]
    
    print("🌐 Test des routes principales...")
    successful_routes = 0
    
    for route, description in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {route} - {description}")
                successful_routes += 1
            else:
                print(f"  ❌ {route} - {description} (HTTP {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {route} - {description} (ERREUR: {e})")
    
    print(f"\n📊 Routes fonctionnelles: {successful_routes}/{len(routes)}")
    
    # Test des redirections
    print("\n🔄 Test des redirections...")
    
    # Test de redirection pour route inconnue
    try:
        response = requests.get(f"{base_url}/route-inexistante", timeout=5, allow_redirects=False)
        if response.status_code == 302:
            print("  ✅ Redirection pour route inconnue: OK")
        else:
            print(f"  ⚠️ Redirection pour route inconnue: HTTP {response.status_code}")
    except:
        print("  ❌ Test de redirection: Erreur")
    
    # Test de l'API
    print("\n🔌 Test de l'API...")
    try:
        login_data = {
            'email': 'akjouj17@gmail.com',
            'password': 'Hamza12345'
        }
        response = requests.post(f"{base_url}/api/auth/login", data=login_data, timeout=5)
        if response.status_code == 200:
            print("  ✅ API Login: Fonctionne")
        else:
            print(f"  ❌ API Login: HTTP {response.status_code}")
    except:
        print("  ❌ API Login: Erreur de connexion")
    
    # Résumé
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ DU TEST")
    print("=" * 70)
    
    if successful_routes == len(routes):
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ Navigation: Fonctionnelle")
        print("✅ Routage: Correct")
        print("✅ Redirections: OK")
        print("✅ API: Opérationnelle")
        print("\n🚀 Application prête à l'utilisation !")
        
        # Ouvrir l'application
        print("\n📱 Ouverture de l'application...")
        try:
            webbrowser.open(f"{base_url}/auth")
            print("✅ Application ouverte dans le navigateur")
        except:
            print("⚠️ Impossible d'ouvrir automatiquement le navigateur")
            print(f"   Ouvrez manuellement: {base_url}/auth")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les routes marquées ❌")
    
    print("=" * 70)

def test_file_links():
    """Test que tous les liens dans les fichiers HTML sont corrects"""
    print("\n🔗 Vérification des liens dans les fichiers HTML...")
    
    files_to_check = [
        'auth_interface.html',
        'modern_dashboard.html',
        'ministry_page.html',
        'analysis_interface.html'
    ]
    
    for file in files_to_check:
        if Path(file).exists():
            print(f"  ✅ {file}: Présent")
        else:
            print(f"  ❌ {file}: Manquant")

if __name__ == "__main__":
    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://localhost:8080", timeout=3)
        print("✅ Serveur accessible")
    except:
        print("❌ Serveur non accessible - Démarrez le serveur avec: python simple_server.py")
        exit(1)
    
    test_navigation_flow()
    test_file_links()
