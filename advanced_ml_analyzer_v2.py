#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TalentScope - Analyseur ML Avancé v2.0
Algorithme d'apprentissage continu pour l'analyse de CVs
"""

import re
import json
import math
import pickle
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict, Counter
import os

class AdvancedMLAnalyzer:
    def __init__(self):
        self.model_file = "ml_model.pkl"
        self.history_file = "analysis_history.json"
        self.weights = self._initialize_weights()
        self.learning_rate = 0.1
        self.load_model()
        self.load_history()
    
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialise les poids du modèle ML"""
        return {
            # Compétences techniques
            'technical_skills': 0.25,
            'programming_languages': 0.20,
            'frameworks': 0.15,
            'databases': 0.10,
            
            # Expérience
            'experience_years': 0.15,
            'relevant_experience': 0.20,
            'project_complexity': 0.10,
            
            # Formation
            'education_level': 0.08,
            'certifications': 0.05,
            'relevant_education': 0.07,
            
            # Soft skills
            'leadership': 0.05,
            'communication': 0.03,
            'teamwork': 0.02,
            
            # Facteurs de qualité
            'cv_quality': 0.05,
            'keyword_density': 0.03,
            'structure_quality': 0.02
        }
    
    def load_model(self):
        """Charge le modèle ML sauvegardé"""
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.weights = saved_data.get('weights', self.weights)
                    print(f"✅ Modèle ML chargé: {len(self.weights)} paramètres")
            except Exception as e:
                print(f"⚠️ Erreur chargement modèle: {e}")
    
    def save_model(self):
        """Sauvegarde le modèle ML"""
        try:
            model_data = {
                'weights': self.weights,
                'timestamp': datetime.now().isoformat(),
                'version': '2.0'
            }
            with open(self.model_file, 'wb') as f:
                pickle.dump(model_data, f)
            print("✅ Modèle ML sauvegardé")
        except Exception as e:
            print(f"❌ Erreur sauvegarde modèle: {e}")
    
    def load_history(self):
        """Charge l'historique des analyses"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                print(f"✅ Historique chargé: {len(self.history)} analyses")
            except Exception as e:
                print(f"⚠️ Erreur chargement historique: {e}")
                self.history = []
        else:
            self.history = []
    
    def save_history(self):
        """Sauvegarde l'historique des analyses"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            print("✅ Historique sauvegardé")
        except Exception as e:
            print(f"❌ Erreur sauvegarde historique: {e}")
    
    def extract_features(self, cv_content: str, job_requirements: Dict) -> Dict[str, float]:
        """Extrait les caractéristiques d'un CV"""
        features = {}
        
        # Normalisation du contenu
        content_lower = cv_content.lower()
        
        # 1. Compétences techniques
        technical_keywords = job_requirements.get('skills', '').lower().split(',')
        features['technical_skills'] = self._calculate_keyword_match(content_lower, technical_keywords)
        
        # 2. Langages de programmation
        programming_langs = ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']
        features['programming_languages'] = self._calculate_keyword_match(content_lower, programming_langs)
        
        # 3. Frameworks
        frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'laravel', 'express', 'tensorflow', 'pytorch', 'scikit-learn']
        features['frameworks'] = self._calculate_keyword_match(content_lower, frameworks)
        
        # 4. Bases de données
        databases = ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite', 'cassandra']
        features['databases'] = self._calculate_keyword_match(content_lower, databases)
        
        # 5. Années d'expérience
        features['experience_years'] = self._extract_experience_years(content_lower)
        
        # 6. Expérience pertinente
        features['relevant_experience'] = self._calculate_relevant_experience(content_lower, job_requirements)
        
        # 7. Niveau d'éducation
        features['education_level'] = self._extract_education_level(content_lower)
        
        # 8. Certifications
        features['certifications'] = self._count_certifications(content_lower)
        
        # 9. Qualité du CV
        features['cv_quality'] = self._assess_cv_quality(cv_content)
        
        # 10. Densité de mots-clés
        features['keyword_density'] = self._calculate_keyword_density(content_lower, technical_keywords)
        
        return features
    
    def _calculate_keyword_match(self, content: str, keywords: List[str]) -> float:
        """Calcule le score de correspondance des mots-clés"""
        if not keywords:
            return 0.0
        
        matches = 0
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword in content:
                matches += 1
        
        return min(matches / len(keywords), 1.0)
    
    def _extract_experience_years(self, content: str) -> float:
        """Extrait les années d'expérience"""
        # Patterns pour détecter l'expérience
        patterns = [
            r'(\d+)\s*ans?\s*d\'?expérience',
            r'(\d+)\s*years?\s*of\s*experience',
            r'expérience\s*:\s*(\d+)',
            r'experience\s*:\s*(\d+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            if matches:
                years = int(matches[0])
                return min(years / 10.0, 1.0)  # Normalisé sur 10 ans max
        
        return 0.0
    
    def _calculate_relevant_experience(self, content: str, job_requirements: Dict) -> float:
        """Calcule l'expérience pertinente"""
        job_title = job_requirements.get('title', '').lower()
        job_description = job_requirements.get('description', '').lower()
        
        # Mots-clés du poste
        job_keywords = set(job_title.split() + job_description.split())
        
        # Compter les occurrences dans le CV
        relevance_score = 0
        for keyword in job_keywords:
            if len(keyword) > 3:  # Ignorer les mots trop courts
                relevance_score += content.count(keyword)
        
        return min(relevance_score / 50.0, 1.0)  # Normalisé
    
    def _extract_education_level(self, content: str) -> float:
        """Extrait le niveau d'éducation"""
        education_levels = {
            'doctorat': 1.0,
            'phd': 1.0,
            'master': 0.8,
            'maîtrise': 0.8,
            'licence': 0.6,
            'bachelor': 0.6,
            'bts': 0.4,
            'dut': 0.4,
            'bac': 0.2,
            'high school': 0.2
        }
        
        max_level = 0
        for level, score in education_levels.items():
            if level in content:
                max_level = max(max_level, score)
        
        return max_level
    
    def _count_certifications(self, content: str) -> float:
        """Compte les certifications"""
        cert_keywords = ['certification', 'certificat', 'certified', 'aws', 'google', 'microsoft', 'oracle', 'cisco']
        count = sum(1 for keyword in cert_keywords if keyword in content)
        return min(count / 5.0, 1.0)  # Normalisé sur 5 certifications max
    
    def _assess_cv_quality(self, content: str) -> float:
        """Évalue la qualité du CV"""
        quality_score = 0.5  # Score de base
        
        # Longueur appropriée
        if 500 <= len(content) <= 2000:
            quality_score += 0.2
        
        # Structure (présence de sections)
        sections = ['expérience', 'formation', 'compétences', 'projet']
        section_count = sum(1 for section in sections if section in content.lower())
        quality_score += (section_count / len(sections)) * 0.3
        
        return min(quality_score, 1.0)
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> float:
        """Calcule la densité des mots-clés"""
        if not keywords or not content:
            return 0.0
        
        total_words = len(content.split())
        keyword_count = sum(content.count(keyword.strip()) for keyword in keywords if keyword.strip())
        
        return min(keyword_count / total_words * 100, 1.0) if total_words > 0 else 0.0
    
    def calculate_score(self, features: Dict[str, float]) -> float:
        """Calcule le score final basé sur les caractéristiques"""
        score = 0.0
        total_weight = 0.0
        
        for feature, value in features.items():
            if feature in self.weights:
                weight = self.weights[feature]
                score += value * weight
                total_weight += weight
        
        # Normalisation
        if total_weight > 0:
            score = score / total_weight
        
        # Application d'une fonction sigmoïde pour un score plus réaliste
        score = 1 / (1 + math.exp(-10 * (score - 0.5)))
        
        return min(max(score * 100, 0), 100)
    
    def get_score_category(self, score: float) -> Tuple[str, str]:
        """Détermine la catégorie du score"""
        if score >= 85:
            return "EXCELLENT", "#10B981"
        elif score >= 70:
            return "TRÈS BON", "#3B82F6"
        elif score >= 55:
            return "BON", "#06B6D4"
        elif score >= 40:
            return "MOYEN", "#F59E0B"
        else:
            return "FAIBLE", "#EF4444"
    
    def analyze_cvs(self, job_data: Dict, cv_files: List[Dict]) -> List[Dict]:
        """Analyse les CVs avec l'algorithme ML"""
        results = []
        
        for cv_file in cv_files:
            # Simulation du contenu du CV (en production, ceci viendrait du parsing PDF)
            cv_content = self._simulate_cv_content(cv_file['name'])
            
            # Extraction des caractéristiques
            features = self.extract_features(cv_content, job_data)
            
            # Calcul du score
            score = self.calculate_score(features)
            category, color = self.get_score_category(score)
            
            # Analyse détaillée
            analysis = self._generate_detailed_analysis(features, job_data)
            
            result = {
                'filename': cv_file['name'],
                'score': round(score, 1),
                'category': category,
                'color': color,
                'features': features,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
        
        # Tri intelligent basé sur le score et l'apprentissage
        results = self._intelligent_sort(results, job_data)
        
        # Sauvegarde pour l'apprentissage
        self._save_analysis_for_learning(job_data, results)
        
        return results
    
    def _simulate_cv_content(self, filename: str) -> str:
        """Simule le contenu d'un CV basé sur le nom de fichier"""
        # En production, ceci serait remplacé par un vrai parser PDF
        name = filename.replace('cv_', '').replace('.pdf', '').lower()
        
        # Contenu simulé basé sur le nom
        cv_templates = {
            'adam': """
            Adam Smith - Développeur Full Stack
            Expérience: 3 ans
            Compétences: Python, JavaScript, React, Node.js, MongoDB
            Formation: Master en Informatique
            Projets: Développement d'applications web, API REST
            """,
            'ali': """
            Ali Hassan - Data Scientist
            Expérience: 5 ans
            Compétences: Python, Machine Learning, TensorFlow, SQL, Pandas
            Formation: Doctorat en Data Science
            Certifications: AWS Certified, Google Cloud
            Projets: Modèles de prédiction, analyse de données
            """,
            'hafsa': """
            Hafsa Alami - Ingénieure IA
            Expérience: 4 ans
            Compétences: Python, Deep Learning, PyTorch, Computer Vision, NLP
            Formation: Master en Intelligence Artificielle
            Projets: Reconnaissance d'images, chatbots intelligents
            """,
            'hamza': """
            Hamza Benali - Développeur Backend
            Expérience: 2 ans
            Compétences: Java, Spring Boot, PostgreSQL, Docker
            Formation: Licence en Informatique
            Projets: Microservices, API REST
            """,
            'sophia': """
            Sophia Chen - Analyste de Données
            Expérience: 3 ans
            Compétences: R, Python, Tableau, SQL, Statistiques
            Formation: Master en Statistiques
            Projets: Tableaux de bord, analyses prédictives
            """,
            'yassine': """
            Yassine El Fassi - DevOps Engineer
            Expérience: 4 ans
            Compétences: AWS, Docker, Kubernetes, Jenkins, Linux
            Formation: Master en Systèmes Réseaux
            Certifications: AWS Certified DevOps
            Projets: CI/CD, infrastructure cloud
            """
        }
        
        return cv_templates.get(name, f"CV de {name} - Contenu générique")
    
    def _generate_detailed_analysis(self, features: Dict[str, float], job_data: Dict) -> Dict[str, Any]:
        """Génère une analyse détaillée"""
        strengths = []
        weaknesses = []
        recommendations = []
        
        # Analyse des forces
        if features.get('technical_skills', 0) > 0.7:
            strengths.append("Compétences techniques excellentes")
        if features.get('experience_years', 0) > 0.5:
            strengths.append("Expérience solide")
        if features.get('education_level', 0) > 0.7:
            strengths.append("Formation de haut niveau")
        
        # Analyse des faiblesses
        if features.get('technical_skills', 0) < 0.3:
            weaknesses.append("Compétences techniques limitées")
        if features.get('experience_years', 0) < 0.2:
            weaknesses.append("Expérience insuffisante")
        if features.get('cv_quality', 0) < 0.5:
            weaknesses.append("Qualité du CV à améliorer")
        
        # Recommandations
        if features.get('technical_skills', 0) < 0.5:
            recommendations.append("Formation recommandée en technologies requises")
        if features.get('certifications', 0) < 0.3:
            recommendations.append("Certifications professionnelles suggérées")
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'match_percentage': round(sum(features.values()) / len(features) * 100, 1)
        }
    
    def _intelligent_sort(self, results: List[Dict], job_data: Dict) -> List[Dict]:
        """Tri intelligent basé sur l'apprentissage"""
        # Tri principal par score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Ajustement basé sur l'historique
        for result in results:
            historical_bonus = self._get_historical_bonus(result['filename'], job_data)
            result['score'] = min(result['score'] + historical_bonus, 100)
        
        # Re-tri après ajustement
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results
    
    def _get_historical_bonus(self, filename: str, job_data: Dict) -> float:
        """Calcule un bonus basé sur l'historique"""
        bonus = 0.0
        
        # Recherche dans l'historique
        for analysis in self.history:
            if analysis.get('job_title') == job_data.get('title'):
                for result in analysis.get('results', []):
                    if result.get('filename') == filename:
                        # Bonus basé sur les performances passées
                        past_score = result.get('score', 0)
                        if past_score > 80:
                            bonus += 2.0
                        elif past_score > 60:
                            bonus += 1.0
        
        return min(bonus, 5.0)  # Bonus maximum de 5 points
    
    def _save_analysis_for_learning(self, job_data: Dict, results: List[Dict]):
        """Sauvegarde l'analyse pour l'apprentissage futur"""
        analysis_record = {
            'timestamp': datetime.now().isoformat(),
            'job_title': job_data.get('title'),
            'job_description': job_data.get('description'),
            'results': results,
            'total_cvs': len(results)
        }
        
        self.history.append(analysis_record)
        
        # Garder seulement les 100 dernières analyses
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        # Sauvegarde
        self.save_history()
        
        # Mise à jour du modèle (apprentissage)
        self._update_model_weights(results)
    
    def _update_model_weights(self, results: List[Dict]):
        """Met à jour les poids du modèle basé sur les résultats"""
        # Algorithme d'apprentissage simple
        for result in results:
            score = result['score'] / 100.0
            features = result['features']
            
            # Ajustement des poids basé sur la performance
            for feature, value in features.items():
                if feature in self.weights:
                    # Si le score est élevé et la feature aussi, augmenter le poids
                    if score > 0.7 and value > 0.5:
                        self.weights[feature] += self.learning_rate * 0.01
                    # Si le score est faible mais la feature élevée, diminuer le poids
                    elif score < 0.4 and value > 0.5:
                        self.weights[feature] -= self.learning_rate * 0.01
        
        # Normalisation des poids
        total_weight = sum(self.weights.values())
        if total_weight > 0:
            for key in self.weights:
                self.weights[key] = self.weights[key] / total_weight
        
        # Sauvegarde du modèle mis à jour
        self.save_model()

# Instance globale
ml_analyzer = AdvancedMLAnalyzer()

def analyze_cvs_advanced(job_data: Dict, cv_files: List[Dict]) -> List[Dict]:
    """Fonction principale d'analyse"""
    return ml_analyzer.analyze_cvs(job_data, cv_files)

if __name__ == "__main__":
    # Test de l'analyseur
    job_data = {
        'title': 'Data Scientist',
        'description': 'Recherche d\'un Data Scientist avec expérience en Python, machine learning, et analyse de données.',
        'skills': 'Python, Machine Learning, SQL, Pandas, Scikit-learn'
    }
    
    cv_files = [
        {'name': 'cv_Adam.pdf'},
        {'name': 'cv_Ali.pdf'},
        {'name': 'cv_Hafsa.pdf'},
        {'name': 'cv_Hamza.pdf'},
        {'name': 'cv_Sophia.pdf'},
        {'name': 'cv_Yassine.pdf'}
    ]
    
    results = analyze_cvs_advanced(job_data, cv_files)
    
    print("🎯 Résultats de l'analyse ML avancée:")
    for result in results:
        print(f"📄 {result['filename']}: {result['score']}% - {result['category']}")
