from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# Define your SQLAlchemy models here

class Laboratory(db.Model):
    lab_id = db.Column(db.String(250), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    supervisor = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    purchase_date = db.Column(db.Date)
    maintenance_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    lab = db.Column(db.String(100), nullable=False)
    qr_codes = db.relationship('QRCode', backref='qr_code_equipment', lazy=True, overlaps="qr_code_equipment")
    UUID = db.Column(db.String(100))

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
    id = db.Column(db.Integer, primary_key=True)
    substance_name = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    chemical_formula = db.Column(db.String(100))
    hazard_level = db.Column(db.String(50))
    storage_conditions = db.Column(db.String(200))
    storage_place= db.Column(db.String(200))
    purchase_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    cid = db.Column(db.String(100))
    cas = db.Column(db.String(100))
    UUID = db.Column(db.String(100))
    #qr_codes = relationship('QRCode', backref='qr_codes_chemical', lazy=True, primaryjoin='ChemicalSubstance.id == QRCode.chemical_substance_id')
    qr_codes = db.relationship('QRCode', backref='qr_code_chemical', lazy=True, overlaps="qr_code_chemical")
    safety_sheet = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_data = db.Column(db.String(255))

    # Foreign keys for each type of substance
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    chemical_substance_id = db.Column(db.Integer, db.ForeignKey('chemical_substance.id'))
    biological_substance_id = db.Column(db.Integer, db.ForeignKey('biological_substance.id'))

    # Relationships with each type of substance
    equipment = db.relationship('Equipment', backref='qr_code_equipment', foreign_keys=[equipment_id],overlaps="qr_code_equipment")
    chemical_substance = db.relationship('ChemicalSubstance', backref='qr_codes_chemical', lazy=True,overlaps="qr_codes_chemical")
    biological_substance = db.relationship('BiologicalSubstance', backref='qr_codes_biological', lazy=True,overlaps="qr_codes_biological")

class BiologicalSubstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    substance_name = db.Column(db.String(100), nullable=False)
    lab = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    organism_type = db.Column(db.String(100))
    hazard_level = db.Column(db.String(50))
    storage_conditions = db.Column(db.String(200))
    storage_place= db.Column(db.String(200))
    acquisition_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    hazard_level = db.Column(db.String(50))
    cid = db.Column(db.String(100))
    cas = db.Column(db.String(100))
    UUID = db.Column(db.String(100))
    qr_codes = db.relationship('QRCode', backref='qr_code_biological', lazy=True, overlaps="qr_code_biological")
    safety_sheet = db.Column(db.String(100))

class User(UserMixin):
    users = []
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    


def get_user(email):
    for user in User.users:
        if user.email == email:
            return user
    return None