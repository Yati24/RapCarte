from flask import Flask, jsonify, redirect, render_template, request, session
from extensions import db, migrate, login_manager, bcrypt
from config import Config



# ----- INIT APP -----
app = Flask(__name__)
app.config.from_object("config.Config")

# ----- EXTENSIONS -----
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
bcrypt.init_app(app)

# ----- MODELS -----
from models import User, Rapper, Vote

# ----- ROUTES -----
@app.route("/")
def index():
    return "Rap Carte ✅"


# ----- RUN -----
if __name__ == "__main__":
    app.run(debug=True)
