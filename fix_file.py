#!/usr/bin/env python3
"""
Script pour corriger définitivement les erreurs d'indentation
"""

def fix_file():
    # Lire le fichier
    with open('launch_ultra_simple.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Corriger les lignes spécifiques
    lines[2065] = '                st.success("✅ Configuration sauvegardée avec succès!")\n'
    lines[2072] = '                st.markdown("🔄 **Redémarrage de l\'application pour appliquer les changements...**")\n'
    lines[2085] = '                st.rerun()\n'
    
    # Écrire le fichier corrigé
    with open('launch_ultra_simple.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fichier corrigé avec succès!")

if __name__ == "__main__":
    fix_file()

