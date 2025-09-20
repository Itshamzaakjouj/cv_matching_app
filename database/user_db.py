import json
import os
from pathlib import Path

class UserDatabase:
    def __init__(self):
        self.db_path = Path("database/users.json")
        self._ensure_db_exists()
        
    def _ensure_db_exists(self):
        """Crée le fichier de base de données s'il n'existe pas"""
        try:
            # Créer le dossier database s'il n'existe pas
            if not self.db_path.parent.exists():
                os.makedirs(self.db_path.parent)
            
            # Créer le fichier users.json s'il n'existe pas
            if not self.db_path.exists():
                with open(self.db_path, 'w', encoding='utf-8') as f:
                    json.dump({"users": {}}, f, indent=4)
            else:
                # Vérifier que le fichier est un JSON valide
                try:
                    with open(self.db_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    # Si le fichier est corrompu, le recréer
                    with open(self.db_path, 'w', encoding='utf-8') as f:
                        json.dump({"users": {}}, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données : {str(e)}")
            raise
    
    def load_users(self):
        """Charge tous les utilisateurs de la base de données"""
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)["users"]
    
    def save_users(self, users):
        """Sauvegarde les utilisateurs dans la base de données"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump({"users": users}, f, indent=4)
    
    def add_user(self, email, password, full_name=None):
        """Ajoute un nouvel utilisateur"""
        try:
            # Validation des types
            if not isinstance(email, str) or not isinstance(password, str):
                return False, "Email et mot de passe doivent être des chaînes de caractères"
            
            if full_name is not None and not isinstance(full_name, str):
                return False, "Le nom complet doit être une chaîne de caractères"
            
            # S'assurer que le dossier database existe
            if not os.path.exists('database'):
                os.makedirs('database')
            
            # Charger les utilisateurs existants
            users = self.load_users()
            
            # Vérifier si l'email existe déjà
            if email in users:
                return False, "Cet email est déjà utilisé."
            
            # Créer le nouvel utilisateur
            users[email] = {
                "password": str(password),
                "full_name": str(full_name) if full_name else None,
                "created_at": str(Path.ctime(Path.cwd()))
            }
            
            # Sauvegarder dans le fichier
            self.save_users(users)
            return True, "Compte créé avec succès!"
            
        except Exception as e:
            print(f"Erreur détaillée lors de la création du compte : {str(e)}")
            return False, "Erreur lors de la création du compte. Veuillez réessayer."
    
    def verify_user(self, email, password):
        """Vérifie les identifiants d'un utilisateur"""
        users = self.load_users()
        if email not in users:
            return False, "Cet email n'est pas enregistré."
        
        if users[email]["password"] != password:
            return False, "Mot de passe incorrect."
        
        return True, users[email]
    
    def user_exists(self, email):
        """Vérifie si un utilisateur existe"""
        users = self.load_users()
        return email in users
    
    def get_user_info(self, email):
        """Récupère les informations d'un utilisateur"""
        users = self.load_users()
        return users.get(email, None)
    
    def update_user(self, email, updates):
        """Met à jour les informations d'un utilisateur"""
        users = self.load_users()
        if email not in users:
            return False, "Utilisateur non trouvé."
        
        users[email].update(updates)
        self.save_users(users)
        return True, "Informations mises à jour avec succès!"
