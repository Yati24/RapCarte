from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    rappers_added = db.relationship('Rapper', backref='creator', lazy=True)
    votes = db.relationship('Vote', backref='voter', lazy=True)

class Rapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    spotify_url = db.Column(db.String(255))
    votes = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    votes_list = db.relationship('Vote', backref='rapper', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rapper_id = db.Column(db.Integer, db.ForeignKey('rapper.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'rapper_id', name='unique_user_rapper_vote'),)
