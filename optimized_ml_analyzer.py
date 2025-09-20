#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - ANALYSEUR ML ULTRA-OPTIMISÉ
Ministère de l'Économie et des Finances
Version: 2.0 - Machine Learning haute performance
"""

import numpy as np
import pandas as pd
import re
import json
import time
from typing import Dict, List, Tuple, Any, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache
import multiprocessing as mp
from dataclasses import dataclass
import hashlib

@dataclass
class CVProfile:
    """Structure de données optimisée pour un profil de CV"""
    name: str
    skills: List[str]
    experience_years: float
    education: str
    raw_text: str
    processed_text: Optional[str] = None
    skill_vector: Optional[np.ndarray] = None
    hash_id: Optional[str] = None

class OptimizedMLAnalyzer:
    """Analyseur ML ultra-optimisé avec vectorisation et parallélisation"""
    
    def __init__(self, n_workers: int = None):
        self.n_workers = n_workers or min(8, mp.cpu_count())
        
        # Vocabulaire de compétences optimisé avec poids
        self.skill_weights = {
            # Langages de programmation (poids élevé)
            'python': 1.5, 'java': 1.3, 'javascript': 1.3, 'typescript': 1.2,
            'c++': 1.2, 'c#': 1.2, 'php': 1.1, 'ruby': 1.1, 'go': 1.2, 'rust': 1.2,
            
            # Frameworks web (poids moyen-élevé)
            'react': 1.4, 'angular': 1.3, 'vue': 1.2, 'nodejs': 1.3,
            'django': 1.3, 'flask': 1.2, 'spring': 1.3, 'laravel': 1.2,
            
            # Bases de données (poids moyen-élevé)
            'mysql': 1.2, 'postgresql': 1.3, 'mongodb': 1.2, 'redis': 1.1,
            'elasticsearch': 1.2, 'oracle': 1.1, 'sqlite': 1.0,
            
            # Cloud & DevOps (poids très élevé)
            'aws': 1.6, 'azure': 1.5, 'gcp': 1.4, 'docker': 1.4,
            'kubernetes': 1.5, 'jenkins': 1.2, 'git': 1.1, 'terraform': 1.3,
            
            # Machine Learning & Data Science (poids maximal)
            'machine learning': 2.0, 'deep learning': 1.9, 'ai': 1.8,
            'tensorflow': 1.7, 'pytorch': 1.7, 'scikit-learn': 1.5,
            'pandas': 1.4, 'numpy': 1.3, 'matplotlib': 1.2, 'seaborn': 1.2,
            'jupyter': 1.1, 'spark': 1.4, 'hadoop': 1.3,
            
            # Autres technologies importantes
            'linux': 1.2, 'windows': 1.0, 'macos': 1.0,
            'rest api': 1.3, 'graphql': 1.2, 'microservices': 1.4
        }
        
        # Matrice de compétences pré-calculée pour la vectorisation
        self.skill_names = list(self.skill_weights.keys())
        self.skill_weights_vector = np.array([self.skill_weights[skill] for skill in self.skill_names])
        
        # Cache LRU pour les résultats
        self._cache_size = 1000
        self._init_caches()
        
        # Patterns regex pré-compilés pour les performances
        self._compile_patterns()
        
        # Matrice de similarité pré-calculée
        self._similarity_matrix = None
        self._build_similarity_matrix()
    
    def _init_caches(self):
        """Initialise les caches LRU"""
        self.text_processing_cache = {}
        self.skill_extraction_cache = {}
        self.experience_cache = {}
        self.education_cache = {}
    
    def _compile_patterns(self):
        """Pré-compile les patterns regex pour les performances"""
        self.experience_patterns = [
            re.compile(r'(\d+)\s*ans?\s+d\'?expérience', re.IGNORECASE),
            re.compile(r'(\d+)\s*years?\s+of\s+experience', re.IGNORECASE),
            re.compile(r'expérience\s*:\s*(\d+)', re.IGNORECASE),
            re.compile(r'experience\s*:\s*(\d+)', re.IGNORECASE),
            re.compile(r'(\d+)\s*années?\s+de\s+', re.IGNORECASE),
            re.compile(r'(\d+)\s*years?\s+in\s+', re.IGNORECASE)
        ]
        
        self.date_pattern = re.compile(r'(19|20)\d{2}')
        self.text_clean_pattern = re.compile(r'[^a-zA-Z\s]')
        
        # Patterns d'éducation
        self.education_patterns = {
            'doctorat': re.compile(r'\b(phd|doctorat|doctorate|thèse)\b', re.IGNORECASE),
            'master': re.compile(r'\b(master|mba|msc|ma|m2|m1)\b', re.IGNORECASE),
            'licence': re.compile(r'\b(licence|bachelor|bsc|ba|l3|l2|l1)\b', re.IGNORECASE),
            'bts': re.compile(r'\b(bts|dut|deug)\b', re.IGNORECASE),
            'bac': re.compile(r'\b(bac|baccalauréat|high school|lycée)\b', re.IGNORECASE)
        }
    
    def _build_similarity_matrix(self):
        """Construit une matrice de similarité entre compétences"""
        n_skills = len(self.skill_names)
        self._similarity_matrix = np.eye(n_skills)
        
        # Groupes de compétences similaires
        similarity_groups = [
            ['python', 'pandas', 'numpy', 'scikit-learn', 'matplotlib'],
            ['machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch'],
            ['react', 'javascript', 'typescript', 'nodejs'],
            ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            ['mysql', 'postgresql', 'mongodb', 'redis']
        ]
        
        for group in similarity_groups:
            indices = []
            for skill in group:
                if skill in self.skill_names:
                    indices.append(self.skill_names.index(skill))
            
            # Définir la similarité entre les compétences du même groupe
            for i in indices:
                for j in indices:
                    if i != j:
                        self._similarity_matrix[i, j] = 0.7
    
    @lru_cache(maxsize=1000)
    def _process_text(self, text: str) -> str:
        """Traite et nettoie le texte avec cache LRU"""
        if not text:
            return ""
        
        # Convertir en minuscules et nettoyer
        processed = text.lower()
        processed = self.text_clean_pattern.sub(' ', processed)
        
        # Supprimer les mots vides et normaliser les espaces
        words = processed.split()
        words = [word for word in words if len(word) > 2]
        
        return ' '.join(words)
    
    def _extract_skills_vectorized(self, text: str) -> Tuple[List[str], np.ndarray]:
        """Extraction vectorisée des compétences"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash in self.skill_extraction_cache:
            return self.skill_extraction_cache[text_hash]
        
        processed_text = self._process_text(text)
        
        # Vectorisation : vérifier toutes les compétences en une fois
        skill_vector = np.zeros(len(self.skill_names))
        found_skills = []
        
        for i, skill in enumerate(self.skill_names):
            if skill in processed_text:
                skill_vector[i] = self.skill_weights[skill]
                found_skills.append(skill)
        
        result = (found_skills, skill_vector)
        self.skill_extraction_cache[text_hash] = result
        
        return result
    
    @lru_cache(maxsize=500)
    def _extract_experience_years(self, text: str) -> float:
        """Extraction optimisée des années d'expérience"""
        years = []
        
        # Utiliser les patterns pré-compilés
        for pattern in self.experience_patterns:
            matches = pattern.findall(text)
            years.extend([int(match) for match in matches])
        
        # Estimation à partir des dates si aucun pattern trouvé
        if not years:
            date_matches = self.date_pattern.findall(text)
            if len(date_matches) >= 2:
                years_found = [int(year) for year in date_matches]
                if years_found:
                    experience = max(years_found) - min(years_found)
                    if experience > 0:
                        years.append(experience)
        
        return max(years) if years else 0.0
    
    @lru_cache(maxsize=500)
    def _extract_education_level(self, text: str) -> str:
        """Extraction optimisée du niveau d'éducation"""
        for level, pattern in self.education_patterns.items():
            if pattern.search(text):
                return level
        return 'inconnu'
    
    def _calculate_skill_similarity_matrix(self, job_skills: List[str], cv_skills_vector: np.ndarray) -> float:
        """Calcule la similarité des compétences avec matrice de similarité"""
        if not job_skills:
            return 0.0
        
        # Créer un vecteur pour les compétences demandées
        job_vector = np.zeros(len(self.skill_names))
        for skill in job_skills:
            skill_lower = skill.lower().strip()
            if skill_lower in self.skill_names:
                idx = self.skill_names.index(skill_lower)
                job_vector[idx] = self.skill_weights[skill_lower]
        
        if np.sum(job_vector) == 0:
            return 0.0
        
        # Calculer la similarité avec la matrice de similarité
        similarity_scores = np.dot(cv_skills_vector, np.dot(self._similarity_matrix, job_vector))
        max_possible_score = np.sum(job_vector)
        
        return min((similarity_scores / max_possible_score) * 100, 100) if max_possible_score > 0 else 0
    
    def _calculate_experience_score_vectorized(self, job_experience: str, cv_experiences: np.ndarray) -> np.ndarray:
        """Calcul vectorisé des scores d'expérience"""
        experience_mapping = {
            'junior': (0, 2),
            'intermediate': (2, 5),
            'senior': (5, 10),
            'expert': (10, 20)
        }
        
        if job_experience not in experience_mapping:
            return np.full(len(cv_experiences), 50.0)
        
        min_exp, max_exp = experience_mapping[job_experience]
        
        # Vectorisation avec numpy
        scores = np.where(
            cv_experiences < min_exp,
            np.maximum(0, cv_experiences / min_exp * 50),
            np.where(
                cv_experiences <= max_exp,
                50 + (cv_experiences - min_exp) / (max_exp - min_exp) * 40,
                np.minimum(100, 90 + (cv_experiences - max_exp) * 2)
            )
        )
        
        return scores
    
    def _calculate_education_scores_vectorized(self, educations: List[str]) -> np.ndarray:
        """Calcul vectorisé des scores d'éducation"""
        education_scores = {
            'doctorat': 100, 'master': 85, 'licence': 70,
            'bts': 60, 'bac': 40, 'inconnu': 30
        }
        
        return np.array([education_scores.get(edu, 30) for edu in educations])
    
    def analyze_cv_batch(self, cv_profiles: List[CVProfile], job_description: str, 
                        job_skills: List[str] = None, job_experience: str = None) -> List[Dict[str, Any]]:
        """Analyse en lot optimisée avec parallélisation"""
        
        if not cv_profiles:
            return []
        
        start_time = time.time()
        
        # Étape 1: Traitement parallèle de l'extraction des données
        with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
            # Extraire les compétences en parallèle
            skill_futures = {
                executor.submit(self._extract_skills_vectorized, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Extraire l'expérience en parallèle
            exp_futures = {
                executor.submit(self._extract_experience_years, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Extraire l'éducation en parallèle
            edu_futures = {
                executor.submit(self._extract_education_level, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Collecter les résultats
            skills_data = {}
            for future in skill_futures:
                idx = skill_futures[future]
                skills_data[idx] = future.result()
            
            experiences_data = {}
            for future in exp_futures:
                idx = exp_futures[future]
                experiences_data[idx] = future.result()
            
            educations_data = {}
            for future in edu_futures:
                idx = edu_futures[future]
                educations_data[idx] = future.result()
        
        # Étape 2: Calculs vectorisés
        cv_experiences = np.array([experiences_data[i] for i in range(len(cv_profiles))])
        cv_educations = [educations_data[i] for i in range(len(cv_profiles))]
        cv_skills_vectors = np.array([skills_data[i][1] for i in range(len(cv_profiles))])
        
        # Calculs vectorisés des scores
        experience_scores = self._calculate_experience_score_vectorized(job_experience or 'intermediate', cv_experiences)
        education_scores = self._calculate_education_scores_vectorized(cv_educations)
        
        # Étape 3: Calcul des scores finaux
        results = []
        for i, cv in enumerate(cv_profiles):
            found_skills, skill_vector = skills_data[i]
            
            # Scores individuels
            skill_score = self._calculate_skill_similarity_matrix(job_skills or [], skill_vector)
            experience_score = experience_scores[i]
            education_score = education_scores[i]
            
            # Similarité textuelle (optimisée)
            text_similarity = self._calculate_text_similarity_fast(job_description, cv.raw_text)
            
            # Score ML basé sur les features
            ml_score = self._calculate_ml_score_fast(skill_vector, cv_experiences[i], education_score)
            
            # Score final pondéré
            final_score = (
                skill_score * 0.35 +
                experience_score * 0.25 +
                education_score * 0.15 +
                text_similarity * 0.15 +
                ml_score * 0.10
            )
            
            # Déterminer le statut
            if final_score >= 85:
                status, status_class = "Excellent", "excellent"
            elif final_score >= 70:
                status, status_class = "Très bon", "good"
            elif final_score >= 50:
                status, status_class = "Bon", "average"
            else:
                status, status_class = "À améliorer", "poor"
            
            results.append({
                'name': cv.name,
                'final_score': round(final_score, 1),
                'status': status,
                'status_class': status_class,
                'breakdown': {
                    'skill_score': round(skill_score, 1),
                    'experience_score': round(experience_score, 1),
                    'education_score': round(education_score, 1),
                    'text_similarity': round(text_similarity, 1),
                    'ml_score': round(ml_score, 1)
                },
                'extracted_info': {
                    'skills': found_skills,
                    'experience_years': cv_experiences[i],
                    'education': cv_educations[i]
                },
                'processing_time': time.time() - start_time
            })
        
        # Trier par score décroissant
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results
    
    @lru_cache(maxsize=200)
    def _calculate_text_similarity_fast(self, text1: str, text2: str) -> float:
        """Calcul rapide de similarité textuelle"""
        if not text1 or not text2:
            return 0.0
        
        # Utiliser des sets pour l'intersection rapide
        words1 = set(self._process_text(text1).split())
        words2 = set(self._process_text(text2).split())
        
        if not words1:
            return 0.0
        
        intersection = len(words1 & words2)
        return min((intersection / len(words1)) * 100, 100)
    
    def _calculate_ml_score_fast(self, skill_vector: np.ndarray, experience: float, education_score: float) -> float:
        """Calcul rapide du score ML"""
        # Score basé sur la densité des compétences
        skill_density = np.sum(skill_vector) / len(skill_vector) * 100
        
        # Score basé sur l'expérience (normalisé)
        exp_score = min(experience * 5, 50)
        
        # Score composite
        composite_score = (skill_density * 0.5 + exp_score * 0.3 + education_score * 0.2)
        
        return min(composite_score, 100)
    
    def analyze_single_cv(self, cv_text: str, cv_name: str, job_description: str, 
                         job_skills: List[str] = None, job_experience: str = None) -> Dict[str, Any]:
        """Analyse rapide d'un CV unique"""
        cv_profile = CVProfile(
            name=cv_name,
            skills=[],
            experience_years=0,
            education='',
            raw_text=cv_text
        )
        
        results = self.analyze_cv_batch([cv_profile], job_description, job_skills, job_experience)
        return results[0] if results else {}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Statistiques de performance du cache"""
        return {
            'cache_sizes': {
                'text_processing': len(self.text_processing_cache),
                'skill_extraction': len(self.skill_extraction_cache),
                'experience': len(self.experience_cache),
                'education': len(self.education_cache)
            },
            'skill_vocabulary_size': len(self.skill_names),
            'similarity_matrix_shape': self._similarity_matrix.shape if self._similarity_matrix is not None else None,
            'workers_count': self.n_workers
        }

# Fonction utilitaire pour créer des profils de CV de test
def create_test_cv_profiles() -> List[CVProfile]:
    """Crée des profils de CV de test pour les benchmarks"""
    profiles = [
        CVProfile(
            name="CV_Senior_Data_Scientist.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Data Scientist Senior avec 8 ans d'expérience en Python, Machine Learning, et Deep Learning.
            Expert en TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, AWS, Docker, Kubernetes.
            Doctorat en Data Science de l'École Polytechnique.
            Projets: Classification d'images, NLP, systèmes de recommandation, MLOps."""
        ),
        CVProfile(
            name="CV_ML_Engineer.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Ingénieur Machine Learning avec 5 ans d'expérience en développement de modèles.
            Compétences: Python, Scikit-learn, Pandas, NumPy, SQL, Git, Jenkins.
            Master en Intelligence Artificielle. Expérience en déploiement de modèles en production."""
        ),
        CVProfile(
            name="CV_Data_Analyst.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Analyste de données avec 3 ans d'expérience en analyse statistique.
            Maîtrise de Python, Pandas, Matplotlib, SQL, Excel, Tableau.
            Licence en Statistiques. Spécialisé dans la visualisation de données."""
        ),
        CVProfile(
            name="CV_Junior_Developer.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Développeur Junior avec 1 an d'expérience en développement web.
            Technologies: JavaScript, React, HTML, CSS, Node.js.
            BTS en Développement Web. Stage de 6 mois en entreprise."""
        )
    ]
    
    return profiles

def benchmark_analyzer():
    """Benchmark de performance de l'analyseur"""
    print("🚀 BENCHMARK DE L'ANALYSEUR ML OPTIMISÉ")
    print("=" * 50)
    
    try:
        analyzer = OptimizedMLAnalyzer()
        cv_profiles = create_test_cv_profiles()
        
        job_description = """Nous recherchons un Data Scientist senior pour rejoindre notre équipe.
        Compétences requises: Python, Machine Learning, Deep Learning, TensorFlow, PyTorch.
        Expérience: 5+ ans. Master ou PhD en Data Science."""
        
        job_skills = ['python', 'machine learning', 'tensorflow', 'pytorch', 'deep learning']
        
        # Benchmark
        start_time = time.time()
        results = analyzer.analyze_cv_batch(cv_profiles, job_description, job_skills, 'senior')
        end_time = time.time()
        
        print(f"⏱️  Temps d'analyse: {end_time - start_time:.3f} secondes")
        print(f"📊 CVs analysés: {len(results)}")
        print(f"⚡ Vitesse: {len(results)/(end_time - start_time):.1f} CVs/seconde")
        print()
        
        for result in results:
            print(f"📄 {result['name']}: {result['final_score']}% ({result['status']})")
        
        print()
        stats = analyzer.get_performance_stats()
        print("📈 Statistiques de performance:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Erreur lors du benchmark: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    benchmark_analyzer()

🏛️ TALENTSCOPE - ANALYSEUR ML ULTRA-OPTIMISÉ
Ministère de l'Économie et des Finances
Version: 2.0 - Machine Learning haute performance
"""

import numpy as np
import pandas as pd
import re
import json
import time
from typing import Dict, List, Tuple, Any, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache
import multiprocessing as mp
from dataclasses import dataclass
import hashlib

@dataclass
class CVProfile:
    """Structure de données optimisée pour un profil de CV"""
    name: str
    skills: List[str]
    experience_years: float
    education: str
    raw_text: str
    processed_text: Optional[str] = None
    skill_vector: Optional[np.ndarray] = None
    hash_id: Optional[str] = None

class OptimizedMLAnalyzer:
    """Analyseur ML ultra-optimisé avec vectorisation et parallélisation"""
    
    def __init__(self, n_workers: int = None):
        self.n_workers = n_workers or min(8, mp.cpu_count())
        
        # Vocabulaire de compétences optimisé avec poids
        self.skill_weights = {
            # Langages de programmation (poids élevé)
            'python': 1.5, 'java': 1.3, 'javascript': 1.3, 'typescript': 1.2,
            'c++': 1.2, 'c#': 1.2, 'php': 1.1, 'ruby': 1.1, 'go': 1.2, 'rust': 1.2,
            
            # Frameworks web (poids moyen-élevé)
            'react': 1.4, 'angular': 1.3, 'vue': 1.2, 'nodejs': 1.3,
            'django': 1.3, 'flask': 1.2, 'spring': 1.3, 'laravel': 1.2,
            
            # Bases de données (poids moyen-élevé)
            'mysql': 1.2, 'postgresql': 1.3, 'mongodb': 1.2, 'redis': 1.1,
            'elasticsearch': 1.2, 'oracle': 1.1, 'sqlite': 1.0,
            
            # Cloud & DevOps (poids très élevé)
            'aws': 1.6, 'azure': 1.5, 'gcp': 1.4, 'docker': 1.4,
            'kubernetes': 1.5, 'jenkins': 1.2, 'git': 1.1, 'terraform': 1.3,
            
            # Machine Learning & Data Science (poids maximal)
            'machine learning': 2.0, 'deep learning': 1.9, 'ai': 1.8,
            'tensorflow': 1.7, 'pytorch': 1.7, 'scikit-learn': 1.5,
            'pandas': 1.4, 'numpy': 1.3, 'matplotlib': 1.2, 'seaborn': 1.2,
            'jupyter': 1.1, 'spark': 1.4, 'hadoop': 1.3,
            
            # Autres technologies importantes
            'linux': 1.2, 'windows': 1.0, 'macos': 1.0,
            'rest api': 1.3, 'graphql': 1.2, 'microservices': 1.4
        }
        
        # Matrice de compétences pré-calculée pour la vectorisation
        self.skill_names = list(self.skill_weights.keys())
        self.skill_weights_vector = np.array([self.skill_weights[skill] for skill in self.skill_names])
        
        # Cache LRU pour les résultats
        self._cache_size = 1000
        self._init_caches()
        
        # Patterns regex pré-compilés pour les performances
        self._compile_patterns()
        
        # Matrice de similarité pré-calculée
        self._similarity_matrix = None
        self._build_similarity_matrix()
    
    def _init_caches(self):
        """Initialise les caches LRU"""
        self.text_processing_cache = {}
        self.skill_extraction_cache = {}
        self.experience_cache = {}
        self.education_cache = {}
    
    def _compile_patterns(self):
        """Pré-compile les patterns regex pour les performances"""
        self.experience_patterns = [
            re.compile(r'(\d+)\s*ans?\s+d\'?expérience', re.IGNORECASE),
            re.compile(r'(\d+)\s*years?\s+of\s+experience', re.IGNORECASE),
            re.compile(r'expérience\s*:\s*(\d+)', re.IGNORECASE),
            re.compile(r'experience\s*:\s*(\d+)', re.IGNORECASE),
            re.compile(r'(\d+)\s*années?\s+de\s+', re.IGNORECASE),
            re.compile(r'(\d+)\s*years?\s+in\s+', re.IGNORECASE)
        ]
        
        self.date_pattern = re.compile(r'(19|20)\d{2}')
        self.text_clean_pattern = re.compile(r'[^a-zA-Z\s]')
        
        # Patterns d'éducation
        self.education_patterns = {
            'doctorat': re.compile(r'\b(phd|doctorat|doctorate|thèse)\b', re.IGNORECASE),
            'master': re.compile(r'\b(master|mba|msc|ma|m2|m1)\b', re.IGNORECASE),
            'licence': re.compile(r'\b(licence|bachelor|bsc|ba|l3|l2|l1)\b', re.IGNORECASE),
            'bts': re.compile(r'\b(bts|dut|deug)\b', re.IGNORECASE),
            'bac': re.compile(r'\b(bac|baccalauréat|high school|lycée)\b', re.IGNORECASE)
        }
    
    def _build_similarity_matrix(self):
        """Construit une matrice de similarité entre compétences"""
        n_skills = len(self.skill_names)
        self._similarity_matrix = np.eye(n_skills)
        
        # Groupes de compétences similaires
        similarity_groups = [
            ['python', 'pandas', 'numpy', 'scikit-learn', 'matplotlib'],
            ['machine learning', 'deep learning', 'ai', 'tensorflow', 'pytorch'],
            ['react', 'javascript', 'typescript', 'nodejs'],
            ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            ['mysql', 'postgresql', 'mongodb', 'redis']
        ]
        
        for group in similarity_groups:
            indices = []
            for skill in group:
                if skill in self.skill_names:
                    indices.append(self.skill_names.index(skill))
            
            # Définir la similarité entre les compétences du même groupe
            for i in indices:
                for j in indices:
                    if i != j:
                        self._similarity_matrix[i, j] = 0.7
    
    @lru_cache(maxsize=1000)
    def _process_text(self, text: str) -> str:
        """Traite et nettoie le texte avec cache LRU"""
        if not text:
            return ""
        
        # Convertir en minuscules et nettoyer
        processed = text.lower()
        processed = self.text_clean_pattern.sub(' ', processed)
        
        # Supprimer les mots vides et normaliser les espaces
        words = processed.split()
        words = [word for word in words if len(word) > 2]
        
        return ' '.join(words)
    
    def _extract_skills_vectorized(self, text: str) -> Tuple[List[str], np.ndarray]:
        """Extraction vectorisée des compétences"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        if text_hash in self.skill_extraction_cache:
            return self.skill_extraction_cache[text_hash]
        
        processed_text = self._process_text(text)
        
        # Vectorisation : vérifier toutes les compétences en une fois
        skill_vector = np.zeros(len(self.skill_names))
        found_skills = []
        
        for i, skill in enumerate(self.skill_names):
            if skill in processed_text:
                skill_vector[i] = self.skill_weights[skill]
                found_skills.append(skill)
        
        result = (found_skills, skill_vector)
        self.skill_extraction_cache[text_hash] = result
        
        return result
    
    @lru_cache(maxsize=500)
    def _extract_experience_years(self, text: str) -> float:
        """Extraction optimisée des années d'expérience"""
        years = []
        
        # Utiliser les patterns pré-compilés
        for pattern in self.experience_patterns:
            matches = pattern.findall(text)
            years.extend([int(match) for match in matches])
        
        # Estimation à partir des dates si aucun pattern trouvé
        if not years:
            date_matches = self.date_pattern.findall(text)
            if len(date_matches) >= 2:
                years_found = [int(year) for year in date_matches]
                if years_found:
                    experience = max(years_found) - min(years_found)
                    if experience > 0:
                        years.append(experience)
        
        return max(years) if years else 0.0
    
    @lru_cache(maxsize=500)
    def _extract_education_level(self, text: str) -> str:
        """Extraction optimisée du niveau d'éducation"""
        for level, pattern in self.education_patterns.items():
            if pattern.search(text):
                return level
        return 'inconnu'
    
    def _calculate_skill_similarity_matrix(self, job_skills: List[str], cv_skills_vector: np.ndarray) -> float:
        """Calcule la similarité des compétences avec matrice de similarité"""
        if not job_skills:
            return 0.0
        
        # Créer un vecteur pour les compétences demandées
        job_vector = np.zeros(len(self.skill_names))
        for skill in job_skills:
            skill_lower = skill.lower().strip()
            if skill_lower in self.skill_names:
                idx = self.skill_names.index(skill_lower)
                job_vector[idx] = self.skill_weights[skill_lower]
        
        if np.sum(job_vector) == 0:
            return 0.0
        
        # Calculer la similarité avec la matrice de similarité
        similarity_scores = np.dot(cv_skills_vector, np.dot(self._similarity_matrix, job_vector))
        max_possible_score = np.sum(job_vector)
        
        return min((similarity_scores / max_possible_score) * 100, 100) if max_possible_score > 0 else 0
    
    def _calculate_experience_score_vectorized(self, job_experience: str, cv_experiences: np.ndarray) -> np.ndarray:
        """Calcul vectorisé des scores d'expérience"""
        experience_mapping = {
            'junior': (0, 2),
            'intermediate': (2, 5),
            'senior': (5, 10),
            'expert': (10, 20)
        }
        
        if job_experience not in experience_mapping:
            return np.full(len(cv_experiences), 50.0)
        
        min_exp, max_exp = experience_mapping[job_experience]
        
        # Vectorisation avec numpy
        scores = np.where(
            cv_experiences < min_exp,
            np.maximum(0, cv_experiences / min_exp * 50),
            np.where(
                cv_experiences <= max_exp,
                50 + (cv_experiences - min_exp) / (max_exp - min_exp) * 40,
                np.minimum(100, 90 + (cv_experiences - max_exp) * 2)
            )
        )
        
        return scores
    
    def _calculate_education_scores_vectorized(self, educations: List[str]) -> np.ndarray:
        """Calcul vectorisé des scores d'éducation"""
        education_scores = {
            'doctorat': 100, 'master': 85, 'licence': 70,
            'bts': 60, 'bac': 40, 'inconnu': 30
        }
        
        return np.array([education_scores.get(edu, 30) for edu in educations])
    
    def analyze_cv_batch(self, cv_profiles: List[CVProfile], job_description: str, 
                        job_skills: List[str] = None, job_experience: str = None) -> List[Dict[str, Any]]:
        """Analyse en lot optimisée avec parallélisation"""
        
        if not cv_profiles:
            return []
        
        start_time = time.time()
        
        # Étape 1: Traitement parallèle de l'extraction des données
        with ThreadPoolExecutor(max_workers=self.n_workers) as executor:
            # Extraire les compétences en parallèle
            skill_futures = {
                executor.submit(self._extract_skills_vectorized, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Extraire l'expérience en parallèle
            exp_futures = {
                executor.submit(self._extract_experience_years, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Extraire l'éducation en parallèle
            edu_futures = {
                executor.submit(self._extract_education_level, cv.raw_text): i 
                for i, cv in enumerate(cv_profiles)
            }
            
            # Collecter les résultats
            skills_data = {}
            for future in skill_futures:
                idx = skill_futures[future]
                skills_data[idx] = future.result()
            
            experiences_data = {}
            for future in exp_futures:
                idx = exp_futures[future]
                experiences_data[idx] = future.result()
            
            educations_data = {}
            for future in edu_futures:
                idx = edu_futures[future]
                educations_data[idx] = future.result()
        
        # Étape 2: Calculs vectorisés
        cv_experiences = np.array([experiences_data[i] for i in range(len(cv_profiles))])
        cv_educations = [educations_data[i] for i in range(len(cv_profiles))]
        cv_skills_vectors = np.array([skills_data[i][1] for i in range(len(cv_profiles))])
        
        # Calculs vectorisés des scores
        experience_scores = self._calculate_experience_score_vectorized(job_experience or 'intermediate', cv_experiences)
        education_scores = self._calculate_education_scores_vectorized(cv_educations)
        
        # Étape 3: Calcul des scores finaux
        results = []
        for i, cv in enumerate(cv_profiles):
            found_skills, skill_vector = skills_data[i]
            
            # Scores individuels
            skill_score = self._calculate_skill_similarity_matrix(job_skills or [], skill_vector)
            experience_score = experience_scores[i]
            education_score = education_scores[i]
            
            # Similarité textuelle (optimisée)
            text_similarity = self._calculate_text_similarity_fast(job_description, cv.raw_text)
            
            # Score ML basé sur les features
            ml_score = self._calculate_ml_score_fast(skill_vector, cv_experiences[i], education_score)
            
            # Score final pondéré
            final_score = (
                skill_score * 0.35 +
                experience_score * 0.25 +
                education_score * 0.15 +
                text_similarity * 0.15 +
                ml_score * 0.10
            )
            
            # Déterminer le statut
            if final_score >= 85:
                status, status_class = "Excellent", "excellent"
            elif final_score >= 70:
                status, status_class = "Très bon", "good"
            elif final_score >= 50:
                status, status_class = "Bon", "average"
            else:
                status, status_class = "À améliorer", "poor"
            
            results.append({
                'name': cv.name,
                'final_score': round(final_score, 1),
                'status': status,
                'status_class': status_class,
                'breakdown': {
                    'skill_score': round(skill_score, 1),
                    'experience_score': round(experience_score, 1),
                    'education_score': round(education_score, 1),
                    'text_similarity': round(text_similarity, 1),
                    'ml_score': round(ml_score, 1)
                },
                'extracted_info': {
                    'skills': found_skills,
                    'experience_years': cv_experiences[i],
                    'education': cv_educations[i]
                },
                'processing_time': time.time() - start_time
            })
        
        # Trier par score décroissant
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        return results
    
    @lru_cache(maxsize=200)
    def _calculate_text_similarity_fast(self, text1: str, text2: str) -> float:
        """Calcul rapide de similarité textuelle"""
        if not text1 or not text2:
            return 0.0
        
        # Utiliser des sets pour l'intersection rapide
        words1 = set(self._process_text(text1).split())
        words2 = set(self._process_text(text2).split())
        
        if not words1:
            return 0.0
        
        intersection = len(words1 & words2)
        return min((intersection / len(words1)) * 100, 100)
    
    def _calculate_ml_score_fast(self, skill_vector: np.ndarray, experience: float, education_score: float) -> float:
        """Calcul rapide du score ML"""
        # Score basé sur la densité des compétences
        skill_density = np.sum(skill_vector) / len(skill_vector) * 100
        
        # Score basé sur l'expérience (normalisé)
        exp_score = min(experience * 5, 50)
        
        # Score composite
        composite_score = (skill_density * 0.5 + exp_score * 0.3 + education_score * 0.2)
        
        return min(composite_score, 100)
    
    def analyze_single_cv(self, cv_text: str, cv_name: str, job_description: str, 
                         job_skills: List[str] = None, job_experience: str = None) -> Dict[str, Any]:
        """Analyse rapide d'un CV unique"""
        cv_profile = CVProfile(
            name=cv_name,
            skills=[],
            experience_years=0,
            education='',
            raw_text=cv_text
        )
        
        results = self.analyze_cv_batch([cv_profile], job_description, job_skills, job_experience)
        return results[0] if results else {}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Statistiques de performance du cache"""
        return {
            'cache_sizes': {
                'text_processing': len(self.text_processing_cache),
                'skill_extraction': len(self.skill_extraction_cache),
                'experience': len(self.experience_cache),
                'education': len(self.education_cache)
            },
            'skill_vocabulary_size': len(self.skill_names),
            'similarity_matrix_shape': self._similarity_matrix.shape if self._similarity_matrix is not None else None,
            'workers_count': self.n_workers
        }

# Fonction utilitaire pour créer des profils de CV de test
def create_test_cv_profiles() -> List[CVProfile]:
    """Crée des profils de CV de test pour les benchmarks"""
    profiles = [
        CVProfile(
            name="CV_Senior_Data_Scientist.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Data Scientist Senior avec 8 ans d'expérience en Python, Machine Learning, et Deep Learning.
            Expert en TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, AWS, Docker, Kubernetes.
            Doctorat en Data Science de l'École Polytechnique.
            Projets: Classification d'images, NLP, systèmes de recommandation, MLOps."""
        ),
        CVProfile(
            name="CV_ML_Engineer.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Ingénieur Machine Learning avec 5 ans d'expérience en développement de modèles.
            Compétences: Python, Scikit-learn, Pandas, NumPy, SQL, Git, Jenkins.
            Master en Intelligence Artificielle. Expérience en déploiement de modèles en production."""
        ),
        CVProfile(
            name="CV_Data_Analyst.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Analyste de données avec 3 ans d'expérience en analyse statistique.
            Maîtrise de Python, Pandas, Matplotlib, SQL, Excel, Tableau.
            Licence en Statistiques. Spécialisé dans la visualisation de données."""
        ),
        CVProfile(
            name="CV_Junior_Developer.pdf",
            skills=[],
            experience_years=0,
            education="",
            raw_text="""Développeur Junior avec 1 an d'expérience en développement web.
            Technologies: JavaScript, React, HTML, CSS, Node.js.
            BTS en Développement Web. Stage de 6 mois en entreprise."""
        )
    ]
    
    return profiles

def benchmark_analyzer():
    """Benchmark de performance de l'analyseur"""
    print("🚀 BENCHMARK DE L'ANALYSEUR ML OPTIMISÉ")
    print("=" * 50)
    
    try:
        analyzer = OptimizedMLAnalyzer()
        cv_profiles = create_test_cv_profiles()
        
        job_description = """Nous recherchons un Data Scientist senior pour rejoindre notre équipe.
        Compétences requises: Python, Machine Learning, Deep Learning, TensorFlow, PyTorch.
        Expérience: 5+ ans. Master ou PhD en Data Science."""
        
        job_skills = ['python', 'machine learning', 'tensorflow', 'pytorch', 'deep learning']
        
        # Benchmark
        start_time = time.time()
        results = analyzer.analyze_cv_batch(cv_profiles, job_description, job_skills, 'senior')
        end_time = time.time()
        
        print(f"⏱️  Temps d'analyse: {end_time - start_time:.3f} secondes")
        print(f"📊 CVs analysés: {len(results)}")
        print(f"⚡ Vitesse: {len(results)/(end_time - start_time):.1f} CVs/seconde")
        print()
        
        for result in results:
            print(f"📄 {result['name']}: {result['final_score']}% ({result['status']})")
        
        print()
        stats = analyzer.get_performance_stats()
        print("📈 Statistiques de performance:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Erreur lors du benchmark: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    benchmark_analyzer()







