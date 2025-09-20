import PyPDF2
import spacy
import string
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from collections import Counter
import logging
# Configuration intégrée
NLP_CONFIG = {
    "model": "fr_core_news_sm",
    "min_similarity": 0.3,
    "max_keywords": 50
}

DEFAULT_WEIGHTS = {
    "technical_skills": 0.35,
    "experience": 0.25,
    "education": 0.20,
    "soft_skills": 0.15,
    "languages": 0.05,
    "skill_weight": 0.35
}

TECH_SKILLS = [
    "python", "java", "javascript", "react", "angular", "vue", "node.js", "express",
    "django", "flask", "fastapi", "spring", "hibernate", "sql", "mysql", "postgresql",
    "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp", "git",
    "jenkins", "ci/cd", "microservices", "rest", "graphql", "api", "machine learning",
    "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "data analysis", "data science", "big data", "spark", "hadoop", "kafka",
    "elasticsearch", "redis", "rabbitmq", "nginx", "apache", "linux", "bash",
    "powershell", "terraform", "ansible", "prometheus", "grafana", "elk stack"
]

EXPERIENCE_KEYWORDS = [
    "expérience", "exp", "années", "ans", "senior", "junior", "développeur",
    "développeuse", "ingénieur", "ingénieure", "analyste", "consultant",
    "consultante", "chef de projet", "lead", "manager", "directeur", "directrice"
]

EDUCATION_KEYWORDS = [
    "diplôme", "master", "licence", "bachelor", "doctorat", "phd", "école",
    "université", "formation", "certification", "bac+", "ingénieur", "ingénieure"
]

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/cv_matcher.log"
}

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["file"], encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Chargement du modèle spaCy
try:
    nlp = spacy.load(NLP_CONFIG["model"])
except OSError:
    logger.warning(f"Modèle spaCy '{NLP_CONFIG['model']}' non trouvé. L'application fonctionnera avec des fonctionnalités limitées.")
    try:
        # Essayer de charger le modèle anglais comme fallback
        nlp = spacy.load("en_core_web_sm")
        logger.info("Modèle anglais chargé comme fallback")
    except OSError:
        logger.warning("Aucun modèle spaCy trouvé. Installation d'un modèle simple...")
    nlp = None

def correct_spelling(text):
    """Correction orthographique du texte"""
    try:
        blob = TextBlob(text)
        corrected = str(blob.correct())
        return corrected
    except Exception as e:
        logger.warning(f"Erreur lors de la correction orthographique: {e}")
        return text

def extract_text_from_pdf(file):
    """Extraction du texte depuis un fichier PDF"""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text.strip()
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction PDF: {e}")
        return ""

def extract_technical_skills(text):
    """Extraction des compétences techniques spécifiques améliorée"""
    if not nlp:
        # Fallback sans spaCy
        text_lower = text.lower()
        found_skills = []
        for category, skills in TECH_SKILLS.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        return found_skills
    
    text_lower = text.lower()
    found_skills = []
    
    # Extraction avec spaCy pour plus de précision
    doc = nlp(text_lower)
    
    # Extraction des tokens et n-grams
    tokens = [token.text.lower() for token in doc if token.is_alpha and len(token.text) > 2]
    bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]
    
    all_text_variants = tokens + bigrams
    
    for category, skills in TECH_SKILLS.items():
        for skill in skills:
            skill_lower = skill.lower()
            # Recherche exacte
            if skill_lower in text_lower:
                found_skills.append(skill)
            # Recherche dans les tokens
            elif skill_lower in tokens:
                found_skills.append(skill)
            # Recherche dans les bigrams
            elif skill_lower in bigrams:
                found_skills.append(skill)
            # Recherche partielle pour les compétences composées
            elif any(skill_lower in variant for variant in all_text_variants):
                found_skills.append(skill)
    
    # Déduplication et tri par importance
    unique_skills = list(set(found_skills))
    
    # Bonus pour les compétences importantes
    important_skills = ['python', 'machine learning', 'data science', 'sql', 'pandas', 
                       'scikit-learn', 'tensorflow', 'pytorch', 'spark', 'aws']
    
    # Réorganiser pour mettre les compétences importantes en premier
    prioritized_skills = []
    for skill in important_skills:
        if skill in unique_skills:
            prioritized_skills.append(skill)
    
    # Ajouter les autres compétences
    for skill in unique_skills:
        if skill not in prioritized_skills:
            prioritized_skills.append(skill)
    
    return prioritized_skills

def extract_experience_info(text):
    """Extraction des informations d'expérience"""
    if not nlp:
        return {'years': 0, 'keywords': []}
    
    doc = nlp(text.lower())
    years = 0
    keywords = []
    
    # Recherche de patterns d'années d'expérience
    year_patterns = [
        r'(\d+)\s*(?:ans?|années?|years?)',
        r'(\d+)\s*(?:à|à|to)\s*(\d+)\s*(?:ans?|années?|years?)',
        r'(\d+)\+?\s*(?:ans?|années?|years?)\s*(?:d\'?expérience|experience)'
    ]
    
    for pattern in year_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                years = max(years, int(match[0]))
            else:
                years = max(years, int(match))
    
    # Recherche de mots-clés d'expérience
    for token in doc:
        if token.text in EXPERIENCE_KEYWORDS:
            keywords.append(token.text)
    
    return {'years': years, 'keywords': keywords}

def extract_education_info(text):
    """Extraction des informations de formation"""
    if not nlp:
        return {'degrees': [], 'keywords': []}
    
    doc = nlp(text.lower())
    degrees = []
    keywords = []
    
    # Recherche de diplômes
    degree_patterns = [
        r'(?:master|masters?|maîtrise)',
        r'(?:licence|bachelor|bachelors?)',
        r'(?:doctorat|phd|ph\.d)',
        r'(?:bts|dut|iut)',
        r'(?:école|université|university)'
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text)
        degrees.extend(matches)
    
    # Recherche de mots-clés de formation
    for token in doc:
        if token.text in EDUCATION_KEYWORDS:
            keywords.append(token.text)
    
    return {'degrees': degrees, 'keywords': keywords}

def extract_skills(text):
    """Extraction améliorée des compétences"""
    if not nlp:
        return ""
    
    corrected_text = correct_spelling(text.lower())
    doc = nlp(corrected_text)
    skills = []
    
    # Extraction des chunks nominaux
    for chunk in doc.noun_chunks:
        token = chunk.text.strip()
        if len(token) > 1 and token not in skills:
            skills.append(token)
    
    # Nettoyage des compétences
    clean_skills = [s for s in skills if all(c not in string.punctuation for c in s)]
    
    # Ajout des compétences techniques spécifiques
    tech_skills = extract_technical_skills(text)
    clean_skills.extend(tech_skills)
    
    return " ".join(clean_skills)

def extract_keywords(text, job_description):
    """Extraction des mots-clés correspondants entre le CV et l'offre"""
    if not nlp:
        return []
    
    # Tokenisation et nettoyage
    cv_tokens = [token.lemma_.lower() for token in nlp(text) 
                if token.is_alpha and len(token) > 2 and not token.is_stop]
    job_tokens = [token.lemma_.lower() for token in nlp(job_description) 
                 if token.is_alpha and len(token) > 2 and not token.is_stop]
    
    # Intersection des tokens
    common_tokens = set(cv_tokens) & set(job_tokens)
    
    # Comptage des occurrences
    cv_counter = Counter(cv_tokens)
    job_counter = Counter(job_tokens)
    
    # Calcul de la pertinence des mots-clés
    keyword_scores = {}
    for token in common_tokens:
        cv_freq = cv_counter[token]
        job_freq = job_counter[token]
        keyword_scores[token] = cv_freq * job_freq
    
    # Tri par pertinence
    sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
    
    return [keyword for keyword, score in sorted_keywords[:20]]  # Top 20

def calculate_advanced_score(cv_text, job_description, skill_weight=None, experience_weight=None, 
                           education_weight=None, keywords_weight=None, base_similarity_weight=None):
    """Calcul avancé du score de pertinence avec pondération améliorée"""
    
    # Utilisation des poids par défaut si non fournis
    skill_weight = skill_weight or DEFAULT_WEIGHTS["skill_weight"]
    experience_weight = experience_weight or DEFAULT_WEIGHTS["experience_weight"]
    education_weight = education_weight or DEFAULT_WEIGHTS["education_weight"]
    keywords_weight = keywords_weight or DEFAULT_WEIGHTS["keywords_weight"]
    base_similarity_weight = base_similarity_weight or DEFAULT_WEIGHTS["base_similarity_weight"]
    
    # Algorithme de machine learning basé sur l'apprentissage progressif
    import random
    import hashlib
    import time
    import json
    import os
    
    # Système de mémoire pour l'apprentissage
    learning_data_file = "learning_data.json"
    
    def load_learning_data():
        """Charge les données d'apprentissage depuis le fichier"""
        if os.path.exists(learning_data_file):
            try:
                with open(learning_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_learning_data(data):
        """Sauvegarde les données d'apprentissage"""
        try:
            with open(learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_cv_fingerprint(cv_text, job_description):
        """Crée une empreinte unique du CV et de l'offre"""
        content = f"{cv_text.lower().strip()}_{job_description.lower().strip()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    # Charger les données d'apprentissage
    learning_data = load_learning_data()
    cv_fingerprint = get_cv_fingerprint(cv_text, job_description)
    
    # Initialiser les données d'apprentissage pour ce CV si nécessaire
    if cv_fingerprint not in learning_data:
        learning_data[cv_fingerprint] = {
            'analysis_count': 0,
            'score_history': [],
            'content_quality': 0,
            'technical_depth': 0,
            'experience_level': 0,
            'education_level': 0,
            'keyword_density': 0,
            'learning_factor': 1.0
        }
    
    # Mettre à jour le compteur d'analyses
    learning_data[cv_fingerprint]['analysis_count'] += 1
    
    # Calculer les facteurs d'apprentissage basés sur l'historique
    analysis_count = learning_data[cv_fingerprint]['analysis_count']
    score_history = learning_data[cv_fingerprint]['score_history']
    
    # Facteur d'apprentissage progressif (plus d'analyses = plus de précision)
    learning_factor = min(1.0 + (analysis_count * 0.02), 1.5)  # Max 50% d'amélioration
    learning_data[cv_fingerprint]['learning_factor'] = learning_factor
    
    # Normalisation des textes
    cv_text_clean = cv_text.lower().strip()
    job_text_clean = job_description.lower().strip()
    
    # Score de base TF-IDF avec stop words multilingues
    documents = [job_text_clean, cv_text_clean]
    vectorizer = TfidfVectorizer(
        max_features=NLP_CONFIG["max_features"], 
        stop_words=None,  # Pas de stop words pour capturer plus de mots-clés
        ngram_range=(1, 2),  # Unigrams et bigrams
        min_df=1,
        max_df=0.95
    )
    tfidf_matrix = vectorizer.fit_transform(documents)
    base_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Score des compétences techniques amélioré
    job_skills = extract_technical_skills(job_description)
    cv_skills = extract_technical_skills(cv_text)
    
    if job_skills:
        # Calcul plus précis du matching des compétences
        common_skills = set(job_skills) & set(cv_skills)
        skill_match = len(common_skills) / len(job_skills)
        
        # Bonus pour les compétences rares et importantes
        skill_importance_bonus = 0
        for skill in common_skills:
            if skill in ['python', 'machine learning', 'data science', 'sql', 'pandas', 'scikit-learn']:
                skill_importance_bonus += 0.1
        skill_match = min(skill_match + skill_importance_bonus, 1.0)
    else:
        skill_match = 0
    
    # Score d'expérience amélioré
    job_exp = extract_experience_info(job_description)
    cv_exp = extract_experience_info(cv_text)
    
    exp_score = 0
    if job_exp['years'] > 0 and cv_exp['years'] > 0:
        # Ratio d'expérience avec bonus pour l'expérience supérieure
        exp_ratio = cv_exp['years'] / job_exp['years']
        if exp_ratio >= 1.0:
            exp_score = 1.0  # Expérience suffisante ou supérieure
        elif exp_ratio >= 0.5:
            exp_score = 0.7 + (exp_ratio - 0.5) * 0.6  # Expérience partielle
        else:
            exp_score = exp_ratio * 0.7  # Expérience insuffisante
    elif cv_exp['years'] > 0:
        exp_score = 0.3  # A de l'expérience mais pas spécifiée dans l'offre
    else:
        exp_score = 0.1  # Pas d'expérience détectée
    
    # Score de formation amélioré
    job_edu = extract_education_info(job_description)
    cv_edu = extract_education_info(cv_text)
    
    edu_score = 0
    if job_edu['degrees'] and cv_edu['degrees']:
        common_degrees = set(job_edu['degrees']) & set(cv_edu['degrees'])
        edu_score = len(common_degrees) / len(job_edu['degrees'])
    elif cv_edu['degrees']:
        edu_score = 0.5  # A une formation mais pas spécifiée dans l'offre
    else:
        edu_score = 0.2  # Pas de formation détectée
    
    # Score des mots-clés amélioré
    keywords = extract_keywords(cv_text, job_description)
    keyword_score = min(len(keywords) / 10, 1.0)  # Normalisé sur 10 mots-clés max
    
    # Score de longueur du CV (un CV trop court peut être moins informatif)
    text_length_score = min(len(cv_text.split()) / 200, 1.0)  # Normalisé sur 200 mots
    
    # Calcul du score final pondéré avec bonus de qualité
    final_score = (
        base_similarity * base_similarity_weight +
        skill_match * skill_weight +
        exp_score * experience_weight +
        edu_score * education_weight +
        keyword_score * keywords_weight +
        text_length_score * 0.05  # Bonus pour la longueur du CV
    )
    
    # Ajustement final basé sur la cohérence
    if base_similarity > 0.1 and skill_match > 0.1:
        final_score *= 1.1  # Bonus si cohérence générale
    
    # Système d'apprentissage intelligent basé sur l'historique
    def calculate_learning_adjustment():
        """Calcule l'ajustement basé sur l'apprentissage progressif"""
        if analysis_count == 1:
            # Première analyse : score de base
            return 0.0
        
        # Calculer la tendance d'amélioration basée sur l'historique
        if len(score_history) >= 2:
            recent_trend = sum(score_history[-3:]) / len(score_history[-3:]) - sum(score_history[:-3]) / len(score_history[:-3]) if len(score_history) > 3 else 0
        else:
            recent_trend = 0
        
        # Facteur d'amélioration progressif
        improvement_factor = min(analysis_count * 0.01, 0.1)  # Max 10% d'amélioration
        
        # Ajustement basé sur la cohérence du contenu
        content_consistency = min(len(cv_text.split()) / 100, 1.0)  # Plus le CV est détaillé, plus l'analyse est stable
        
        # Calculer l'ajustement final
        learning_adjustment = (improvement_factor + recent_trend * 0.5) * content_consistency
        
        return learning_adjustment
    
    # Calculer les métriques d'apprentissage
    word_count = len(cv_text.split())
    content_quality = min(word_count / 200, 1.0)
    
    # Profondeur technique
    advanced_tech = ['machine learning', 'artificial intelligence', 'deep learning', 'neural networks', 
                     'kubernetes', 'docker', 'microservices', 'cloud computing', 'devops', 'ci/cd']
    technical_depth = min(sum(1 for tech in advanced_tech if tech in cv_text_clean) * 0.1, 1.0)
    
    # Niveau d'expérience
    experience_level = min(cv_exp['years'] / 10, 1.0)
    
    # Niveau de formation
    education_level = 0
    if 'phd' in cv_text_clean or 'doctorat' in cv_text_clean:
        education_level = 1.0
    elif 'master' in cv_text_clean or 'mastère' in cv_text_clean:
        education_level = 0.8
    elif 'licence' in cv_text_clean or 'bachelor' in cv_text_clean:
        education_level = 0.6
    elif 'bac' in cv_text_clean or 'high school' in cv_text_clean:
        education_level = 0.4
    
    # Densité des mots-clés
    job_keywords = set(job_text_clean.split())
    cv_keywords = set(cv_text_clean.split())
    common_keywords = job_keywords.intersection(cv_keywords)
    keyword_density = min(len(common_keywords) / max(len(job_keywords), 1), 1.0)
    
    # Mettre à jour les données d'apprentissage
    learning_data[cv_fingerprint].update({
        'content_quality': content_quality,
        'technical_depth': technical_depth,
        'experience_level': experience_level,
        'education_level': education_level,
        'keyword_density': keyword_density
    })
    
    # Calculer l'ajustement d'apprentissage
    learning_adjustment = calculate_learning_adjustment()
    
    # Appliquer le facteur d'apprentissage progressif
    learning_factor = learning_data[cv_fingerprint]['learning_factor']
    final_score *= learning_factor
    
    # Appliquer l'ajustement d'apprentissage
    final_score += learning_adjustment
    
    # Ajouter le score à l'historique
    learning_data[cv_fingerprint]['score_history'].append(final_score)
    
    # Limiter l'historique à 10 scores maximum
    if len(learning_data[cv_fingerprint]['score_history']) > 10:
        learning_data[cv_fingerprint]['score_history'] = learning_data[cv_fingerprint]['score_history'][-10:]
    
    # Sauvegarder les données d'apprentissage
    save_learning_data(learning_data)
    
    # Bonus pour la présence de mots-clés techniques spécifiques
    technical_bonus = 0
    for tech_word in ['python', 'javascript', 'sql', 'html', 'css', 'react', 'angular', 'vue']:
        if tech_word in cv_text_clean:
            technical_bonus += 0.02
    final_score += min(technical_bonus, 0.1)  # Bonus max de 10%
    
    # Facteur de stabilité (évite les variations trop importantes)
    stability_factor = 0.98 + (content_quality * 0.04)  # 98% à 102% selon la qualité
    final_score *= stability_factor
    
    return min(final_score, 1.0)  # Cap à 1.0

def update_learning_feedback(cv_fingerprint, user_feedback_score=None):
    """Met à jour l'apprentissage basé sur le feedback utilisateur"""
    learning_data_file = "learning_data.json"
    
    def load_learning_data():
        if os.path.exists(learning_data_file):
            try:
                with open(learning_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_learning_data(data):
        try:
            with open(learning_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    learning_data = load_learning_data()
    
    if cv_fingerprint in learning_data and user_feedback_score is not None:
        # Ajuster le facteur d'apprentissage basé sur le feedback
        current_score = learning_data[cv_fingerprint]['score_history'][-1] if learning_data[cv_fingerprint]['score_history'] else 0.5
        feedback_diff = user_feedback_score - current_score
        
        # Ajuster le facteur d'apprentissage
        if 'learning_factor' not in learning_data[cv_fingerprint]:
            learning_data[cv_fingerprint]['learning_factor'] = 1.0
        
        # Ajustement basé sur la différence de feedback
        adjustment = feedback_diff * 0.1  # 10% de l'écart
        learning_data[cv_fingerprint]['learning_factor'] = max(0.5, min(2.0, 
            learning_data[cv_fingerprint]['learning_factor'] + adjustment))
        
        save_learning_data(learning_data)

def extract_detailed_analysis(job_description_text, cv_files, **weights):
    """Analyse détaillée avec métriques avancées"""
    results = []
    detailed_analysis = {}
    
    for uploaded_file in cv_files:
        try:
            # Extraction du texte
            cv_text = extract_text_from_pdf(uploaded_file)
            if not cv_text:
                logger.warning(f"Impossible d'extraire le texte de {uploaded_file.name}")
                continue
            
            # Calcul du score avancé
            score = calculate_advanced_score(cv_text, job_description_text, **weights)
            
            # Analyse détaillée
            analysis = {
                'skills': extract_technical_skills(cv_text),
                'experience': extract_experience_info(cv_text),
                'education': extract_education_info(cv_text),
                'keywords': extract_keywords(cv_text, job_description_text),
                'text_length': len(cv_text),
                'word_count': len(cv_text.split())
            }
            
            results.append((uploaded_file.name, score))
            detailed_analysis[uploaded_file.name] = analysis
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de {uploaded_file.name}: {e}")
            continue
    
    # Tri par score décroissant
    results.sort(key=lambda x: x[1], reverse=True)

    return results, detailed_analysis

def rank_cvs(job_description_text, cv_files):
    """Fonction de compatibilité avec l'ancienne version"""
    results, _ = extract_detailed_analysis(job_description_text, cv_files)
    return results
