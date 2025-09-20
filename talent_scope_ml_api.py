#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TalentScope - API ML Complète
API REST pour l'analyse de CVs avec machine learning
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import json
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
import pickle
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Téléchargement des ressources NLTK (à faire une seule fois)
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
except:
    logger.warning("Impossible de télécharger les ressources NLTK")

@dataclass
class CVData:
    """Structure de données pour un CV"""
    id: str
    filename: str
    raw_text: str
    skills: List[str]
    experience_years: float
    education_level: str
    languages: List[str]
    certifications: List[str]
    processed_text: str = ""
    upload_date: str = ""

@dataclass
class JobOffer:
    """Structure de données pour une offre d'emploi"""
    id: str
    title: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]
    min_experience: float
    required_education: str
    languages: List[str]
    processed_text: str = ""
    created_date: str = ""

@dataclass
class AnalysisResult:
    """Résultat d'analyse d'un CV"""
    cv_id: str
    job_id: str
    overall_score: float
    overall_similarity: float
    skills_match: float
    experience_match: float
    education_match: float
    language_match: float
    rank: int
    analysis_date: str

class TextPreprocessor:
    """Classe pour le prétraitement de texte"""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('french') + stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
        except:
            self.stop_words = set()
            self.lemmatizer = None
            logger.warning("NLTK non disponible, utilisation du mode simplifié")
    
    def clean_text(self, text: str) -> str:
        """Nettoie et normalise le texte"""
        if not text:
            return ""
        
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères spéciaux et des chiffres
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        
        # Suppression des espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        """Tokenise et lemmatise le texte"""
        try:
            if self.lemmatizer:
                tokens = word_tokenize(text)
                tokens = [self.lemmatizer.lemmatize(token) 
                         for token in tokens 
                         if token not in self.stop_words and len(token) > 2]
                return tokens
            else:
                # Fallback simple
                words = text.split()
                return [word for word in words if len(word) > 2]
        except:
            # Fallback simple si NLTK ne fonctionne pas
            words = text.split()
            return [word for word in words if len(word) > 2]
    
    def preprocess(self, text: str) -> str:
        """Préprocess complet du texte"""
        cleaned = self.clean_text(text)
        tokens = self.tokenize_and_lemmatize(cleaned)
        return ' '.join(tokens)

class CVAnalyzer:
    """Analyseur principal de CV utilisant le machine learning"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=100)
        self.is_fitted = False
        
        # Mappings pour les niveaux d'éducation
        self.education_mapping = {
            'bac': 1, 'bachelor': 2, 'licence': 2, 'master': 3, 'mba': 3, 
            'doctorat': 4, 'phd': 4, 'ingénieur': 3, 'bts': 1.5, 'dut': 1.5
        }
        
        # Stockage des données
        self.cvs_data = []
        self.jobs_data = []
        self.model_file = "talent_scope_model.pkl"
        
        # Charger le modèle s'il existe
        self.load_model()
    
    def save_model(self):
        """Sauvegarde le modèle entraîné"""
        try:
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'scaler': self.scaler,
                'pca': self.pca,
                'is_fitted': self.is_fitted,
                'cvs_data': self.cvs_data,
                'jobs_data': self.jobs_data,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info("Modèle sauvegardé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du modèle: {e}")
    
    def load_model(self):
        """Charge le modèle sauvegardé"""
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.tfidf_vectorizer = model_data.get('tfidf_vectorizer', self.tfidf_vectorizer)
                self.scaler = model_data.get('scaler', self.scaler)
                self.pca = model_data.get('pca', self.pca)
                self.is_fitted = model_data.get('is_fitted', False)
                self.cvs_data = model_data.get('cvs_data', [])
                self.jobs_data = model_data.get('jobs_data', [])
                
                logger.info("Modèle chargé avec succès")
        except Exception as e:
            logger.warning(f"Impossible de charger le modèle: {e}")
    
    def add_cv(self, cv_data: CVData):
        """Ajoute un CV à la base de données"""
        cv_data.upload_date = datetime.now().isoformat()
        cv_data.processed_text = self.preprocessor.preprocess(
            f"{cv_data.raw_text} {' '.join(cv_data.skills)} {cv_data.education_level} {' '.join(cv_data.languages)}"
        )
        
        # Vérifier si le CV existe déjà
        existing_cv = next((cv for cv in self.cvs_data if cv.id == cv_data.id), None)
        if existing_cv:
            # Mettre à jour le CV existant
            index = self.cvs_data.index(existing_cv)
            self.cvs_data[index] = cv_data
        else:
            # Ajouter un nouveau CV
            self.cvs_data.append(cv_data)
        
        logger.info(f"CV {cv_data.id} ajouté/mis à jour")
    
    def add_job(self, job_data: JobOffer):
        """Ajoute une offre d'emploi à la base de données"""
        job_data.created_date = datetime.now().isoformat()
        job_data.processed_text = self.preprocessor.preprocess(
            f"{job_data.title} {job_data.description} {' '.join(job_data.required_skills)} {' '.join(job_data.preferred_skills)} {job_data.required_education}"
        )
        
        # Vérifier si l'offre existe déjà
        existing_job = next((job for job in self.jobs_data if job.id == job_data.id), None)
        if existing_job:
            # Mettre à jour l'offre existante
            index = self.jobs_data.index(existing_job)
            self.jobs_data[index] = job_data
        else:
            # Ajouter une nouvelle offre
            self.jobs_data.append(job_data)
        
        logger.info(f"Offre {job_data.id} ajoutée/mise à jour")
    
    def fit(self):
        """Entraîne le modèle sur les données disponibles"""
        if not self.cvs_data and not self.jobs_data:
            logger.warning("Aucune donnée disponible pour l'entraînement")
            return
        
        logger.info(f"Entraînement du modèle sur {len(self.cvs_data)} CVs et {len(self.jobs_data)} offres")
        
        # Préprocessing des textes
        all_texts = []
        for cv in self.cvs_data:
            all_texts.append(cv.processed_text)
        
        for job in self.jobs_data:
            all_texts.append(job.processed_text)
        
        if all_texts:
            # Entraînement du vectoriseur TF-IDF
            self.tfidf_vectorizer.fit(all_texts)
            
            # Extraction des features pour les CVs
            if self.cvs_data:
                cv_features = []
                for cv in self.cvs_data:
                    features = self.extract_features_from_cv(cv)
                    cv_features.append(features)
                
                cv_features = np.array(cv_features)
                
                # Normalisation et réduction de dimensionnalité
                self.scaler.fit(cv_features)
                scaled_features = self.scaler.transform(cv_features)
                
                if scaled_features.shape[1] > 100:
                    self.pca.fit(scaled_features)
            
            self.is_fitted = True
            logger.info("Modèle entraîné avec succès")
            
            # Sauvegarder le modèle
            self.save_model()
    
    def extract_features_from_cv(self, cv: CVData) -> np.ndarray:
        """Extrait les features d'un CV"""
        # Features textuelles (TF-IDF)
        text_features = self.tfidf_vectorizer.transform([cv.processed_text]).toarray()[0]
        
        # Features numériques
        numerical_features = [
            cv.experience_years,
            self.education_mapping.get(cv.education_level.lower(), 0),
            len(cv.skills),
            len(cv.languages),
            len(cv.certifications)
        ]
        
        # Combinaison des features
        combined_features = np.concatenate([text_features, numerical_features])
        return combined_features
    
    def extract_features_from_job(self, job: JobOffer) -> np.ndarray:
        """Extrait les features d'une offre d'emploi"""
        # Features textuelles (TF-IDF)
        text_features = self.tfidf_vectorizer.transform([job.processed_text]).toarray()[0]
        
        # Features numériques
        numerical_features = [
            job.min_experience,
            self.education_mapping.get(job.required_education.lower(), 0),
            len(job.required_skills + job.preferred_skills),
            len(job.languages),
            0  # placeholder pour les certifications
        ]
        
        # Combinaison des features
        combined_features = np.concatenate([text_features, numerical_features])
        return combined_features
    
    def calculate_similarity_score(self, cv: CVData, job: JobOffer) -> Dict:
        """Calcule le score de similarité entre un CV et une offre d'emploi"""
        if not self.is_fitted:
            # Entraîner le modèle si ce n'est pas fait
            self.fit()
        
        if not self.is_fitted:
            raise ValueError("Le modèle ne peut pas être entraîné")
        
        # Extraction des features
        cv_features = self.extract_features_from_cv(cv).reshape(1, -1)
        job_features = self.extract_features_from_job(job).reshape(1, -1)
        
        # Normalisation
        cv_scaled = self.scaler.transform(cv_features)
        job_scaled = self.scaler.transform(job_features)
        
        # Réduction de dimensionnalité si nécessaire
        if hasattr(self.pca, 'components_'):
            cv_reduced = self.pca.transform(cv_scaled)
            job_reduced = self.pca.transform(job_scaled)
        else:
            cv_reduced = cv_scaled
            job_reduced = job_scaled
        
        # Calcul de la similarité cosinus
        overall_similarity = cosine_similarity(cv_reduced, job_reduced)[0][0]
        
        # Calculs de similarités spécifiques
        skills_match = self.calculate_skills_match(cv.skills, job.required_skills, job.preferred_skills)
        experience_match = self.calculate_experience_match(cv.experience_years, job.min_experience)
        education_match = self.calculate_education_match(cv.education_level, job.required_education)
        language_match = self.calculate_language_match(cv.languages, job.languages)
        
        # Score pondéré final
        weighted_score = (
            overall_similarity * 0.4 +
            skills_match * 0.3 +
            experience_match * 0.15 +
            education_match * 0.10 +
            language_match * 0.05
        )
        
        return {
            'overall_score': float(weighted_score),
            'overall_similarity': float(overall_similarity),
            'skills_match': float(skills_match),
            'experience_match': float(experience_match),
            'education_match': float(education_match),
            'language_match': float(language_match),
            'cv_id': cv.id,
            'job_id': job.id
        }
    
    def calculate_skills_match(self, cv_skills: List[str], required_skills: List[str], preferred_skills: List[str]) -> float:
        """Calcule la correspondance des compétences"""
        cv_skills_lower = [skill.lower() for skill in cv_skills]
        required_lower = [skill.lower() for skill in required_skills]
        preferred_lower = [skill.lower() for skill in preferred_skills]
        
        # Correspondance des compétences requises
        required_match = len(set(cv_skills_lower) & set(required_lower)) / max(len(required_lower), 1)
        
        # Correspondance des compétences préférées
        preferred_match = len(set(cv_skills_lower) & set(preferred_lower)) / max(len(preferred_lower), 1)
        
        # Score pondéré
        return required_match * 0.7 + preferred_match * 0.3
    
    def calculate_experience_match(self, cv_experience: float, required_experience: float) -> float:
        """Calcule la correspondance de l'expérience"""
        if cv_experience >= required_experience:
            return 1.0
        elif cv_experience >= required_experience * 0.8:
            return 0.8
        elif cv_experience >= required_experience * 0.6:
            return 0.6
        else:
            return cv_experience / required_experience if required_experience > 0 else 0.5
    
    def calculate_education_match(self, cv_education: str, required_education: str) -> float:
        """Calcule la correspondance du niveau d'éducation"""
        cv_level = self.education_mapping.get(cv_education.lower(), 0)
        required_level = self.education_mapping.get(required_education.lower(), 0)
        
        if cv_level >= required_level:
            return 1.0
        else:
            return cv_level / required_level if required_level > 0 else 0.5
    
    def calculate_language_match(self, cv_languages: List[str], required_languages: List[str]) -> float:
        """Calcule la correspondance des langues"""
        if not required_languages:
            return 1.0
        
        cv_langs_lower = [lang.lower() for lang in cv_languages]
        required_langs_lower = [lang.lower() for lang in required_languages]
        
        matches = len(set(cv_langs_lower) & set(required_langs_lower))
        return matches / len(required_langs_lower)
    
    def rank_candidates(self, job_id: str, cv_ids: List[str] = None) -> List[Dict]:
        """Classe les candidats par ordre de pertinence pour un poste"""
        # Trouver l'offre d'emploi
        job = next((j for j in self.jobs_data if j.id == job_id), None)
        if not job:
            raise ValueError(f"Offre d'emploi {job_id} non trouvée")
        
        # Sélectionner les CVs à analyser
        if cv_ids:
            cvs = [cv for cv in self.cvs_data if cv.id in cv_ids]
        else:
            cvs = self.cvs_data
        
        if not cvs:
            raise ValueError("Aucun CV trouvé pour l'analyse")
        
        logger.info(f"Classement de {len(cvs)} candidats pour le poste {job.title}")
        
        results = []
        for cv in cvs:
            score_data = self.calculate_similarity_score(cv, job)
            results.append(score_data)
        
        # Tri par score décroissant
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Ajout du rang et des informations du CV
        for i, result in enumerate(results):
            result['rank'] = i + 1
            result['cv_filename'] = next((cv.filename for cv in cvs if cv.id == result['cv_id']), '')
            result['analysis_date'] = datetime.now().isoformat()
        
        return results
    
    def get_top_candidates(self, job_id: str, top_n: int = 4, cv_ids: List[str] = None) -> List[Dict]:
        """Retourne les N meilleurs candidats"""
        ranked_results = self.rank_candidates(job_id, cv_ids)
        return ranked_results[:top_n]

# Instance globale de l'analyseur
analyzer = CVAnalyzer()

# Initialisation de l'API FastAPI
app = FastAPI(
    title="TalentScope ML API",
    description="API d'analyse de CVs avec machine learning",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "TalentScope ML API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": {
            "cvs": "/api/cvs",
            "jobs": "/api/jobs", 
            "analysis": "/api/analysis"
        }
    }

@app.get("/api/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_fitted": analyzer.is_fitted,
        "cvs_count": len(analyzer.cvs_data),
        "jobs_count": len(analyzer.jobs_data)
    }

# === GESTION DES CVs ===

@app.post("/api/cvs/upload")
async def upload_cv(
    filename: str = Form(...),
    content: str = Form(...),
    skills: str = Form(""),
    experience_years: float = Form(0.0),
    education_level: str = Form(""),
    languages: str = Form(""),
    certifications: str = Form("")
):
    """Télécharge et traite un CV"""
    try:
        # Créer l'ID du CV
        cv_id = f"cv_{len(analyzer.cvs_data) + 1:03d}"
        
        # Parser les listes
        skills_list = [s.strip() for s in skills.split(',') if s.strip()] if skills else []
        languages_list = [l.strip() for l in languages.split(',') if l.strip()] if languages else []
        certifications_list = [c.strip() for c in certifications.split(',') if c.strip()] if certifications else []
        
        # Créer l'objet CV
        cv_data = CVData(
            id=cv_id,
            filename=filename,
            raw_text=content,
            skills=skills_list,
            experience_years=experience_years,
            education_level=education_level,
            languages=languages_list,
            certifications=certifications_list
        )
        
        # Ajouter le CV
        analyzer.add_cv(cv_data)
        
        # Réentraîner le modèle
        analyzer.fit()
        
        return {
            "success": True,
            "cv_id": cv_id,
            "message": f"CV {filename} téléchargé avec succès",
            "total_cvs": len(analyzer.cvs_data)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du CV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cvs/list")
async def list_cvs():
    """Liste tous les CVs"""
    return {
        "success": True,
        "cvs": [
            {
                "id": cv.id,
                "filename": cv.filename,
                "skills": cv.skills,
                "experience_years": cv.experience_years,
                "education_level": cv.education_level,
                "languages": cv.languages,
                "certifications": cv.certifications,
                "upload_date": cv.upload_date
            }
            for cv in analyzer.cvs_data
        ],
        "total": len(analyzer.cvs_data)
    }

@app.delete("/api/cvs/{cv_id}")
async def delete_cv(cv_id: str):
    """Supprime un CV"""
    try:
        cv_to_remove = next((cv for cv in analyzer.cvs_data if cv.id == cv_id), None)
        if not cv_to_remove:
            raise HTTPException(status_code=404, detail="CV non trouvé")
        
        analyzer.cvs_data.remove(cv_to_remove)
        analyzer.fit()  # Réentraîner le modèle
        
        return {
            "success": True,
            "message": f"CV {cv_id} supprimé avec succès",
            "total_cvs": len(analyzer.cvs_data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du CV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === GESTION DES OFFRES D'EMPLOI ===

@app.post("/api/jobs/create")
async def create_job(
    title: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(""),
    preferred_skills: str = Form(""),
    min_experience: float = Form(0.0),
    required_education: str = Form(""),
    languages: str = Form("")
):
    """Crée une nouvelle offre d'emploi"""
    try:
        # Créer l'ID de l'offre
        job_id = f"job_{len(analyzer.jobs_data) + 1:03d}"
        
        # Parser les listes
        required_skills_list = [s.strip() for s in required_skills.split(',') if s.strip()] if required_skills else []
        preferred_skills_list = [s.strip() for s in preferred_skills.split(',') if s.strip()] if preferred_skills else []
        languages_list = [l.strip() for l in languages.split(',') if l.strip()] if languages else []
        
        # Créer l'objet Job
        job_data = JobOffer(
            id=job_id,
            title=title,
            description=description,
            required_skills=required_skills_list,
            preferred_skills=preferred_skills_list,
            min_experience=min_experience,
            required_education=required_education,
            languages=languages_list
        )
        
        # Ajouter l'offre
        analyzer.add_job(job_data)
        
        # Réentraîner le modèle
        analyzer.fit()
        
        return {
            "success": True,
            "job_id": job_id,
            "message": f"Offre {title} créée avec succès",
            "total_jobs": len(analyzer.jobs_data)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'offre: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/jobs/list")
async def list_jobs():
    """Liste toutes les offres d'emploi"""
    return {
        "success": True,
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "required_skills": job.required_skills,
                "preferred_skills": job.preferred_skills,
                "min_experience": job.min_experience,
                "required_education": job.required_education,
                "languages": job.languages,
                "created_date": job.created_date
            }
            for job in analyzer.jobs_data
        ],
        "total": len(analyzer.jobs_data)
    }

# === ANALYSE ET COMPARAISON ===

@app.post("/api/analysis/rank")
async def rank_candidates(
    job_id: str = Form(...),
    cv_ids: str = Form(""),
    top_n: int = Form(4)
):
    """Classe les candidats par ordre de pertinence"""
    try:
        # Parser les IDs des CVs
        cv_ids_list = [cv_id.strip() for cv_id in cv_ids.split(',') if cv_id.strip()] if cv_ids else None
        
        # Effectuer le classement
        results = analyzer.get_top_candidates(job_id, top_n, cv_ids_list)
        
        return {
            "success": True,
            "job_id": job_id,
            "results": results,
            "total_analyzed": len(results),
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du classement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analysis/analyze")
async def analyze_cv_job_match(
    job_id: str = Form(...),
    cv_id: str = Form(...)
):
    """Analyse la correspondance entre un CV et une offre d'emploi"""
    try:
        # Trouver le CV et l'offre
        cv = next((c for c in analyzer.cvs_data if c.id == cv_id), None)
        job = next((j for j in analyzer.jobs_data if j.id == job_id), None)
        
        if not cv:
            raise HTTPException(status_code=404, detail="CV non trouvé")
        if not job:
            raise HTTPException(status_code=404, detail="Offre d'emploi non trouvée")
        
        # Calculer le score
        result = analyzer.calculate_similarity_score(cv, job)
        
        return {
            "success": True,
            "cv_id": cv_id,
            "job_id": job_id,
            "cv_filename": cv.filename,
            "job_title": job.title,
            "scores": result,
            "analysis_date": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/results/{job_id}")
async def get_analysis_results(job_id: str, top_n: int = 4):
    """Récupère les résultats d'analyse pour une offre d'emploi"""
    try:
        results = analyzer.get_top_candidates(job_id, top_n)
        
        return {
            "success": True,
            "job_id": job_id,
            "results": results,
            "total_candidates": len(results),
            "analysis_date": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des résultats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === ENDPOINTS DE DÉMONSTRATION ===

@app.post("/api/demo/setup")
async def setup_demo_data():
    """Configure des données de démonstration"""
    try:
        # CVs de démonstration
        demo_cvs = [
            CVData(
                id="cv_001",
                filename="cv_Adam.pdf",
                raw_text="Développeur Python avec 1 an d'expérience. Compétences en programmation de base.",
                skills=["Python", "Programmation"],
                experience_years=1.0,
                education_level="Licence",
                languages=["Français"],
                certifications=[]
            ),
            CVData(
                id="cv_002", 
                filename="cv_Ali.pdf",
                raw_text="Data Scientist avec 5 ans d'expérience en machine learning et analyse de données. Expert en Python, TensorFlow, et statistiques.",
                skills=["Python", "Machine Learning", "TensorFlow", "Data Science", "Statistiques"],
                experience_years=5.0,
                education_level="Master",
                languages=["Français", "Anglais"],
                certifications=["AWS ML", "Google Analytics"]
            ),
            CVData(
                id="cv_003",
                filename="cv_Hafsa.pdf", 
                raw_text="Ingénieure IA avec 4 ans d'expérience en deep learning et computer vision. Spécialisée en PyTorch et réseaux de neurones.",
                skills=["Python", "Deep Learning", "PyTorch", "Computer Vision", "IA"],
                experience_years=4.0,
                education_level="Ingénieur",
                languages=["Français", "Anglais", "Arabe"],
                certifications=["Deep Learning Specialization"]
            ),
            CVData(
                id="cv_004",
                filename="cv_Hamza.pdf",
                raw_text="Développeur Backend avec 2 ans d'expérience en Java et Spring Boot. Connaissance des bases de données.",
                skills=["Java", "Spring Boot", "PostgreSQL", "Backend"],
                experience_years=2.0,
                education_level="Licence",
                languages=["Français", "Anglais"],
                certifications=[]
            )
        ]
        
        # Offre de démonstration
        demo_job = JobOffer(
            id="job_001",
            title="Data Scientist",
            description="Recherche un Data Scientist avec expérience en Python, machine learning, et analyse de données. Le candidat idéal devrait avoir des connaissances en pandas, scikit-learn, et visualisation de données.",
            required_skills=["Python", "Machine Learning", "Data Science"],
            preferred_skills=["TensorFlow", "Pandas", "Scikit-learn"],
            min_experience=2.0,
            required_education="Master",
            languages=["Français", "Anglais"]
        )
        
        # Ajouter les données
        for cv in demo_cvs:
            analyzer.add_cv(cv)
        
        analyzer.add_job(demo_job)
        
        # Entraîner le modèle
        analyzer.fit()
        
        return {
            "success": True,
            "message": "Données de démonstration configurées avec succès",
            "cvs_added": len(demo_cvs),
            "jobs_added": 1,
            "model_fitted": analyzer.is_fitted
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la configuration des données de démonstration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Démarrage de TalentScope ML API v2.0...")
    print("📊 API d'analyse de CVs avec machine learning")
    print("🔗 Documentation disponible sur http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

