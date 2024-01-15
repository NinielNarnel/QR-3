from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField, SubmitField, HiddenField,PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask import Flask, render_template
from .models import Laboratory


class LaboratoryForm(FlaskForm):
    lab_id= StringField('Lab Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    supervisor = StringField('Supervisor', validators=[InputRequired()])

class EquipmentForm(FlaskForm):
    
    equipment_name = StringField('Equipment Name', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    description = TextAreaField('Description')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[InputRequired()])
    maintenance_date = DateField('Maintenance Date', format='%Y-%m-%d')

class ResearcherForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    phone = StringField('Phone')
    lab = StringField('Lab', validators=[InputRequired()])

class ChemicalSubstanceForm(FlaskForm):
    cid = IntegerField('cid', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    storage_place = TextAreaField('Storage Place')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[InputRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')

class BiologicalSubstanceForm(FlaskForm):
    substance_name = StringField('Substance Name', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    cid = IntegerField('Cid', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    organism_type = StringField('Organism Type')
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    storage_place = StringField('Storage Place')
    acquisition_date = DateField('Acquisition Date', format='%Y-%m-%d', validators=[InputRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')
    
class EditItemForm(FlaskForm):
    
    lab = StringField('Lab', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    submit = SubmitField('Guardar Cambios')
    csrf_token = StringField('CSRF Token')

class EditBiologicalForm(EditItemForm):
    organism_type = StringField('Organism Type')
    substance_name = StringField('Substance Name', validators=[InputRequired()])
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    storage_place = TextAreaField('Storage Place')
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')
    cas = IntegerField('CAS', validators=[InputRequired()])

class EditChemicalForm(EditItemForm):
    chemical_formula = StringField('Chemical Formula')
    substance_name = StringField('Substance Name', validators=[InputRequired()])
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    storage_place = TextAreaField('Storage Place')
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')
    cas = IntegerField('CAS', validators=[InputRequired()])

class EditEquipmentForm(EditItemForm):
    equipment_name = StringField('Name')
    description = TextAreaField('Description')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d')
    maintenance_date = DateField('Maintenance Date', format='%Y-%m-%d')

class DeleteItemForm(FlaskForm):
    #csrf_token = HiddenField()
    csrf_token = StringField('CSRF Token')
    submit = SubmitField('Confirmar Eliminación')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign Up')