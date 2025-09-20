#!/usr/bin/env python3
"""
Script pour corriger le bloc elif page == 'analysis'
"""

def fix_analysis_block():
    # Lire le fichier
    with open('launch_ultra_simple.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Corriger les lignes du bloc analysis (2429-2435)
    lines[2428] = '                st.session_state.current_page = 1\n'
    lines[2429] = '                st.session_state.job_description = ""\n'
    lines[2430] = '                st.session_state.uploaded_cvs = []\n'
    lines[2431] = '                st.session_state.analysis_complete = False\n'
    lines[2432] = '                st.session_state.ml_results = None\n'
    lines[2433] = '                st.session_state.cv_data = {}\n'
    lines[2434] = '                st.session_state.show_analysis = True\n'
    
    # Écrire le fichier corrigé
    with open('launch_ultra_simple.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Bloc analysis corrigé avec succès!")

if __name__ == "__main__":
    fix_analysis_block()

