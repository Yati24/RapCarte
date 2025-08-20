from flask import Flask, jsonify, redirect, render_template, request, session
from extensions import db, migrate, login_manager, bcrypt
from config import Config

from models import User, Rapper, Vote


# ----- INIT APP -----
app = Flask(__name__)
app.config.from_object("config.Config")

# ----- EXTENSIONS -----
db.init_app(app)
migrate.init_app(app, db)

# pas activé pour éviter les erreurs, pas encore de login
# login_manager.init_app(app)

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

@app.route("/contribute")
def contribute():
    return render_template("contribute.html", title="Contribute")

@app.route("/login")
def login():
    return render_template("login.html", title="Login")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html", title="Privacy Policy")


# ----- RUN -----
if __name__ == "__main__":
    app.run(debug=True)
