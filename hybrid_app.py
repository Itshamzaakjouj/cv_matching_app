#!/usr/bin/env python3
"""
🏛️ TALENTSCOPE - APPLICATION HYBRIDE MODERNE
Ministère de l'Économie et des Finances
Version: 2.0 Hybride (Auth existante + App moderne)
"""

from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
import asyncio
from datetime import datetime
from typing import List, Optional
import pandas as pd
import base64
from pathlib import Path

# Configuration de l'application FastAPI
app = FastAPI(
    title="TalentScope - Ministère de l'Économie et des Finances",
    description="Application hybride moderne de matching CV",
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

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de données en mémoire (pour la démo)
users_db = {
    "admin@ministere.gov.ma": {"password": "admin123", "name": "Administrateur", "role": "admin"},
    "user@ministere.gov.ma": {"password": "user123", "name": "Utilisateur", "role": "user"}
}

sessions_db = {}
analyses_db = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil - Redirection vers l'interface d'authentification existante"""
    return RedirectResponse(url="http://localhost:8080/auth_interface.html")

@app.get("/auth", response_class=HTMLResponse)
async def auth_page(request: Request):
    """Page d'authentification - Redirection vers l'interface existante"""
    return RedirectResponse(url="http://localhost:8080/auth_interface.html")

@app.post("/api/login")
async def login(email: str = Form(...), password: str = Form(...)):
    """API de connexion"""
    if email in users_db and users_db[email]["password"] == password:
        session_id = f"session_{datetime.now().timestamp()}"
        sessions_db[session_id] = {
            "email": email,
            "name": users_db[email]["name"],
            "role": users_db[email]["role"],
            "login_time": datetime.now().isoformat()
        }
        return JSONResponse({
            "success": True,
            "session_id": session_id,
            "user": {
                "name": users_db[email]["name"],
                "role": users_db[email]["role"]
            }
        })
    return JSONResponse({"success": False, "message": "Identifiants incorrects"}, status_code=401)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session_id: Optional[str] = None):
    """Tableau de bord principal moderne"""
    if not session_id or session_id not in sessions_db:
        return RedirectResponse(url="http://localhost:8080/auth_interface.html")
    
    user = sessions_db[session_id]
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "session_id": session_id
    })

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request, session_id: Optional[str] = None):
    """Page d'analyse moderne"""
    if not session_id or session_id not in sessions_db:
        return RedirectResponse(url="http://localhost:8080/auth_interface.html")
    
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "session_id": session_id
    })

@app.post("/api/analyze")
async def analyze_cvs(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...),
    session_id: str = Form(...)
):
    """API d'analyse des CVs"""
    if not session_id or session_id not in sessions_db:
        raise HTTPException(status_code=401, detail="Session invalide")
    
    # Simulation d'analyse (remplacer par vraie logique ML)
    results = []
    for i, file in enumerate(files):
        score = 85 + (i * 3)  # Score simulé
        results.append({
            "name": file.filename,
            "score": score,
            "status": "Excellent" if score >= 90 else "Très bon" if score >= 80 else "Bon",
            "position": f"Candidat {i+1}",
            "skills": ["Python", "Machine Learning", "Data Science"],
            "date": datetime.now().strftime("%d/%m/%Y")
        })
    
    # Sauvegarder l'analyse
    analysis_id = f"analysis_{datetime.now().timestamp()}"
    analyses_db[analysis_id] = {
        "job_description": job_description,
        "results": results,
        "created_at": datetime.now().isoformat(),
        "session_id": session_id
    }
    
    return JSONResponse({
        "success": True,
        "analysis_id": analysis_id,
        "results": results
    })

@app.get("/api/dashboard-data")
async def get_dashboard_data(session_id: str):
    """Données du tableau de bord"""
    if not session_id or session_id not in sessions_db:
        raise HTTPException(status_code=401, detail="Session invalide")
    
    # Données simulées pour le dashboard
    return JSONResponse({
        "stats": {
            "total_analyses": 24,
            "total_cvs": 156,
            "average_score": 78.5,
            "success_rate": 92.3
        },
        "recent_analyses": [
            {"name": "cv_hamza.pdf", "score": 91.3, "date": "18/09/2024"},
            {"name": "cv_sophia.pdf", "score": 76.1, "date": "17/09/2024"},
            {"name": "cv_adam.pdf", "score": 85.2, "date": "16/09/2024"}
        ],
        "trends": {
            "daily_analyses": [12, 15, 8, 20, 18, 16, 8],
            "scores": [75.2, 76.1, 72.8, 81.5, 79.3, 78.1, 80.2]
        }
    })

@app.get("/api/logout")
async def logout(session_id: str):
    """Déconnexion"""
    if session_id in sessions_db:
        del sessions_db[session_id]
    return JSONResponse({"success": True})

if __name__ == "__main__":
    print("🏛️ TALENTSCOPE - APPLICATION HYBRIDE MODERNE")
    print("=" * 60)
    print("🚀 Technologies: FastAPI + Interface Auth existante")
    print("⚡ Performance maximale avec interface familière")
    print("=" * 60)
    
    # Créer les dossiers nécessaires
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    
    print("✅ Dossiers créés")
    print("🚀 Démarrage du serveur...")
    
    uvicorn.run(
        "hybrid_app:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
