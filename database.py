#!/usr/bin/env python3
"""
TalentScope - Gestion de la Base de Données
Ministère de l'Économie et des Finances
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class TalentScopeDB:
    def __init__(self, db_path: str = "talentscope.db"):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise les tables de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    department TEXT,
                    position TEXT,
                    phone TEXT,
                    avatar_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Table des offres d'emploi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_offers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    department TEXT NOT NULL,
                    description TEXT NOT NULL,
                    required_skills TEXT, -- JSON array
                    required_experience TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Table des CVs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cvs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    uploaded_by INTEGER,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'uploaded',
                    FOREIGN KEY (uploaded_by) REFERENCES users (id)
                )
            ''')
            
            # Table des analyses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_offer_id INTEGER,
                    cv_id INTEGER,
                    overall_score REAL,
                    skills_score REAL,
                    experience_score REAL,
                    education_score REAL,
                    soft_skills_score REAL,
                    analysis_details TEXT, -- JSON
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'completed',
                    FOREIGN KEY (job_offer_id) REFERENCES job_offers (id),
                    FOREIGN KEY (cv_id) REFERENCES cvs (id)
                )
                ''')
            
            # Table des sessions d'analyse
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    job_offer_id INTEGER,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (job_offer_id) REFERENCES job_offers (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # Table des CVs dans une session
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS session_cvs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    cv_id INTEGER,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES analysis_sessions (id),
                    FOREIGN KEY (cv_id) REFERENCES cvs (id)
                )
            ''')
            
            # Table des paramètres de l'application
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    theme TEXT DEFAULT 'light',
                    language TEXT DEFAULT 'fr',
                    email_notifications BOOLEAN DEFAULT 1,
                    push_notifications BOOLEAN DEFAULT 1,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            self.create_default_data()
    
    def create_default_data(self):
        """Crée les données par défaut"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Vérifier si des utilisateurs existent déjà
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Créer les utilisateurs par défaut
                default_users = [
                    ("akjouj17@gmail.com", "Hamza12345", "Akjouj Hamza", "admin", "Informatique", "Développeur Senior"),
                    ("elhafsaghazouani@gmail.com", "Hafsa2003", "Hafsa El Ghazouani", "user", "Ressources Humaines", "Analyste RH")
                ]
                
                for email, password, name, role, dept, pos in default_users:
                    cursor.execute('''
                        INSERT INTO users (email, password, name, role, department, position)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (email, password, name, role, dept, pos))
            
            conn.commit()
    
    # Méthodes pour les utilisateurs
    def create_user(self, email: str, password: str, name: str, role: str = "user", 
                   department: str = None, position: str = None) -> int:
        """Crée un nouvel utilisateur"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (email, password, name, role, department, position)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, password, name, role, department, position))
            return cursor.lastrowid
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Récupère un utilisateur par email"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_user_login(self, user_id: int):
        """Met à jour la dernière connexion"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            ''', (user_id,))
    
    # Méthodes pour les offres d'emploi
    def create_job_offer(self, title: str, department: str, description: str, 
                        required_skills: List[str], required_experience: str, 
                        created_by: int) -> int:
        """Crée une nouvelle offre d'emploi"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO job_offers (title, department, description, required_skills, required_experience, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, department, description, json.dumps(required_skills), required_experience, created_by))
            return cursor.lastrowid
    
    def get_job_offers(self, user_id: int = None) -> List[Dict]:
        """Récupère les offres d'emploi"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT * FROM job_offers WHERE created_by = ? ORDER BY created_at DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT * FROM job_offers ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # Méthodes pour les CVs
    def create_cv(self, filename: str, original_filename: str, file_path: str, 
                 file_size: int, uploaded_by: int) -> int:
        """Enregistre un nouveau CV"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cvs (filename, original_filename, file_path, file_size, uploaded_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, original_filename, file_path, file_size, uploaded_by))
            return cursor.lastrowid
    
    def get_cvs(self, user_id: int = None) -> List[Dict]:
        """Récupère les CVs"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT * FROM cvs WHERE uploaded_by = ? ORDER BY uploaded_at DESC
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT * FROM cvs ORDER BY uploaded_at DESC
                ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # Méthodes pour les analyses
    def create_analysis(self, job_offer_id: int, cv_id: int, overall_score: float,
                       skills_score: float, experience_score: float, education_score: float,
                       soft_skills_score: float, analysis_details: Dict) -> int:
        """Crée une nouvelle analyse"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analyses (job_offer_id, cv_id, overall_score, skills_score, 
                                    experience_score, education_score, soft_skills_score, analysis_details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (job_offer_id, cv_id, overall_score, skills_score, experience_score, 
                  education_score, soft_skills_score, json.dumps(analysis_details)))
            return cursor.lastrowid
    
    def get_analyses(self, user_id: int = None) -> List[Dict]:
        """Récupère les analyses"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT a.*, jo.title as job_title, c.original_filename as cv_name,
                       u.name as analyzed_by
                FROM analyses a
                JOIN job_offers jo ON a.job_offer_id = jo.id
                JOIN cvs c ON a.cv_id = c.id
                JOIN users u ON jo.created_by = u.id
            '''
            
            if user_id:
                query += " WHERE jo.created_by = ?"
                cursor.execute(query + " ORDER BY a.analyzed_at DESC", (user_id,))
            else:
                cursor.execute(query + " ORDER BY a.analyzed_at DESC")
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # Méthodes pour les sessions d'analyse
    def create_analysis_session(self, session_name: str, job_offer_id: int, created_by: int) -> int:
        """Crée une nouvelle session d'analyse"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analysis_sessions (session_name, job_offer_id, created_by)
                VALUES (?, ?, ?)
            ''', (session_name, job_offer_id, created_by))
            return cursor.lastrowid
    
    def add_cv_to_session(self, session_id: int, cv_id: int):
        """Ajoute un CV à une session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO session_cvs (session_id, cv_id)
                VALUES (?, ?)
            ''', (session_id, cv_id))
    
    def get_session_cvs(self, session_id: int) -> List[Dict]:
        """Récupère les CVs d'une session"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.* FROM cvs c
                JOIN session_cvs sc ON c.id = sc.cv_id
                WHERE sc.session_id = ?
                ORDER BY sc.added_at
            ''', (session_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    # Méthodes pour les paramètres
    def get_user_settings(self, user_id: int) -> Dict:
        """Récupère les paramètres d'un utilisateur"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_settings WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else {
                'theme': 'light',
                'language': 'fr',
                'email_notifications': True,
                'push_notifications': True
            }
    
    def update_user_settings(self, user_id: int, settings: Dict):
        """Met à jour les paramètres d'un utilisateur"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO app_settings 
                (user_id, theme, language, email_notifications, push_notifications)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, settings.get('theme', 'light'), settings.get('language', 'fr'),
                  settings.get('email_notifications', True), settings.get('push_notifications', True)))
    
    # Méthodes de statistiques
    def get_dashboard_stats(self, user_id: int = None) -> Dict:
        """Récupère les statistiques du dashboard"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Nombre d'analyses
            if user_id:
                cursor.execute('''
                    SELECT COUNT(*) FROM analyses a
                    JOIN job_offers jo ON a.job_offer_id = jo.id
                    WHERE jo.created_by = ?
                ''', (user_id,))
            else:
                cursor.execute("SELECT COUNT(*) FROM analyses")
            analyses_count = cursor.fetchone()[0]
            
            # Nombre de CVs traités
            if user_id:
                cursor.execute('''
                    SELECT COUNT(DISTINCT a.cv_id) FROM analyses a
                    JOIN job_offers jo ON a.job_offer_id = jo.id
                    WHERE jo.created_by = ?
                ''', (user_id,))
            else:
                cursor.execute("SELECT COUNT(DISTINCT cv_id) FROM analyses")
            cvs_processed = cursor.fetchone()[0]
            
            # Score moyen
            if user_id:
                cursor.execute('''
                    SELECT AVG(a.overall_score) FROM analyses a
                    JOIN job_offers jo ON a.job_offer_id = jo.id
                    WHERE jo.created_by = ?
                ''', (user_id,))
            else:
                cursor.execute("SELECT AVG(overall_score) FROM analyses")
            avg_score = cursor.fetchone()[0] or 0
            
            # Taux de réussite (scores > 70%)
            if user_id:
                cursor.execute('''
                    SELECT COUNT(*) FROM analyses a
                    JOIN job_offers jo ON a.job_offer_id = jo.id
                    WHERE jo.created_by = ? AND a.overall_score >= 70
                ''', (user_id,))
                total_analyses = analyses_count
            else:
                cursor.execute("SELECT COUNT(*) FROM analyses WHERE overall_score >= 70")
                total_analyses = analyses_count
            
            success_rate = (cursor.fetchone()[0] / total_analyses * 100) if total_analyses > 0 else 0
            
            return {
                'analyses_count': analyses_count,
                'cvs_processed': cvs_processed,
                'avg_score': round(avg_score, 1),
                'success_rate': round(success_rate, 1)
            }

# Instance globale de la base de données
db = TalentScopeDB()
