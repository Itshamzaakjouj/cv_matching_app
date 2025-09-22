#!/usr/bin/env python3
"""
Test simple de la connexion
"""

import webbrowser
import time

def main():
    print("🧪 Test de la connexion TalentScope")
    print("=" * 50)
    
    # Attendre que le serveur démarre
    print("⏳ Attente du démarrage du serveur...")
    time.sleep(3)
    
    # Ouvrir l'interface d'authentification
    print("🌐 Ouverture de l'interface d'authentification...")
    webbrowser.open('http://localhost:8080/auth')
    
    print("\n✅ Interface ouverte !")
    print("\n🔑 Identifiants de test:")
    print("   👨‍💼 Admin: akjouj17@gmail.com / Hamza12345")
    print("   👩‍💼 User: elhafsaghazouani@gmail.com / Hafsa2003")
    print("\n💡 La connexion devrait maintenant fonctionner !")

if __name__ == "__main__":
    main()
