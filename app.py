from flask import Flask, jsonify, redirect, render_template, request, session, url_for, flash
from extensions import db, migrate, login_manager, bcrypt
from config import Config
from flask_login import login_user, logout_user, login_required
from models import User, Rapper, Vote
from flask_bcrypt import Bcrypt

# ----- INIT APP -----
app = Flask(__name__)
app.config.from_object("config.Config")

# ----- EXTENSIONS -----
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
bcrypt.init_app(app)

# ----- MODELS -----
from models import User, Rapper, Vote

# ----- ROUTES -----
@app.route("/")
def index():
    rappers = Rapper.query.all()
    return render_template("map.html", rappers=rappers)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/contribute", methods=["GET", "POST"])
@login_required
def contribute():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        spotify_url = request.form.get("spotify")

        if not name or not lat or not lon:
            flash("Veuillez remplir tous les champs obligatoires.", "warning")
            return redirect(url_for("contribute"))

        new_rapper = Rapper(name=name, description=description, lat=float(lat), lon=float(lon), spotify_url=spotify_url, created_by='0')
        db.session.add(new_rapper)
        db.session.commit()
        flash("Rappeur ajouté avec succès !", "success")
        return redirect(url_for("index"))
    
    rappers = Rapper.query.all()
    return render_template("contribute.html", rappers=rappers, title="Contribute")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return redirect(url_for("login"))

        login_user(user)   # you can pass remember=bool(...) si tu ajoutes une checkbox
        return redirect(url_for("index"))

    return render_template("login.html", title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        print(">>> REGISTER POST reçu")   # DEBUG
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        country  = request.form.get("country", "").strip()
        city     = request.form.get("city", "").strip()
        print(">>> FORM DATA :", username, email, password, country, city)

        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            print(">>> Utilisateur déjà existant :", existing_user.username, existing_user.email)
            flash("Username ou email déjà utilisé.", "warning")
            return redirect(url_for("register"))
        
        # Création utilisateur
        user = User(username=username, email=email, country=country, city=city)
        user.set_password(password)   # bcrypt via ta méthode
        print(">>> Mot de passe haché :", user.password)
        db.session.add(user)

        db.session.commit()
        print(">>> Nouvel utilisateur ajouté :", user.username, user.email)

        # Login auto
        login_user(user)
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("index"))

    return render_template("register.html", title="Register")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", title="Privacy Policy")





# ----- ADMIN CRUD -----

@app.route("/admin")
@login_required
def admin_index():
    users = User.query.all()
    rappers = Rapper.query.all()
    return render_template("admin.html", users=users, rappers=rappers)


# ----- USER CRUD -----
@app.route("/admin/user/create", methods=["POST"])
@login_required
def create_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    city = request.form.get("city")
    country = request.form.get("country")
    user = User(username=username, email=email, country=country, city=city)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("admin_index"))

@app.route("/admin/user/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin_index"))


# ----- RAPPER CRUD -----
@app.route("/admin/rapper/create", methods=["POST"])
@login_required
def create_rapper():
    name = request.form.get("name")
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    description = request.form.get("description")
    spotify_url = request.form.get("spotify")
    rapper = Rapper(name=name, lat=lat, lon=lon, description=description, spotify_url=spotify_url)
    db.session.add(rapper)
    db.session.commit()
    return redirect(url_for("admin_index"))

@app.route("/admin/rapper/delete/<int:rapper_id>")
@login_required
def delete_rapper(rapper_id):
    rapper = Rapper.query.get(rapper_id)
    if rapper:
        db.session.delete(rapper)
        db.session.commit()
    return redirect(url_for("admin_index"))

# Afficher le formulaire de modification
@app.route("/admin/user/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.country = request.form.get("country")
        user.city = request.form.get("city")
        password = request.form.get("password")
        if password:  # si un nouveau mot de passe est fourni
            user.set_password(password)
        db.session.commit()
        return redirect(url_for("admin_index"))
    return render_template("edit_user.html", user=user)

@app.route("/admin/rapper/edit/<int:rapper_id>", methods=["GET", "POST"])
@login_required
def edit_rapper(rapper_id):
    rapper = Rapper.query.get_or_404(rapper_id)
    if request.method == "POST":
        rapper.name = request.form.get("name")
        rapper.lat = float(request.form.get("lat"))
        rapper.lon = float(request.form.get("lon"))
        rapper.description = request.form.get("description")
        rapper.spotify_url = request.form.get("spotify")
        db.session.commit()
        return redirect(url_for("admin_index"))
    return render_template("edit_rapper.html", rapper=rapper)


login_manager.login_view = "login"  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----- RUN -----
if __name__ == "__main__":
    app.run(debug=True)
