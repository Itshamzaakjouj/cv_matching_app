from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
import uvicorn
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

app = FastAPI(title="TalentScope API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class CVData(BaseModel):
    name: str
    person: str
    position: str
    experience: str
    level: str
    score: float
    skills: float
    experience_score: float
    education: float

class JobDescription(BaseModel):
    description: str

class AnalysisRequest(BaseModel):
    job_description: str
    cvs: List[CVData]

class ConfigData(BaseModel):
    technical_weight: float
    experience_weight: float
    education_weight: float
    language: str
    theme: str
    auto_save: bool
    export_format: str
    include_charts: bool
    email_reports: bool

# Données simulées (comme dans l'ancienne app)
cv_data = {
    "cv_1.pdf": {
        "score": 85.5,
        "compétences": 90,
        "expérience": 80,
        "éducation": 75,
        "nom": "Marie Dubois",
        "poste": "Data Scientist",
        "expérience_ans": "3 ans",
        "niveau": "Intermédiaire"
    },
    "cv_2.pdf": {
        "score": 92.3,
        "compétences": 95,
        "expérience": 90,
        "éducation": 85,
        "nom": "Jean Martin",
        "poste": "Senior Data Analyst",
        "expérience_ans": "5 ans",
        "niveau": "Senior"
    },
    "cv_3.pdf": {
        "score": 78.1,
        "compétences": 85,
        "expérience": 70,
        "éducation": 80,
        "nom": "Sophie Bernard",
        "poste": "Junior Developer",
        "expérience_ans": "1 an",
        "niveau": "Junior"
    },
    "cv_4.pdf": {
        "score": 88.7,
        "compétences": 90,
        "expérience": 85,
        "éducation": 90,
        "nom": "Pierre Moreau",
        "poste": "ML Engineer",
        "expérience_ans": "4 ans",
        "niveau": "Intermédiaire"
    },
    "cv_5.pdf": {
        "score": 94.2,
        "compétences": 95,
        "expérience": 95,
        "éducation": 90,
        "nom": "Anna Kowalski",
        "poste": "Lead Data Scientist",
        "expérience_ans": "7 ans",
        "niveau": "Expert"
    }
}

# Configuration par défaut
config_data = {
    "technical_weight": 0.50,
    "experience_weight": 0.30,
    "education_weight": 0.20,
    "language": "Français",
    "theme": "Clair",
    "auto_save": True,
    "export_format": "PDF",
    "include_charts": True,
    "email_reports": False
}

# Routes API
@app.get("/")
async def root():
    return {"message": "TalentScope API is running"}

@app.get("/api/cvs")
async def get_cvs():
    """Récupérer tous les CVs"""
    return {"cvs": cv_data}

@app.post("/api/cvs")
async def add_cv(cv: CVData):
    """Ajouter un nouveau CV"""
    cv_key = f"cv_{cv.name}.pdf"
    cv_data[cv_key] = {
        "score": cv.score,
        "compétences": cv.skills,
        "expérience": cv.experience_score,
        "éducation": cv.education,
        "nom": cv.person,
        "poste": cv.position,
        "expérience_ans": cv.experience,
        "niveau": cv.level
    }
    return {"message": "CV ajouté avec succès", "cv": cv_data[cv_key]}

@app.post("/api/analysis")
async def analyze_cvs(request: AnalysisRequest):
    """Analyser les CVs avec la description de poste"""
    # Simulation de l'analyse ML (comme dans l'ancienne app)
    results = []
    
    for cv in request.cvs:
        # Calcul du score basé sur les poids de configuration
        technical_score = cv.skills * config_data["technical_weight"]
        experience_score = cv.experience_score * config_data["experience_weight"]
        education_score = cv.education * config_data["education_weight"]
        
        total_score = technical_score + experience_score + education_score
        
        results.append({
            "name": cv.name,
            "person": cv.person,
            "position": cv.position,
            "score": round(total_score, 1),
            "technical_score": round(technical_score, 1),
            "experience_score": round(experience_score, 1),
            "education_score": round(education_score, 1),
            "level": cv.level,
            "experience": cv.experience
        })
    
    # Trier par score décroissant
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "results": results,
        "job_description": request.job_description,
        "analysis_date": datetime.now().isoformat()
    }

@app.get("/api/comparison")
async def get_comparison_data(selected_cvs: str):
    """Récupérer les données de comparaison pour les CVs sélectionnés"""
    cv_names = selected_cvs.split(",") if selected_cvs else []
    comparison_data = []
    
    for cv_name in cv_names:
        if cv_name in cv_data:
            data = cv_data[cv_name]
            comparison_data.append({
                "name": cv_name,
                "person": data["nom"],
                "position": data["poste"],
                "score": data["score"],
                "skills": data["compétences"],
                "experience": data["expérience"],
                "education": data["éducation"],
                "level": data["niveau"],
                "experience_years": data["expérience_ans"]
            })
    
    return {"comparison_data": comparison_data}

@app.get("/api/charts/radar")
async def get_radar_chart_data(selected_cvs: str):
    """Générer les données pour le graphique radar"""
    cv_names = selected_cvs.split(",") if selected_cvs else []
    
    categories = ['Compétences', 'Expérience', 'Éducation']
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']
    
    radar_data = []
    
    for i, cv_name in enumerate(cv_names):
        if cv_name in cv_data:
            data = cv_data[cv_name]
            color = colors[i % len(colors)]
            
            radar_data.append({
                "name": data["nom"],
                "values": [data["compétences"], data["expérience"], data["éducation"]],
                "color": color,
                "fillColor": f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)"
            })
    
    return {
        "categories": categories,
        "data": radar_data
    }

@app.get("/api/charts/bar")
async def get_bar_chart_data(selected_cvs: str):
    """Générer les données pour le graphique en barres"""
    cv_names = selected_cvs.split(",") if selected_cvs else []
    
    bar_data = {
        "labels": [],
        "datasets": [
            {"label": "Compétences", "data": [], "backgroundColor": "#3B82F6"},
            {"label": "Expérience", "data": [], "backgroundColor": "#10B981"},
            {"label": "Formation", "data": [], "backgroundColor": "#F59E0B"}
        ]
    }
    
    for cv_name in cv_names:
        if cv_name in cv_data:
            data = cv_data[cv_name]
            bar_data["labels"].append(data["nom"])
            bar_data["datasets"][0]["data"].append(data["compétences"])
            bar_data["datasets"][1]["data"].append(data["expérience"])
            bar_data["datasets"][2]["data"].append(data["éducation"])
    
    return bar_data

@app.get("/api/config")
async def get_config():
    """Récupérer la configuration"""
    return config_data

@app.post("/api/config")
async def update_config(config: ConfigData):
    """Mettre à jour la configuration"""
    global config_data
    config_data = config.dict()
    return {"message": "Configuration mise à jour avec succès"}

@app.get("/api/dashboard")
async def get_dashboard_data():
    """Récupérer les données du dashboard"""
    total_cvs = len(cv_data)
    avg_score = sum(cv["score"] for cv in cv_data.values()) / total_cvs if total_cvs > 0 else 0
    
    # Top 3 CVs
    top_cvs = sorted(cv_data.items(), key=lambda x: x[1]["score"], reverse=True)[:3]
    
    # Répartition par niveau
    level_distribution = {}
    for cv in cv_data.values():
        level = cv["niveau"]
        level_distribution[level] = level_distribution.get(level, 0) + 1
    
    return {
        "total_cvs": total_cvs,
        "average_score": round(avg_score, 1),
        "top_cvs": [
            {
                "name": name,
                "person": data["nom"],
                "score": data["score"],
                "position": data["poste"]
            }
            for name, data in top_cvs
        ],
        "level_distribution": level_distribution,
        "recent_analyses": [
            {
                "id": 1,
                "job_title": "Data Scientist",
                "date": "2025-09-18",
                "candidates": 5,
                "best_score": 94.2
            },
            {
                "id": 2,
                "job_title": "ML Engineer",
                "date": "2025-09-17",
                "candidates": 3,
                "best_score": 88.7
            }
        ]
    }

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_app():
    """Servir l'application HTML"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
