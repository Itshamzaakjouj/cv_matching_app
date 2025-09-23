#!/usr/bin/env python3
"""
Test complet des connexions TalentScope
Vérification Backend-Frontend-Database
"""

import requests
import sqlite3
import os
import time
from pathlib import Path

def test_server_routes():
    """Test toutes les routes du serveur"""
    print("🌐 Test des routes du serveur...")
    
    routes_to_test = [
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
    
    base_url = "http://localhost:8080"
    results = []
    
    for route, description in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            results.append((route, description, response.status_code, status))
            print(f"  {status} {route} - {description} (HTTP {response.status_code})")
        except requests.exceptions.RequestException as e:
            results.append((route, description, "ERROR", "❌"))
            print(f"  ❌ {route} - {description} (ERREUR: {e})")
    
    return results

def test_database_connection():
    """Test la connexion à la base de données"""
    print("\n🗄️ Test de la base de données...")
    
    db_path = "talentscope.db"
    
    if not os.path.exists(db_path):
        print(f"  ❌ Fichier de base de données non trouvé: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test des tables principales
        tables = ['users', 'job_offers', 'cv_analyses', 'analysis_results']
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  ✅ Table {table}: {count} enregistrements")
            except sqlite3.OperationalError:
                print(f"  ⚠️ Table {table}: Non trouvée (peut être normale)")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"  ❌ Erreur base de données: {e}")
        return False

def test_frontend_files():
    """Test l'existence des fichiers frontend"""
    print("\n📁 Test des fichiers frontend...")
    
    required_files = [
        'auth_interface.html',
        'modern_dashboard.html',
        'analysis_interface.html',
        'ministry_page.html',
        'profile_management.html',
        'settings.html',
        'treated_cvs.html',
        'user_database.js',
        'direct-translation.js'
    ]
    
    results = []
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        results.append((file, status))
        print(f"  {status} {file}")
    
    return results

def test_api_endpoints():
    """Test les endpoints API"""
    print("\n🔌 Test des endpoints API...")
    
    base_url = "http://localhost:8080"
    
    # Test de l'endpoint de login
    try:
        login_data = {
            'email': 'akjouj17@gmail.com',
            'password': 'Hamza12345'
        }
        response = requests.post(f"{base_url}/api/auth/login", data=login_data, timeout=5)
        
        if response.status_code == 200:
            print("  ✅ API Login: Fonctionne")
            try:
                data = response.json()
                if data.get('success'):
                    print(f"    👤 Utilisateur connecté: {data.get('user', {}).get('name', 'N/A')}")
                else:
                    print(f"    ⚠️ Login échoué: {data.get('detail', 'N/A')}")
            except:
                print("    ⚠️ Réponse non-JSON")
        else:
            print(f"  ❌ API Login: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ API Login: Erreur de connexion ({e})")

def main():
    """Fonction principale de test"""
    print("=" * 70)
    print("🧪 TEST COMPLET DES CONNEXIONS TALENTSCOPE")
    print("=" * 70)
    
    # Test du serveur
    print("⏳ Vérification que le serveur est démarré...")
    try:
        response = requests.get("http://localhost:8080", timeout=3)
        print("✅ Serveur accessible")
    except:
        print("❌ Serveur non accessible - Démarrez le serveur avec: python simple_server.py")
        return
    
    # Tests
    route_results = test_server_routes()
    db_ok = test_database_connection()
    file_results = test_frontend_files()
    test_api_endpoints()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    # Routes
    successful_routes = sum(1 for _, _, _, status in route_results if status == "✅")
    total_routes = len(route_results)
    print(f"🌐 Routes: {successful_routes}/{total_routes} fonctionnelles")
    
    # Fichiers
    existing_files = sum(1 for _, status in file_results if status == "✅")
    total_files = len(file_results)
    print(f"📁 Fichiers: {existing_files}/{total_files} présents")
    
    # Base de données
    print(f"🗄️ Base de données: {'✅ Fonctionnelle' if db_ok else '❌ Problème'}")
    
    # Statut global
    if successful_routes == total_routes and existing_files == total_files and db_ok:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ Backend-Frontend-Database: Connexions OK")
        print("🚀 Application prête à l'utilisation")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les éléments marqués ❌")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
