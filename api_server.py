#!/usr/bin/env python3
"""
TalentScope - Serveur API Backend
Ministère de l'Économie et des Finances
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import json
import hashlib
import shutil
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from database import db

# Configuration de l'application FastAPI
app = FastAPI(
    title="TalentScope API",
    description="API pour la plateforme de gestion des talents",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer les dossiers nécessaires
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="."), name="static")

# Variables globales pour la session
current_user = None

def get_current_user():
    """Récupère l'utilisateur actuel"""
    return current_user

# Routes d'authentification
@app.post("/api/auth/login")
async def login(email: str = Form(...), password: str = Form(...)):
    """Authentification utilisateur"""
    global current_user
    
    user = db.get_user_by_email(email)
    if not user or user['password'] != password:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    
    # Mettre à jour la dernière connexion
    db.update_user_login(user['id'])
    current_user = user
    
    return {
        "success": True,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "role": user['role'],
            "department": user['department'],
            "position": user['position']
        }
    }

@app.post("/api/auth/logout")
async def logout():
    """Déconnexion utilisateur"""
    global current_user
    current_user = None
    return {"success": True, "message": "Déconnexion réussie"}

@app.get("/api/auth/me")
async def get_current_user_info():
    """Récupère les informations de l'utilisateur connecté"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    return {
        "success": True,
        "user": {
            "id": current_user['id'],
            "name": current_user['name'],
            "email": current_user['email'],
            "role": current_user['role'],
            "department": current_user['department'],
            "position": current_user['position']
        }
    }

# Routes pour les offres d'emploi
@app.post("/api/job-offers")
async def create_job_offer(
    title: str = Form(...),
    department: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(...),  # JSON string
    required_experience: str = Form(...)
):
    """Crée une nouvelle offre d'emploi"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    try:
        skills = json.loads(required_skills)
        job_id = db.create_job_offer(
            title=title,
            department=department,
            description=description,
            required_skills=skills,
            required_experience=required_experience,
            created_by=current_user['id']
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "message": "Offre d'emploi créée avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/job-offers")
async def get_job_offers():
    """Récupère les offres d'emploi"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    offers = db.get_job_offers(current_user['id'])
    return {"success": True, "offers": offers}

# Routes pour les CVs
@app.post("/api/cvs/upload")
async def upload_cv(file: UploadFile = File(...)):
    """Upload un CV"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    # Vérifier le type de fichier
    allowed_types = ['.pdf', '.doc', '.docx']
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail="Type de fichier non supporté")
    
    # Générer un nom de fichier unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join("uploads", filename)
    
    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Enregistrer en base de données
    cv_id = db.create_cv(
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file.size,
        uploaded_by=current_user['id']
    )
    
    return {
        "success": True,
        "cv_id": cv_id,
        "filename": file.filename,
        "message": "CV uploadé avec succès"
    }

@app.get("/api/cvs")
async def get_cvs():
    """Récupère les CVs"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    cvs = db.get_cvs(current_user['id'])
    return {"success": True, "cvs": cvs}

@app.delete("/api/cvs/{cv_id}")
async def delete_cv(cv_id: int):
    """Supprime un CV"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    # Récupérer les informations du CV
    cvs = db.get_cvs(current_user['id'])
    cv = next((c for c in cvs if c['id'] == cv_id), None)
    
    if not cv:
        raise HTTPException(status_code=404, detail="CV non trouvé")
    
    # Supprimer le fichier
    if os.path.exists(cv['file_path']):
        os.remove(cv['file_path'])
    
    # Supprimer de la base de données
    with db.db_path as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cvs WHERE id = ? AND uploaded_by = ?", (cv_id, current_user['id']))
    
    return {"success": True, "message": "CV supprimé avec succès"}

# Routes pour les analyses
@app.post("/api/analyses")
async def create_analysis(
    job_offer_id: int = Form(...),
    cv_id: int = Form(...),
    overall_score: float = Form(...),
    skills_score: float = Form(...),
    experience_score: float = Form(...),
    education_score: float = Form(...),
    soft_skills_score: float = Form(...),
    analysis_details: str = Form(...)  # JSON string
):
    """Crée une nouvelle analyse"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    try:
        details = json.loads(analysis_details)
        analysis_id = db.create_analysis(
            job_offer_id=job_offer_id,
            cv_id=cv_id,
            overall_score=overall_score,
            skills_score=skills_score,
            experience_score=experience_score,
            education_score=education_score,
            soft_skills_score=soft_skills_score,
            analysis_details=details
        )
        
        return {
            "success": True,
            "analysis_id": analysis_id,
            "message": "Analyse créée avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analyses")
async def get_analyses():
    """Récupère les analyses"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    analyses = db.get_analyses(current_user['id'])
    return {"success": True, "analyses": analyses}

# Routes pour les sessions d'analyse
@app.post("/api/analysis-sessions")
async def create_analysis_session(
    session_name: str = Form(...),
    job_offer_id: int = Form(...)
):
    """Crée une nouvelle session d'analyse"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    session_id = db.create_analysis_session(
        session_name=session_name,
        job_offer_id=job_offer_id,
        created_by=current_user['id']
    )
    
    return {
        "success": True,
        "session_id": session_id,
        "message": "Session d'analyse créée avec succès"
    }

@app.post("/api/analysis-sessions/{session_id}/cvs")
async def add_cv_to_session(session_id: int, cv_id: int = Form(...)):
    """Ajoute un CV à une session"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    db.add_cv_to_session(session_id, cv_id)
    return {"success": True, "message": "CV ajouté à la session"}

@app.get("/api/analysis-sessions/{session_id}/cvs")
async def get_session_cvs(session_id: int):
    """Récupère les CVs d'une session"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    cvs = db.get_session_cvs(session_id)
    return {"success": True, "cvs": cvs}

# Routes pour les paramètres
@app.get("/api/settings")
async def get_settings():
    """Récupère les paramètres de l'utilisateur"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    settings = db.get_user_settings(current_user['id'])
    return {"success": True, "settings": settings}

@app.put("/api/settings")
async def update_settings(
    theme: str = Form(...),
    language: str = Form(...),
    email_notifications: bool = Form(...),
    push_notifications: bool = Form(...)
):
    """Met à jour les paramètres de l'utilisateur"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    settings = {
        'theme': theme,
        'language': language,
        'email_notifications': email_notifications,
        'push_notifications': push_notifications
    }
    
    db.update_user_settings(current_user['id'], settings)
    return {"success": True, "message": "Paramètres mis à jour avec succès"}

# Routes pour les statistiques
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Récupère les statistiques du dashboard"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    stats = db.get_dashboard_stats(current_user['id'])
    return {"success": True, "stats": stats}

# Routes pour les fichiers
@app.get("/api/files/{filename}")
async def get_file(filename: str):
    """Récupère un fichier"""
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

# Route de santé
@app.get("/api/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
