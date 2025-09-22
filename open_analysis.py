#!/usr/bin/env python3
"""
Ouvre directement la page d'analyse des CVs
"""

import webbrowser
import time

def open_analysis_page():
    """Ouvre la page d'analyse dans le navigateur."""
    print("🔍 Ouverture de la page d'analyse des CVs...")
    
    analysis_url = "http://localhost:8080/analysis"
    dashboard_url = "http://localhost:8080/dashboard"
    
    try:
        # Ouvrir la page d'analyse
        webbrowser.open(analysis_url)
        print(f"✅ Page d'analyse ouverte: {analysis_url}")
        
        time.sleep(1)
        
        # Ouvrir aussi le dashboard pour référence
        webbrowser.open(dashboard_url)
        print(f"✅ Dashboard ouvert: {dashboard_url}")
        
        print("\n🎯 Pages ouvertes:")
        print(f"   🔍 Analyse: {analysis_url}")
        print(f"   🏛️  Dashboard: {dashboard_url}")
        print("\n💡 Vous pouvez maintenant:")
        print("   1. Utiliser directement la page d'analyse")
        print("   2. Ou cliquer sur 'Commencer l'analyse' dans le dashboard")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ouverture: {e}")
        print("Veuillez ouvrir manuellement:")
        print(f"   Analyse: {analysis_url}")
        print(f"   Dashboard: {dashboard_url}")

if __name__ == "__main__":
    open_analysis_page()
