from app import app, db
from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from .models import Laboratory, Equipment, Researcher, ChemicalSubstance, BiologicalSubstance
from .forms import LaboratoryForm, EquipmentForm, ResearcherForm, ChemicalSubstanceForm, BiologicalSubstanceForm

# Flask route for the main page
@app.route('/')
def main_page():
    return render_template('main_page.html')

#####################################################################################################
# LAB
#####################################################################################################

@app.route('/add_lab', methods=['GET', 'POST'])
def add_lab():
    form = LaboratoryForm()
    if form.validate_on_submit():
        new_lab = Laboratory(
            lab_name=form.lab_name.data,
            location=form.location.data,
            supervisor=form.supervisor.data,
            created_at=datetime.now(),
            updated_at=None
        )
        db.session.add(new_lab)
        db.session.commit()
        return redirect(url_for('list_labs'))
    return render_template('add_lab.html', form=form)

@app.route('/list_labs')
def list_labs():
    labs = Laboratory.query.all()
    return render_template('list_labs.html', labs=labs)

#####################################################################################################
# EQUIPMENT
#####################################################################################################

# Route for adding equipment
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    form = EquipmentForm()

    # Populate the lab choices in the form
    form.lab_id.choices = [(lab.lab_id, lab.lab_name) for lab in Laboratory.query.all()]

    if form.validate_on_submit():
        equipment = Equipment(
            equipment_name=form.equipment_name.data,
            lab_id=form.lab_id.data,
            quantity=form.quantity.data,
            description=form.description.data,
            purchase_date=form.purchase_date.data,
            maintenance_date=form.maintenance_date.data,
        )
        db.session.add(equipment)
        db.session.commit()
        return redirect(url_for('list_equipment'))

    return render_template('add_equipment.html', form=form)

# Route for listing all equipment
@app.route('/list_equipment')
def list_equipment():
    equipment = Equipment.query.all()
    return render_template('list_equipment.html', equipment=equipment)

#####################################################################################################
# RESEARCHER
#####################################################################################################

@app.route('/add_researcher', methods=['GET', 'POST'])
def add_researcher():
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher = Researcher(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            lab=form.lab.data,
            created_at=datetime.now(),
            updated_at=None
        )
        db.session.add(researcher)
        db.session.commit()
        return redirect(url_for('list_researchers'))
    return render_template('add_researcher.html', form=form)

@app.route('/list_researchers')
def list_researchers():
    researchers = Researcher.query.all()
    return render_template('list_researchers.html', researchers=researchers)


#####################################################################################################
# BIOLOGICAL SUBSTANCE
#####################################################################################################

@app.route('/add_biological_substance', methods=['GET', 'POST'])
def add_biological_substance():
    form = BiologicalSubstanceForm()

    if form.validate_on_submit():
        new_biological_substance = BiologicalSubstance(
            substance_name=form.substance_name.data,
            lab=form.lab.data,
            quantity=form.quantity.data,
            organism_type=form.organism_type.data,
            hazard_level=form.hazard_level.data,
            storage_conditions=form.storage_conditions.data,
            acquisition_date=form.acquisition_date.data,
            expiration_date=form.expiration_date.data
        )

        db.session.add(new_biological_substance)
        db.session.commit()

        return redirect(url_for('list_biological_substances'))

    return render_template('add_biological_substance.html', form=form)

@app.route('/list_biological_substances')
def list_biological_substances():
    biologicals = BiologicalSubstance.query.all()
    return render_template('list_biological_substances.html', biologicals=biologicals)


#####################################################################################################
# CHEMICAL SUBSTANCE
#####################################################################################################

@app.route('/add_chemical_substance', methods=['GET', 'POST'])
def add_chemical_substance():
    form = ChemicalSubstanceForm()
    if form.validate_on_submit():
        new_chemical_substance = ChemicalSubstance(
            substance_name=form.substance_name.data,
            lab=form.lab.data,
            quantity=form.quantity.data,
            chemical_formula=form.chemical_formula.data,
            hazard_level=form.hazard_level.data,
            storage_conditions=form.storage_conditions.data,
            purchase_date=form.purchase_date.data,
            expiration_date=form.expiration_date.data
        )
        db.session.add(new_chemical_substance)
        db.session.commit()
        return redirect(url_for('list_chemical_substances'))

    return render_template('add_chemical_substance.html', form=form)

@app.route('/list_chemical_substances')
def list_chemical_substances():
    chemicals = ChemicalSubstance.query.all()
    return render_template('list_chemical_substances.html', chemicals=chemicals)


