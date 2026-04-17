"""
Définition des modèles SQLAlchemy utilisés dans l'application.
Chaque classe correspond à une table MySQL.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Instance SQLAlchemy utilisée dans toute l'application
db = SQLAlchemy()

# ----------------------------------------------------------------------
# Modèle Utilisateur
# ----------------------------------------------------------------------

class User(UserMixin, db.Model):
    """
    Table des utilisateurs.
    Utilisée pour l'authentification via Flask-Login.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Nom d'utilisateur unique (obligatoire)
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Email unique (obligatoire)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Mot de passe hashé (obligatoire)
    password_hash = db.Column(db.String(255), nullable=False)


# ----------------------------------------------------------------------
# Modèle Appareil Photo
# ----------------------------------------------------------------------

class Camera(db.Model):
    """
    Table des appareils photo.
    Chaque appareil possède :
    - une marque
    - un modèle
    - une date de sortie
    - un score (1 à 5)
    - une catégorie (Amateur, Amateur sérieux, Professionnel)
    - un chemin d'image stocké localement
    """
    __tablename__ = "cameras"

    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(80), nullable=False)
    modele = db.Column(db.String(80), nullable=False)
    date_sortie = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    url_image = db.Column(db.String(255), nullable=False)


# ----------------------------------------------------------------------
# Modèle Télescope
# ----------------------------------------------------------------------

class Telescope(db.Model):
    """
    Table des télescopes.
    Chaque télescope possède :
    - une marque
    - un modèle
    - une date de sortie
    - un score (1 à 5)
    - une catégorie (Enfants, Automatisés, Complets)
    - un chemin d'image stocké localement
    """
    __tablename__ = "telescopes"

    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(80), nullable=False)
    modele = db.Column(db.String(80), nullable=False)
    date_sortie = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    url_image = db.Column(db.String(255), nullable=False)


# ----------------------------------------------------------------------
# Modèle Photographie
# ----------------------------------------------------------------------

class Photo(db.Model):
    """
    Table des photographies affichées dans la galerie.
    Chaque photo possède :
    - un titre
    - un chemin d'image stocké localement
    """
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(120), nullable=False)
    url_image = db.Column(db.String(255), nullable=False)

# ----------------------------------------------------------------------
# Modèle Forum : Fil de discussion
# ----------------------------------------------------------------------

class Thread(db.Model):
    """
    Table des fils de discussion du forum.
    Chaque fil possède :
    - un titre
    - un auteur (utilisateur)
    - une date de création
    """
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date_creation = db.Column(db.DateTime, server_default=db.func.now())

    # Relation : un fil contient plusieurs posts
    posts = db.relationship("Post", backref="thread", cascade="all, delete")


# ----------------------------------------------------------------------
# Modèle Forum : Messages dans un fil
# ----------------------------------------------------------------------

class Post(db.Model):
    """
    Table des messages du forum.
    Chaque message possède :
    - un contenu
    - un auteur
    - une date
    - un lien vers le fil auquel il appartient
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.id"), nullable=False)
    date_post = db.Column(db.DateTime, server_default=db.func.now())
