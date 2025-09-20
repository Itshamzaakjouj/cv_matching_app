#!/usr/bin/env python3
"""
Script pour corriger les erreurs d'indentation dans launch_ultra_simple.py
"""

def fix_indentation():
    # Lire le fichier
    with open('launch_ultra_simple.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Corriger les lignes problématiques
    for i, line in enumerate(lines):
        # Ligne 2066 (index 2065)
        if i == 2065 and line.strip() == 'st.success("✅ Configuration sauvegardée avec succès!"):':
            lines[i] = '                st.success("✅ Configuration sauvegardée avec succès!")\n'
        # Ligne 2073 (index 2072)  
        elif i == 2072 and line.strip() == 'st.markdown("🔄 **Redémarrage de l\'application pour appliquer les changements...**"):':
            lines[i] = '                st.markdown("🔄 **Redémarrage de l\'application pour appliquer les changements...**")\n'
        # Ligne 2086 (index 2085)
        elif i == 2085 and line.strip() == 'st.rerun():':
            lines[i] = '                st.rerun()\n'
    
    # Écrire le fichier corrigé
    with open('launch_ultra_simple.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Erreurs d'indentation corrigées!")

if __name__ == "__main__":
    fix_indentation()

