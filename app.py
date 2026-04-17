"""
Application Flask pour un site communautaire autour de l'Astronomie.
Ce fichier contient :
- La configuration de Flask et de la base de données MySQL
- Le système d'authentification (inscription, connexion, déconnexion)
- Les routes principales du site (Appareils, Télescopes, Photographies)
- Le chargement initial des données (seed)
"""

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests

# Import des modèles SQLAlchemy
from models import db, User, Camera, Telescope, Photo, Thread, Post


# ----------------------------------------------------------------------
# Configuration de l'application Flask
# ----------------------------------------------------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = "change_me"  # Clé secrète pour les sessions
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/astro_community"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ----------------------------------------------------------------------
# Configuration du système d'authentification Flask-Login
# ----------------------------------------------------------------------

login_manager = LoginManager()
login_manager.login_view = "login"  # Page affichée si un utilisateur non connecté tente d'accéder à une page protégée
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Chargement d'un utilisateur depuis la base de données."""
    return User.query.get(int(user_id))

# ----------------------------------------------------------------------
# Initialisation automatique de la base de données et insertion des données
# ----------------------------------------------------------------------

@app.before_request
def create_tables_and_seed():
    """
    Création automatique des tables au premier lancement de l'application.
    Insertion des données de démonstration si la base est vide.
    """
    if not hasattr(app, "db_initialized"):
        db.create_all()
        seed_data()
        app.db_initialized = True

def seed_data():
    """
    Insertion des données initiales (appareils photo, télescopes, photographies).
    Cette fonction ne s'exécute qu'une seule fois.
    """
    if User.query.first():
        return

    cameras = [
        Camera(marque="Canon", modele="EOS 2000D", date_sortie="2018", score=3,
               categorie="Amateur", url_image="images/appareil/canonEOS2000D.jpg"),
        Camera(marque="Sony", modele="A7 III", date_sortie="2018", score=5,
               categorie="Amateur sérieux", url_image="images/appareil/sonyALPHA.jpg"),
        Camera(marque="Canon", modele="EOS R5", date_sortie="2020", score=5,
               categorie="Professionnel", url_image="images/appareil/canon.jpg"),
    ]

    telescopes = [
        Telescope(marque="Celestron", modele="FirstScope", date_sortie="2010", score=3,
                  categorie="Enfants", url_image="images/telescope/enfant.PNG"),
        Telescope(marque="Sky-Watcher", modele="Star Discovery", date_sortie="2015", score=4,
                  categorie="Automatisés", url_image="images/telescope/automatisee.PNG"),
        Telescope(marque="Meade", modele="LX200", date_sortie="2012", score=5,
                  categorie="Complets", url_image="images/telescope/complets.PNG"),
    ]

    photos = [
        Photo(titre="Voie Lactée", url_image="images/photographie/voieLactee.jpg"),
        Photo(titre="Nébuleuse d'Orion", url_image="images/photographie/nebuluse.jpg"),
        Photo(titre="Lune", url_image="images/photographie/lune.jpg"),
    ]

    db.session.add_all(cameras + telescopes + photos)
    db.session.commit()

# ----------------------------------------------------------------------
# Authentification : inscription, connexion, déconnexion
# ----------------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Page d'inscription.
    Permet à un utilisateur de créer un compte avant d'accéder au site.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        # Vérification du nom d'utilisateur
        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.", "danger")
            return redirect(url_for("register"))

        # Vérification de l'email
        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé. Veuillez en choisir un autre.", "danger")
            return redirect(url_for("register"))

        # Vérification des mots de passe
        if password != confirm:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for("register"))

        # Hashage du mot de passe
        hashed = generate_password_hash(password)

        # Création de l'utilisateur
        user = User(username=username, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Page de connexion.
    Permet à un utilisateur existant d'accéder aux pages protégées.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        # Vérification des identifiants
        if not user or not check_password_hash(user.password_hash, password):
            flash("Identifiants incorrects.", "danger")
            return redirect(url_for("login"))

        # Connexion de l'utilisateur
        login_user(user)
        session["user_id"] = user.id

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Déconnexion de l'utilisateur.
    Retour à la page d'accueil publique.
    """
    logout_user()
    session.pop("user_id", None)
    return redirect(url_for("index"))

# ----------------------------------------------------------------------
# Pages principales du site
# ----------------------------------------------------------------------

@app.route("/")
def index():
    """Page d'accueil publique."""
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Page d'accueil après connexion."""
    return render_template("dashboard.html", user=current_user)


@app.route("/appareils")
@login_required
def appareils():
    """Liste des appareils photo classés par catégories."""
    cameras = Camera.query.all()
    return render_template("appareils.html", cameras=cameras)


@app.route("/telescopes")
@login_required
def telescopes():
    """Liste des télescopes classés par catégories."""
    telescopes = Telescope.query.all()
    return render_template("telescopes.html", telescopes=telescopes)


@app.route("/photos")
@login_required
def photos():
    """Liste des photographies."""
    photos = Photo.query.all()
    return render_template("photos.html", photos=photos)


@app.route("/profil")
@login_required
def profil():
    """Page de profil utilisateur."""
    return render_template("profil.html", user=current_user)

# ----------------------------------------------------------------------
# Page Actualités (API NASA APOD)
# ----------------------------------------------------------------------

@app.route("/actualites")
@login_required
def actualites():
    """
    Page affichant l'image astronomique du jour via l'API NASA APOD.
    """
    try:
        url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        data = requests.get(url).json()
    except:
        data = {"title": "Erreur API", "explanation": "Impossible de contacter la NASA."}

    return render_template("actualites.html", data=data)

# ----------------------------------------------------------------------
# Pages Détails : Appareil Photo & Télescope
# ----------------------------------------------------------------------

@app.route("/appareil/<int:id>")
@login_required
def details_appareil(id):
    """
    Page de détails pour un appareil photo.
    Affiche toutes les informations d'un appareil sélectionné.
    """
    appareil = Camera.query.get_or_404(id)
    return render_template("details_appareil.html", appareil=appareil)


@app.route("/telescope/<int:id>")
@login_required
def details_telescope(id):
    """
    Page de détails pour un télescope.
    Affiche toutes les informations d'un télescope sélectionné.
    """
    telescope = Telescope.query.get_or_404(id)
    return render_template("details_telescope.html", telescope=telescope)

# ----------------------------------------------------------------------
# Forum : liste des fils de discussion
# ----------------------------------------------------------------------

@app.route("/forum")
@login_required
def forum():
    """
    Page principale du forum.
    Affiche la liste des fils de discussion.
    """
    threads = Thread.query.order_by(Thread.date_creation.desc()).all()
    return render_template("forum.html", threads=threads)


# ----------------------------------------------------------------------
# Création d'un nouveau fil de discussion
# ----------------------------------------------------------------------

@app.route("/forum/new", methods=["GET", "POST"])
@login_required
def new_thread():
    """
    Page permettant de créer un nouveau fil de discussion.
    """
    if request.method == "POST":
        titre = request.form["titre"]

        thread = Thread(titre=titre, user_id=current_user.id)
        db.session.add(thread)
        db.session.commit()

        return redirect(url_for("forum"))

    return render_template("new_thread.html")


# ----------------------------------------------------------------------
# Page d'un fil de discussion
# ----------------------------------------------------------------------

@app.route("/forum/thread/<int:id>")
@login_required
def thread(id):
    """
    Affiche un fil de discussion et ses messages.
    """
    thread = Thread.query.get_or_404(id)
    posts = Post.query.filter_by(thread_id=id).order_by(Post.date_post.asc()).all()
    return render_template("thread.html", thread=thread, posts=posts)


# ----------------------------------------------------------------------
# Répondre à un fil de discussion
# ----------------------------------------------------------------------

@app.route("/forum/thread/<int:id>/reply", methods=["POST"])
@login_required
def reply(id):
    """
    Ajout d'un message dans un fil de discussion.
    """
    contenu = request.form["contenu"]

    post = Post(contenu=contenu, user_id=current_user.id, thread_id=id)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("thread", id=id))

# ----------------------------------------------------------------------
# Lancement de l'application
# ----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
