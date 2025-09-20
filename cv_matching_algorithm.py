"""
Algorithme universel de matching CV-Offre d'emploi
Compatible avec tous les secteurs d'activité
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import warnings
warnings.filterwarnings('ignore')

# Télécharger les ressources NLTK nécessaires
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

@dataclass
class MatchingScore:
    """Classe pour stocker les scores de matching détaillés"""
    overall_score: float
    competencies_score: float
    experience_score: float
    education_score: float
    semantic_score: float
    keyword_score: float
    soft_skills_score: float
    details: Dict[str, Any]

class UniversalCVJobMatcher:
    """Algorithme universel de matching CV-Offre d'emploi"""
    
    def __init__(self, language='fr'):
        self.language = language
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('french' if language == 'fr' else 'english'))
        
        # Modèles pré-entraînés
        print("Chargement des modèles universels...")
        self.sentence_model = SentenceTransformer('distiluse-base-multilingual-cased')
        
        try:
            self.nlp = spacy.load("fr_core_news_sm")
        except OSError:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Modèle spaCy non trouvé. Installation : python -m spacy download fr_core_news_sm")
                self.nlp = None
        
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words=list(self.stop_words),
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95
        )
        
        # Pondérations
        self.weights = {
            'competencies': 0.25,
            'experience': 0.25,
            'education': 0.15,
            'semantic': 0.20,
            'keywords': 0.10,
            'soft_skills': 0.05
        }
        
        # Bases de connaissances
        self.universal_competencies = self._load_universal_competencies()
        self.soft_skills_keywords = self._load_soft_skills()
        self.education_levels = self._load_education_levels()

    def _load_universal_competencies(self) -> Dict[str, List[str]]:
        """Base de compétences pour tous les secteurs"""
        return {
            # SECTEUR COMMERCIAL & VENTE
            'vente': ['vente', 'commercial', 'prospection', 'négociation', 'closing', 'b2b', 'b2c', 'crm', 'pipeline'],
            'marketing': ['marketing', 'communication', 'digital', 'seo', 'sem', 'social media', 'brand', 'campagne'],
            'relation_client': ['service client', 'support', 'satisfaction', 'fidélisation', 'réclamations'],
            
            # SECTEUR FINANCIER
            'finance': ['comptabilité', 'audit', 'contrôle de gestion', 'budget', 'fiscalité', 'consolidation'],
            'banque': ['crédit', 'risk management', 'compliance', 'trading', 'asset management', 'private banking'],
            'assurance': ['souscription', 'sinistres', 'actuariat', 'courtage', 'réassurance'],
            
            # SECTEUR RH & MANAGEMENT
            'ressources_humaines': ['recrutement', 'formation', 'paie', 'droit social', 'sirh', 'talents'],
            'management': ['leadership', 'équipe', 'coaching', 'performance', 'stratégie', 'change management'],
            
            # SECTEUR MÉDICAL & SANTÉ
            'medical': ['diagnostic', 'thérapie', 'patient', 'protocole', 'hygiène', 'urgences', 'chirurgie'],
            'pharmacie': ['médicaments', 'posologie', 'interactions', 'galénique', 'réglementation'],
            'paramédical': ['soins', 'rééducation', 'prévention', 'accompagnement', 'matériel médical'],
            
            # SECTEUR JURIDIQUE
            'droit': ['contrats', 'contentieux', 'jurisprudence', 'conseil juridique', 'compliance', 'réglementation'],
            'notariat': ['actes', 'succession', 'immobilier', 'famille', 'patrimoine'],
            
            # SECTEUR INGÉNIERIE & TECHNIQUE
            'ingenierie': ['conception', 'calculs', 'études', 'projets', 'normes', 'qualité', 'innovation'],
            'production': ['manufacturing', 'lean', 'amélioration continue', 'maintenance', 'sécurité'],
            'logistique': ['supply chain', 'approvisionnement', 'stocks', 'transport', 'optimisation'],
            
            # SECTEUR IT & DÉVELOPPEMENT
            'developpement': ['programmation', 'développement', 'coding', 'software', 'applications', 'debugging'],
            'langages': ['python', 'java', 'javascript', 'c++', 'php', 'ruby', 'golang', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'frontend', 'backend'],
            'data': ['machine learning', 'deep learning', 'data science', 'big data', 'sql', 'nosql', 'hadoop'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing', 'devops', 'docker', 'kubernetes'],
            
            # COMPÉTENCES TRANSVERSALES
            'gestion_projet': ['project management', 'planning', 'budget', 'risques', 'agile', 'scrum'],
            'analyse': ['analyse', 'synthèse', 'reporting', 'kpi', 'tableaux de bord', 'data analysis'],
            'langues': ['anglais', 'espagnol', 'allemand', 'italien', 'mandarin', 'multilingue'],
            'outils_bureautique': ['excel', 'word', 'powerpoint', 'outlook', 'sharepoint', 'teams']
        }
    
    def _load_soft_skills(self) -> List[str]:
        """Compétences comportementales universelles"""
        return [
            'communication', 'leadership', 'travail en équipe', 'autonomie', 'rigueur',
            'adaptabilité', 'créativité', 'initiative', 'empathie', 'résolution de problèmes',
            'organisation', 'persévérance', 'diplomatie', 'écoute', 'curiosité',
            'stress management', 'flexibilité', 'proactivité', 'collaboration', 'innovation'
        ]
    
    def _load_education_levels(self) -> Dict[int, List[str]]:
        """Niveaux d'éducation universels"""
        return {
            6: ['doctorat', 'phd', 'hdr', 'professeur', 'chercheur'],
            5: ['master', 'mastère', 'mba', 'ingénieur', 'pharmacien', 'médecin', 'avocat'],
            4: ['licence', 'bachelor', 'bac+3', 'licence professionnelle'],
            3: ['bts', 'dut', 'bac+2', 'technicien supérieur'],
            2: ['baccalauréat', 'bac', 'niveau bac', 'terminale'],
            1: ['cap', 'bep', 'certificat', 'niveau cap']
        }

    def preprocess_text(self, text: str) -> str:
        """Prétraitement du texte"""
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'[^\w\sàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def extract_competencies(self, text: str, sector_hint: Optional[str] = None) -> List[str]:
        """Extraction des compétences avec contexte sectoriel"""
        text_lower = text.lower()
        found_competencies = []
        
        categories_to_search = self.universal_competencies.keys()
        if sector_hint:
            categories_to_search = [k for k in categories_to_search if sector_hint.lower() in k] + list(categories_to_search)
        
        for category, keywords in self.universal_competencies.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_competencies.append(category)
                    break
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['PRODUCT', 'ORG', 'MISC', 'SKILL']:
                    entity_text = ent.text.lower()
                    for category, keywords in self.universal_competencies.items():
                        if any(kw in entity_text for kw in keywords):
                            found_competencies.append(category)
        
        return list(set(found_competencies))

    def extract_soft_skills(self, text: str) -> List[str]:
        """Extraction des soft skills"""
        text_lower = text.lower()
        return [skill for skill in self.soft_skills_keywords if skill in text_lower]

    def extract_years_experience(self, text: str) -> int:
        """Extraction des années d'expérience"""
        patterns = [
            r'(\d+)\s*an[s]?\s*d[\'e]?\s*expérience',
            r'(\d+)\s*année[s]?\s*d[\'e]?\s*expérience',
            r'expérience\s*:?\s*(\d+)\s*an[s]?',
            r'(\d+)\s*an[s]?\s*dans',
            r'depuis\s*(\d+)\s*an[s]?',
            r'(\d+)\s*year[s]?\s*of\s*experience',
            r'(\d+)\s*year[s]?\s*experience',
            r'experience\s*:?\s*(\d+)\s*year[s]?',
            r'(\d+)\+\s*an[s]?',
            r'plus\s*de\s*(\d+)\s*an[s]?'
        ]
        
        max_years = 0
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = int(match)
                    if years <= 50:  # Filtre de réalisme
                        max_years = max(max_years, years)
                except ValueError:
                    continue
        
        return max_years

    def extract_education_level(self, text: str) -> int:
        """Extraction du niveau d'éducation"""
        text_lower = text.lower()
        max_level = 0
        
        for level, keywords in self.education_levels.items():
            for keyword in keywords:
                if keyword in text_lower:
                    max_level = max(max_level, level)
        
        return max_level

    def calculate_competencies_score(self, cv_competencies: List[str], job_competencies: List[str]) -> float:
        """Calcul du score de compétences"""
        if not job_competencies:
            return 1.0
        
        cv_set = set(cv_competencies)
        job_set = set(job_competencies)
        
        common_competencies = cv_set.intersection(job_set)
        coverage_score = len(common_competencies) / len(job_set) if job_set else 0
        
        bonus_competencies = cv_set - job_set
        bonus_score = min(len(bonus_competencies) * 0.05, 0.2)
        
        return min(coverage_score + bonus_score, 1.0)

    def calculate_soft_skills_score(self, cv_soft_skills: List[str], job_soft_skills: List[str]) -> float:
        """Calcul du score de soft skills"""
        if not job_soft_skills:
            return 1.0
        
        cv_set = set(cv_soft_skills)
        job_set = set(job_soft_skills)
        
        if not job_set:
            return 1.0
        
        common_skills = cv_set.intersection(job_set)
        return len(common_skills) / len(job_set)

    def calculate_experience_score(self, cv_experience: int, required_experience: int) -> float:
        """Calcul du score d'expérience"""
        if required_experience == 0:
            return 1.0
        
        if cv_experience >= required_experience:
            bonus = min((cv_experience - required_experience) * 0.02, 0.1)
            return min(1.0 + bonus, 1.0)
        else:
            return max(cv_experience / required_experience, 0.3)

    def calculate_education_score(self, cv_education: int, required_education: int) -> float:
        """Calcul du score de formation"""
        if required_education == 0:
            return 1.0
        
        if cv_education >= required_education:
            return 1.0
        else:
            return max(cv_education / required_education, 0.5)

    def calculate_semantic_similarity(self, cv_text: str, job_text: str) -> float:
        """Calcul de la similarité sémantique"""
        try:
            cv_embedding = self.sentence_model.encode([cv_text])
            job_embedding = self.sentence_model.encode([job_text])
            
            similarity = cosine_similarity(cv_embedding, job_embedding)[0][0]
            return max(0, similarity)
        except Exception as e:
            print(f"Erreur similarité sémantique: {e}")
            return 0.0

    def calculate_keyword_score(self, cv_text: str, job_text: str) -> float:
        """Calcul du score de mots-clés"""
        try:
            cv_processed = self.preprocess_text(cv_text)
            job_processed = self.preprocess_text(job_text)
            
            if not cv_processed or not job_processed:
                return 0.0
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([cv_processed, job_processed])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return max(0, similarity)
        except Exception as e:
            print(f"Erreur score mots-clés: {e}")
            return 0.0

    def match_cv_to_job(self, cv_text: str, job_description: str, 
                       required_experience: int = 0, required_education: int = 0,
                       sector_hint: Optional[str] = None) -> MatchingScore:
        """Matching complet CV-Offre"""
        
        # Extraction des caractéristiques
        cv_competencies = self.extract_competencies(cv_text, sector_hint)
        job_competencies = self.extract_competencies(job_description, sector_hint)
        
        cv_soft_skills = self.extract_soft_skills(cv_text)
        job_soft_skills = self.extract_soft_skills(job_description)
        
        cv_experience = self.extract_years_experience(cv_text)
        cv_education = self.extract_education_level(cv_text)
        
        if required_education == 0:
            required_education = self.extract_education_level(job_description)
        
        # Calcul des scores
        competencies_score = self.calculate_competencies_score(cv_competencies, job_competencies)
        soft_skills_score = self.calculate_soft_skills_score(cv_soft_skills, job_soft_skills)
        experience_score = self.calculate_experience_score(cv_experience, required_experience)
        education_score = self.calculate_education_score(cv_education, required_education)
        semantic_score = self.calculate_semantic_similarity(cv_text, job_description)
        keyword_score = self.calculate_keyword_score(cv_text, job_description)
        
        # Score global pondéré
        overall_score = (
            competencies_score * self.weights['competencies'] +
            experience_score * self.weights['experience'] +
            education_score * self.weights['education'] +
            semantic_score * self.weights['semantic'] +
            keyword_score * self.weights['keywords'] +
            soft_skills_score * self.weights['soft_skills']
        )
        
        # Détails pour analyse
        details = {
            'cv_competencies': cv_competencies,
            'job_competencies': job_competencies,
            'cv_soft_skills': cv_soft_skills,
            'job_soft_skills': job_soft_skills,
            'cv_experience': cv_experience,
            'required_experience': required_experience,
            'cv_education_level': cv_education,
            'required_education_level': required_education,
            'common_competencies': list(set(cv_competencies) & set(job_competencies)),
            'missing_competencies': list(set(job_competencies) - set(cv_competencies)),
            'sector_hint': sector_hint
        }
        
        return MatchingScore(
            overall_score=round(overall_score, 3),
            competencies_score=round(competencies_score, 3),
            experience_score=round(experience_score, 3),
            education_score=round(education_score, 3),
            semantic_score=round(semantic_score, 3),
            keyword_score=round(keyword_score, 3),
            soft_skills_score=round(soft_skills_score, 3),
            details=details
        )

    def rank_candidates(self, candidates: List[Dict[str, Any]], 
                       job_description: str, required_experience: int = 0,
                       required_education: int = 0, sector_hint: Optional[str] = None) -> List[Tuple[Dict, MatchingScore]]:
        """Classement des candidats"""
        results = []
        
        for candidate in candidates:
            score = self.match_cv_to_job(
                candidate['cv_text'], 
                job_description, 
                required_experience,
                required_education,
                sector_hint
            )
            results.append((candidate, score))
        
        results.sort(key=lambda x: x[1].overall_score, reverse=True)
        return results

    def generate_feedback(self, matching_score: MatchingScore) -> str:
        """Génération du feedback détaillé"""
        feedback = []
        score = matching_score
        
        # Score global
        if score.overall_score >= 0.8:
            feedback.append("🟢 EXCELLENT PROFIL ! Correspondance très élevée avec l'offre.")
        elif score.overall_score >= 0.65:
            feedback.append("🟡 BON PROFIL avec des axes d'optimisation identifiés.")
        elif score.overall_score >= 0.45:
            feedback.append("🟠 PROFIL CORRECT nécessitant quelques améliorations.")
        else:
            feedback.append("🔴 PROFIL À DÉVELOPPER - Écart significatif avec les exigences.")
        
        # Analyse détaillée
        if score.details['missing_competencies']:
            feedback.append(f"❌ Compétences manquantes prioritaires : {', '.join(score.details['missing_competencies'][:5])}")
        
        if score.details['common_competencies']:
            feedback.append(f"✅ Compétences correspondantes : {', '.join(score.details['common_competencies'][:5])}")
        
        # Expérience
        exp_diff = score.details['required_experience'] - score.details['cv_experience']
        if exp_diff > 0:
            feedback.append(f"⏳ Expérience : Il manque {exp_diff} année(s) par rapport aux exigences.")
        elif score.details['cv_experience'] > score.details['required_experience']:
            feedback.append(f"✨ Expérience : +{score.details['cv_experience'] - score.details['required_experience']} année(s) au-dessus du requis.")
        
        # Formation
        edu_diff = score.details['required_education_level'] - score.details['cv_education_level']
        if edu_diff > 0:
            feedback.append(f"🎓 Formation : Niveau requis supérieur de {edu_diff} niveau(x).")
        
        return '\n'.join(feedback)

# Création d'une instance globale
matcher = UniversalCVJobMatcher()
