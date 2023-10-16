from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField
from wtforms.validators import InputRequired

class LaboratoryForm(FlaskForm):
    lab_name = StringField('Lab Name', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    supervisor = StringField('Supervisor', validators=[InputRequired()])

class EquipmentForm(FlaskForm):
    equipment_name = StringField('Equipment Name', validators=[InputRequired()])
    lab_id = SelectField('Laboratory', choices=[], coerce=int)
    quantity = IntegerField('Quantity', validators=[InputRequired()])
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
    substance_name = StringField('Substance Name', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    chemical_formula = StringField('Chemical Formula')
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[InputRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')

class BiologicalSubstanceForm(FlaskForm):
    substance_name = StringField('Substance Name', validators=[InputRequired()])
    lab = StringField('Lab', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    organism_type = StringField('Organism Type')
    hazard_level = StringField('Hazard Level')
    storage_conditions = TextAreaField('Storage Conditions')
    acquisition_date = DateField('Acquisition Date', format='%Y-%m-%d', validators=[InputRequired()])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d')
