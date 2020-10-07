from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    isAsker = db.Column(db.Boolean, default=True, nullable=False)
    isConfirmer = db.Column(db.Boolean, default=False, nullable=False)
    isSuperAdmin = db.Column(db.Boolean, default=False, nullable=False)
    
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(500), unique=True)
    description = db.Column(db.String(2000))
    duedate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    minPrice = db.Column(db.Integer)
    maxPrice = db.Column(db.Integer)
    dateCreate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dateUpdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    
class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(500), unique=True)
    state = db.Column(db.String(500))
