import os
from dotenv import load_dotenv

# charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    # clé secrète pour la session
    SECRET_KEY = os.getenv("SECRET_KEY")
    # configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # désactiver le suivi des modifications de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
