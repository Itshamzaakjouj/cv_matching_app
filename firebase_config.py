"""
Configuration Firebase pour l'authentification
"""
import pyrebase
import json

# Charger la configuration depuis le fichier firebase_keys.json
with open('firebase_keys.json', 'r') as f:
    config = json.load(f)

# Ajouter l'URL de la base de données si elle n'existe pas
if 'databaseURL' not in config:
    config['databaseURL'] = ''

# Initialisation de Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

class FirebaseAuth:
    @staticmethod
    def sign_in(email, password):
        try:
            # Connexion avec email/mot de passe
            user = auth.sign_in_with_email_and_password(email, password)
            # Obtenir les informations fraîches de l'utilisateur
            user_info = auth.get_account_info(user['idToken'])
            return user_info
        except Exception as e:
            error_message = str(e)
            if "INVALID_PASSWORD" in error_message:
                raise Exception("Mot de passe incorrect")
            elif "EMAIL_NOT_FOUND" in error_message:
                raise Exception("Email non trouvé")
            else:
                raise Exception("Erreur de connexion")

    @staticmethod
    def sign_up(email, password):
        try:
            # Création du compte avec email/mot de passe
            user = auth.create_user_with_email_and_password(email, password)
            # Obtenir les informations fraîches de l'utilisateur
            user_info = auth.get_account_info(user['idToken'])
            return user_info
        except Exception as e:
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                raise Exception("Cet email est déjà utilisé")
            elif "WEAK_PASSWORD" in error_message:
                raise Exception("Le mot de passe doit contenir au moins 6 caractères")
            elif "INVALID_EMAIL" in error_message:
                raise Exception("Format d'email invalide")
            else:
                raise Exception(f"Erreur lors de la création du compte : {str(e)}")

    @staticmethod
    def reset_password(email):
        try:
            auth.send_password_reset_email(email)
            return True
        except Exception as e:
            raise Exception("Erreur lors de la réinitialisation du mot de passe")

# Instance unique de FirebaseAuth
firebase_auth = FirebaseAuth()