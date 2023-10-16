from app import db
from datetime import datetime

# Define your SQLAlchemy models here

class Laboratory(db.Model):
    lab_id = db.Column(db.Integer, primary_key=True)
    lab_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    supervisor = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

class Equipment(db.Model):
    equipment_id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('laboratory.lab_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    purchase_date = db.Column(db.Date)
    maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    lab_id = db.Column(db.Integer, db.ForeignKey('laboratory.lab_id'), nullable=False)
    lab = db.relationship('Laboratory', backref=db.backref('equipment', lazy=True))

class Researcher(db.Model):
    researcher_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    lab = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

class ChemicalSubstance(db.Model):
    substance_id = db.Column(db.Integer, primary_key=True)
    substance_name = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    chemical_formula = db.Column(db.String(100))
    hazard_level = db.Column(db.String(50))
    storage_conditions = db.Column(db.String(200))
    purchase_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

class BiologicalSubstance(db.Model):
    substance_id = db.Column(db.Integer, primary_key=True)
    substance_name = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    organism_type = db.Column(db.String(100))
    hazard_level = db.Column(db.String(50))
    storage_conditions = db.Column(db.String(200))
    acquisition_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

