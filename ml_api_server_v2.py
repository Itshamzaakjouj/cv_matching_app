#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TalentScope - Serveur API ML v2.0
Serveur Flask pour l'analyse avancée de CVs
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from advanced_ml_analyzer_v2 import analyze_cvs_advanced

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze-advanced', methods=['POST'])
def analyze_advanced():
    """Endpoint pour l'analyse avancée des CVs"""
    try:
        data = request.get_json()
        job_data = data.get('job_data', {})
        cv_files = data.get('cv_files', [])
        
        # Analyse avec l'algorithme ML avancé
        results = analyze_cvs_advanced(job_data, cv_files)
        
        # Calcul des statistiques
        total_cvs = len(results)
        scores = [r['score'] for r in results]
        average_score = sum(scores) / len(scores) if scores else 0
        best_match = max(scores) if scores else 0
        
        response = {
            'success': True,
            'totalCvs': total_cvs,
            'averageScore': round(average_score, 1),
            'bestMatch': round(best_match, 1),
            'cvDetails': results,
            'timestamp': results[0]['timestamp'] if results else None
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de santé du serveur"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'service': 'TalentScope ML API'
    })

if __name__ == '__main__':
    print("🚀 Démarrage du serveur ML API v2.0...")
    print("📊 Algorithme d'apprentissage continu activé")
    print("🔗 API disponible sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
