#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur de CV avancé avec Machine Learning
Classification intelligente des CVs basée sur l'offre d'emploi
"""

import re
import json
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter
import numpy as np

@dataclass
class JobOffer:
    title: str
    description: str
    skills: List[str]
    experience_level: str
    requirements: List[str]

@dataclass
class CVAnalysis:
    filename: str
    score: float
    rank: int
    skills_match: float
    experience_match: float
    education_score: float
    text_similarity: float
    ml_score: float
    status: str
    recommendations: List[str]
    extracted_skills: List[str]
    experience_years: int
    education_level: str

class AdvancedMLAnalyzer:
    def __init__(self):
        # Base de données de compétences techniques
        self.technical_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn'],
            'web_dev': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin'],
            'ai_ml': ['artificial intelligence', 'neural networks', 'nlp', 'computer vision', 'reinforcement learning'],
            'devops': ['ci/cd', 'git', 'jenkins', 'gitlab', 'github actions', 'ansible', 'chef', 'puppet']
        }
        
        # Mots-clés d'expérience
        self.experience_keywords = {
            'junior': ['junior', 'entry', 'débutant', 'stagiaire', '0-2', '1-2', '2 ans'],
            'intermediate': ['intermediate', 'mid', 'intermédiaire', '2-5', '3-5', '4 ans', '5 ans'],
            'senior': ['senior', 'lead', 'principal', '5-10', '6-10', '8 ans', '10 ans'],
            'expert': ['expert', 'architect', 'director', '10+', '15+', '20+', 'chef']
        }
        
        # Niveaux d'éducation
        self.education_levels = {
            'doctorat': ['phd', 'doctorat', 'doctorate', 'ph.d', 'thèse'],
            'master': ['master', 'mba', 'm.s', 'm.a', 'm2', 'm1', 'maîtrise'],
            'licence': ['licence', 'bachelor', 'b.s', 'b.a', 'l3', 'l2', 'l1'],
            'bts': ['bts', 'dut', 'associate', 'technicien', 'technique'],
            'bac': ['bac', 'high school', 'lycée', 'terminal']
        }

    def analyze_cv_content(self, filename: str, content: str = None) -> Dict:
        """Analyse le contenu d'un CV et extrait les informations"""
        # Si pas de contenu, simuler basé sur le nom du fichier
        if not content:
            content = self._simulate_cv_content(filename)
        
        # Extraire les informations
        skills = self._extract_skills(content)
        experience = self._extract_experience(content)
        education = self._extract_education(content)
        
        return {
            'skills': skills,
            'experience_years': experience,
            'education_level': education,
            'content': content
        }

    def _simulate_cv_content(self, filename: str) -> str:
        """Simule le contenu d'un CV basé sur le nom du fichier"""
        filename_lower = filename.lower()
        
        # Simulation basée sur le nom du fichier
        if 'senior' in filename_lower or 'lead' in filename_lower:
            return f"""
            Candidat Senior - {filename}
            Expérience: 8+ ans
            Formation: Master en Informatique
            Compétences: Python, Machine Learning, TensorFlow, AWS, Docker, Kubernetes
            Projets: Développement d'algorithmes ML, Architecture cloud, Leadership d'équipe
            """
        elif 'ml' in filename_lower or 'machine' in filename_lower:
            return f"""
            Machine Learning Engineer - {filename}
            Expérience: 4 ans
            Formation: Master en Data Science
            Compétences: Python, Scikit-learn, Pandas, NumPy, Matplotlib, SQL
            Projets: Modèles prédictifs, Analyse de données, Visualisation
            """
        elif 'data' in filename_lower or 'analyst' in filename_lower:
            return f"""
            Data Analyst - {filename}
            Expérience: 2 ans
            Formation: Licence en Statistiques
            Compétences: Python, Pandas, Excel, SQL, Tableau, Power BI
            Projets: Tableaux de bord, Rapports d'analyse, KPI
            """
        elif 'junior' in filename_lower or 'dev' in filename_lower:
            return f"""
            Développeur Junior - {filename}
            Expérience: 1 an
            Formation: BTS Informatique
            Compétences: JavaScript, React, HTML, CSS, Node.js
            Projets: Applications web, Sites e-commerce
            """
        else:
            # Analyse générique
            skills = []
            if 'python' in filename_lower:
                skills.extend(['Python', 'Pandas', 'NumPy'])
            if 'java' in filename_lower:
                skills.extend(['Java', 'Spring', 'Hibernate'])
            if 'web' in filename_lower:
                skills.extend(['HTML', 'CSS', 'JavaScript', 'React'])
            if 'data' in filename_lower:
                skills.extend(['Data Analysis', 'SQL', 'Excel'])
            
            return f"""
            Candidat - {filename}
            Expérience: 3 ans
            Formation: Licence
            Compétences: {', '.join(skills) if skills else 'Diverses compétences techniques'}
            Projets: Développement logiciel, Analyse de données
            """

    def _extract_skills(self, content: str) -> List[str]:
        """Extrait les compétences techniques du contenu"""
        content_lower = content.lower()
        found_skills = []
        
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if skill in content_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))

    def _extract_experience(self, content: str) -> int:
        """Extrait le nombre d'années d'expérience"""
        content_lower = content.lower()
        
        # Recherche de patterns d'expérience
        patterns = [
            r'(\d+)\s*ans?\s*d\'expérience',
            r'expérience\s*:\s*(\d+)',
            r'(\d+)\s*années?',
            r'(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content_lower)
            if match:
                return int(match.group(1))
        
        # Estimation basée sur les mots-clés
        for level, keywords in self.experience_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                if level == 'junior':
                    return 1
                elif level == 'intermediate':
                    return 3
                elif level == 'senior':
                    return 7
                elif level == 'expert':
                    return 12
        
        return 2  # Valeur par défaut

    def _extract_education(self, content: str) -> str:
        """Extrait le niveau d'éducation"""
        content_lower = content.lower()
        
        for level, keywords in self.education_levels.items():
            if any(keyword in content_lower for keyword in keywords):
                return level
        
        return 'licence'  # Valeur par défaut

    def calculate_skill_match_score(self, job_skills: List[str], cv_skills: List[str]) -> float:
        """Calcule le score de correspondance des compétences"""
        if not job_skills or not cv_skills:
            return 0.0
        
        job_skills_lower = [skill.lower().strip() for skill in job_skills]
        cv_skills_lower = [skill.lower().strip() for skill in cv_skills]
        
        # Correspondance exacte
        exact_matches = sum(1 for skill in job_skills_lower if skill in cv_skills_lower)
        
        # Correspondance partielle (mots-clés dans les compétences)
        partial_matches = 0
        for job_skill in job_skills_lower:
            for cv_skill in cv_skills_lower:
                if job_skill in cv_skill or cv_skill in job_skill:
                    partial_matches += 0.5
                    break
        
        total_matches = exact_matches + partial_matches
        return min(100.0, (total_matches / len(job_skills)) * 100)

    def calculate_experience_score(self, job_experience: str, cv_experience: int) -> float:
        """Calcule le score d'expérience"""
        experience_ranges = {
            'junior': (0, 2, 1),
            'intermediate': (2, 5, 3),
            'senior': (5, 10, 7),
            'expert': (10, 20, 15)
        }
        
        min_exp, max_exp, ideal_exp = experience_ranges.get(job_experience, (2, 5, 3))
        
        if cv_experience < min_exp:
            return max(0, (cv_experience / min_exp) * 50)
        elif cv_experience <= max_exp:
            return 50 + ((cv_experience - min_exp) / (max_exp - min_exp)) * 40
        else:
            return min(100, 90 + (cv_experience - max_exp) * 2)

    def calculate_education_score(self, education_level: str) -> float:
        """Calcule le score d'éducation"""
        scores = {
            'doctorat': 100,
            'master': 85,
            'licence': 70,
            'bts': 60,
            'bac': 40
        }
        return scores.get(education_level, 30)

    def calculate_text_similarity(self, job_description: str, cv_content: str) -> float:
        """Calcule la similarité textuelle entre l'offre et le CV"""
        job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
        cv_words = set(re.findall(r'\b\w+\b', cv_content.lower()))
        
        if not job_words:
            return 0.0
        
        common_words = job_words.intersection(cv_words)
        return (len(common_words) / len(job_words)) * 100

    def calculate_ml_score(self, job_offer: JobOffer, cv_analysis: Dict) -> float:
        """Calcule un score ML avancé basé sur plusieurs facteurs"""
        # Poids des différents facteurs
        weights = {
            'skills': 0.35,
            'experience': 0.25,
            'education': 0.15,
            'text_similarity': 0.15,
            'ml_bonus': 0.10
        }
        
        # Score des compétences
        skill_score = self.calculate_skill_match_score(
            job_offer.skills, 
            cv_analysis['skills']
        )
        
        # Score d'expérience
        experience_score = self.calculate_experience_score(
            job_offer.experience_level,
            cv_analysis['experience_years']
        )
        
        # Score d'éducation
        education_score = self.calculate_education_score(
            cv_analysis['education_level']
        )
        
        # Similarité textuelle
        text_similarity = self.calculate_text_similarity(
            job_offer.description,
            cv_analysis['content']
        )
        
        # Bonus ML (simulation d'analyse avancée)
        ml_bonus = self._calculate_ml_bonus(job_offer, cv_analysis)
        
        # Score final pondéré
        final_score = (
            skill_score * weights['skills'] +
            experience_score * weights['experience'] +
            education_score * weights['education'] +
            text_similarity * weights['text_similarity'] +
            ml_bonus * weights['ml_bonus']
        )
        
        return min(100.0, final_score)

    def _calculate_ml_bonus(self, job_offer: JobOffer, cv_analysis: Dict) -> float:
        """Calcule un bonus basé sur l'analyse ML avancée"""
        bonus = 0
        
        # Bonus pour les compétences rares et demandées
        rare_skills = ['kubernetes', 'tensorflow', 'pytorch', 'aws', 'docker']
        cv_skills_lower = [skill.lower() for skill in cv_analysis['skills']]
        
        for skill in rare_skills:
            if skill in cv_skills_lower:
                bonus += 5
        
        # Bonus pour l'expérience dans des domaines spécifiques
        if 'machine learning' in job_offer.description.lower():
            if any(ml_skill in cv_skills_lower for ml_skill in ['tensorflow', 'pytorch', 'scikit-learn']):
                bonus += 10
        
        # Bonus pour l'éducation avancée
        if cv_analysis['education_level'] in ['master', 'doctorat']:
            bonus += 5
        
        return min(20, bonus)  # Maximum 20 points de bonus

    def generate_recommendations(self, score: float, cv_analysis: Dict) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        
        if score >= 85:
            recommendations.append("✅ Excellent candidat, fortement recommandé")
            recommendations.append("🎯 Candidat prioritaire pour l'entretien")
        elif score >= 70:
            recommendations.append("✅ Bon candidat, recommandé avec quelques réserves")
            recommendations.append("📋 Vérifier l'expérience pratique")
        elif score >= 50:
            recommendations.append("⚠️ Candidat acceptable, nécessite une évaluation approfondie")
            recommendations.append("🔍 Considérer un entretien technique")
        else:
            recommendations.append("❌ Candidat non recommandé pour ce poste")
            recommendations.append("💡 Considérer pour d'autres postes")
        
        # Recommandations spécifiques
        if len(cv_analysis['skills']) < 3:
            recommendations.append("📚 Candidat manque de compétences techniques")
        
        if cv_analysis['experience_years'] < 2:
            recommendations.append("👶 Candidat junior, nécessite de la formation")
        
        return recommendations

    def analyze_and_rank_cvs(self, job_offer: JobOffer, cv_files: List[str]) -> List[CVAnalysis]:
        """Analyse et classe les CVs par ordre de pertinence"""
        results = []
        
        for i, cv_file in enumerate(cv_files):
            # Analyser le CV
            cv_analysis = self.analyze_cv_content(cv_file)
            
            # Calculer le score ML
            ml_score = self.calculate_ml_score(job_offer, cv_analysis)
            
            # Calculer les scores individuels
            skill_score = self.calculate_skill_match_score(job_offer.skills, cv_analysis['skills'])
            experience_score = self.calculate_experience_score(job_offer.experience_level, cv_analysis['experience_years'])
            education_score = self.calculate_education_score(cv_analysis['education_level'])
            text_similarity = self.calculate_text_similarity(job_offer.description, cv_analysis['content'])
            
            # Déterminer le statut
            if ml_score >= 85:
                status = "Excellent"
            elif ml_score >= 70:
                status = "Très bon"
            elif ml_score >= 50:
                status = "Bon"
            else:
                status = "À améliorer"
            
            # Générer les recommandations
            recommendations = self.generate_recommendations(ml_score, cv_analysis)
            
            # Créer l'objet d'analyse
            analysis = CVAnalysis(
                filename=cv_file,
                score=round(ml_score, 1),
                rank=0,  # Sera mis à jour après le tri
                skills_match=round(skill_score, 1),
                experience_match=round(experience_score, 1),
                education_score=round(education_score, 1),
                text_similarity=round(text_similarity, 1),
                ml_score=round(ml_score, 1),
                status=status,
                recommendations=recommendations,
                extracted_skills=cv_analysis['skills'],
                experience_years=cv_analysis['experience_years'],
                education_level=cv_analysis['education_level']
            )
            
            results.append(analysis)
        
        # Trier par score décroissant et assigner les rangs
        results.sort(key=lambda x: x.score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results

def main():
    """Fonction de test"""
    analyzer = AdvancedMLAnalyzer()
    
    # Exemple d'offre d'emploi
    job_offer = JobOffer(
        title="Data Scientist Senior",
        description="Recherche un Data Scientist expérimenté pour développer des modèles de machine learning et analyser de grandes quantités de données.",
        skills=["python", "machine learning", "tensorflow", "sql", "aws"],
        experience_level="senior",
        requirements=["Expérience en ML", "Connaissance de Python", "Expérience cloud"]
    )
    
    # Exemple de CVs
    cv_files = [
        "cv_senior_ml_engineer.pdf",
        "cv_junior_data_analyst.pdf",
        "cv_ml_specialist.pdf",
        "cv_data_scientist.pdf"
    ]
    
    # Analyser et classer
    results = analyzer.analyze_and_rank_cvs(job_offer, cv_files)
    
    # Afficher les résultats
    print("🏆 CLASSEMENT DES CVs")
    print("=" * 50)
    
    for result in results:
        print(f"\n📊 Rang #{result.rank} - {result.filename}")
        print(f"   Score global: {result.score}%")
        print(f"   Statut: {result.status}")
        print(f"   Compétences: {result.skills_match}%")
        print(f"   Expérience: {result.experience_match}%")
        print(f"   Éducation: {result.education_score}%")
        print(f"   Similarité: {result.text_similarity}%")
        print(f"   Recommandations:")
        for rec in result.recommendations:
            print(f"     - {rec}")

if __name__ == "__main__":
    main()

