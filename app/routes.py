from app import app, db
from datetime import datetime
from flask import Blueprint, render_template, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from jinja2 import Environment, FileSystemLoader
from .models import Laboratory, Equipment, Researcher, ChemicalSubstance, BiologicalSubstance, QRCode, User
from .forms import LaboratoryForm, EquipmentForm, ResearcherForm, ChemicalSubstanceForm, BiologicalSubstanceForm, EditBiologicalForm, EditChemicalForm, EditEquipmentForm, DeleteItemForm, LoginForm, SignupForm
from Modules import GeneradorUUID, GeneradorCAS, GeneradorSafetySheet, GeneradorPubChem, GeneradorQR, GeneradorOrganismo
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from flask_login import login_user, login_required, logout_user, current_user
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Inicio de sesión exitoso")
            print("Usuario actual después de iniciar sesión:", current_user)
            return redirect(url_for('main_page'))
        else:
            flash("Nombre de usuario o contraseña incorrectos")

    # Si no se validó el formulario o hubo un problema, renderiza la plantilla de inicio de sesión
    return render_template('login.html', form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main_page'))
    return render_template('signup.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))

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
            lab_id=form.lab_id.data,
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
@app.route('/delete_lab/<int:lab_id>')
def delete_lab(lab_id):
    lab = Laboratory.query.get_or_404(lab_id)
    db.session.delete(lab)  # Para eliminar el laboratorio
    db.session.commit()
    return redirect(url_for('list_labs'))

@app.route('/edit_lab/<int:lab_id>', methods=['GET', 'POST'])
def edit_lab(lab_id):
    lab = Laboratory.query.get_or_404(lab_id)
    form = LaboratoryForm(obj=lab)

    if form.validate_on_submit():
        lab.lab_name = form.lab_name.data
        lab.location = form.location.data
        lab.supervisor = form.supervisor.data
        db.session.commit()
        return redirect(url_for('list_labs'))

    return render_template('edit_lab.html', lab=lab, form=form)

#####################################################################################################
# EQUIPMENT
#####################################################################################################

# Route for adding equipment
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    form = EquipmentForm()

    # Populate the lab choices in the form
    ##form.lab_id.choices = [(lab.lab_id, lab.lab_name) for lab in Laboratory.query.all()]

    if form.validate_on_submit():
        UUID = GeneradorUUID.getUUID()
        equipment = Equipment(
            equipment_name=form.equipment_name.data,
            lab=form.lab.data,
            description=form.description.data,
            purchase_date=form.purchase_date.data,
            maintenance_date=form.maintenance_date.data,
            UUID=UUID,
        )
        qr_data = f"Tipo ({form.equipment_name.data}),  UUID ({UUID}), Lab ({form.lab.data}), Maintenance ({form.maintenance_date.data}), Description ({form.description.data})"
        qr_code_data = GeneradorQR.generate_qr_code(equipment, qr_data)
        qr_code_base64 = base64.b64encode(qr_code_data).decode('utf-8')  # Convert to base64

        new_qr_code = QRCode(code_data=qr_code_base64)
        new_qr_code.equipment = equipment
        db.session.add(new_qr_code)
        db.session.commit()
        return render_template('list_equipment.html',equipment=Equipment.query.all())
    return render_template('add_equipment.html', form=form)

@app.route('/list_equipment')
def list_equipment():
    search_query = request.args.get('search', '')

    if search_query:
        # Aplicar el filtro en la base de datos para buscar sustancias biológicas por nombre
        equipment_list = Equipment.query.filter(Equipment.equipment_name.ilike(f"%{search_query}%")).all()
    else:
        # Si no se proporciona una consulta de búsqueda, muestra todas las sustancias biológicas
        equipment_list = Equipment.query.all()

    return render_template('list_equipment.html', equipment=equipment_list)

@app.route('/edit_equipment/<int:equipment_id>', methods=['GET', 'POST'])
def edit_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    form = EditEquipmentForm(obj=equipment)  # Crea una instancia del formulario y carga los datos actuales

    if form.validate_on_submit():
        # Actualizar la sustancia con los datos del formulario
        form.populate_obj(equipment)
        db.session.commit()
        return redirect(url_for('list_equipment'))

    return render_template('edit_equipment.html', form=form, equipment=equipment)

@app.route('/delete_equipment/<int:equipment_id>', methods=['GET', 'POST'])
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    form = DeleteItemForm()
    
    if form.validate_on_submit():
        # Procesar la eliminación aquí
        db.session.delete(equipment)
        db.session.commit()
        return redirect(url_for('list_equipment'))
    
    # Renderizar la plantilla con el formulario y los datos de la sustancia
    return render_template('delete_equipment.html', form=form, equipment=equipment)



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



#BIOLOGICAL SUBSTANCE
@app.route('/add_biological_substance', methods=['GET', 'POST'])
def add_biological_substance():
    form = BiologicalSubstanceForm()    
    if request.method == 'POST':
        if form.validate_on_submit():
            UUID = GeneradorUUID.getUUID()
            user_cid = form.cid.data 
            cas_number = GeneradorCAS.getCAS(user_cid)
            sds = GeneradorSafetySheet.getSDS(cas_number)
            Nombre = GeneradorPubChem.getName(user_cid)
            new_biological_substance = BiologicalSubstance(
                substance_name=Nombre,
                cid=user_cid, 
                cas=cas_number,
                lab=form.lab.data,
                quantity=form.quantity.data,
                hazard_level=form.hazard_level.data,
                storage_conditions=form.storage_conditions.data,
                organism_type = form.organism_type.data,
                acquisition_date=form.acquisition_date.data,
                expiration_date=form.expiration_date.data,
                UUID=UUID,
                safety_sheet=sds,
            )

            qr_data = f"Name ({Nombre}), UUID ({UUID}), Hazard Level ({form.hazard_level.data}), Storage ({form.storage_conditions.data})"
            qr_code_data = GeneradorQR.generate_qr_code(new_biological_substance, qr_data)
            qr_code_base64 = base64.b64encode(qr_code_data).decode('utf-8')  # Convert to base64

            new_qr_code = QRCode(code_data=qr_code_base64, biological_substance=new_biological_substance)
            db.session.add(new_qr_code)
            db.session.commit()
            return render_template('list_biological_substances.html', biologicals=BiologicalSubstance.query.all())
    return render_template('add_biological_substance.html', form=form)

@app.route('/list_biological_substances', methods=['GET'])
def list_biological_substances():
    search_query = request.args.get('search', '')  # Obtener la consulta de búsqueda de la URL

    if search_query:
        # Aplicar el filtro en la base de datos para buscar sustancias biológicas por nombre
        biologicals = BiologicalSubstance.query.filter(BiologicalSubstance.substance_name.ilike(f"%{search_query}%")).all()
    else:
        # Si no se proporciona una consulta de búsqueda, muestra todas las sustancias biológicas
        biologicals = BiologicalSubstance.query.all()

    return render_template('list_biological_substances.html', biologicals=biologicals)

@app.route('/edit_biological_substance/<int:substance_id>', methods=['GET', 'POST'])
def edit_biological_substance(substance_id):
    substance = BiologicalSubstance.query.get_or_404(substance_id)
    form = EditBiologicalForm(obj=substance)  # Crea una instancia del formulario y carga los datos actuales

    if form.validate_on_submit():
        # Actualizar la sustancia con los datos del formulario
        form.populate_obj(substance)
        db.session.commit()
        return redirect(url_for('list_biological_substances'))

    return render_template('edit_biological_substance.html', form=form, substance=substance)

@app.route('/delete_substance/<int:substance_id>', methods=['GET', 'POST'])
def delete_biological_substance(substance_id):
    substance = BiologicalSubstance.query.get_or_404(substance_id)
    form = DeleteItemForm()
    
    if form.validate_on_submit():
        # Procesar la eliminación aquí
        db.session.delete(substance)
        db.session.commit()
        return redirect(url_for('list_biological_substances'))
    
    # Renderizar la plantilla con el formulario y los datos de la sustancia
    return render_template('delete_biological_substance.html', form=form, substance=substance)



#####################################################################################################
# CHEMICAL SUBSTANCE
#####################################################################################################

@app.route('/add_chemical_substance', methods=['GET', 'POST'])
def add_chemical_substance():
    form = ChemicalSubstanceForm()
    if form.validate_on_submit():
        UUID = GeneradorUUID.getUUID()
        user_cid = form.cid.data 
        cas_number = GeneradorCAS.getCAS(user_cid)
        sds = GeneradorSafetySheet.getSDS(cas_number)
        Nombre = GeneradorPubChem.getName(user_cid)
        Fórmula = GeneradorPubChem.getFormula(user_cid)

        new_chemical_substance = ChemicalSubstance(
            substance_name=Nombre,
            cid=user_cid, 
            cas=cas_number,
            lab=form.lab.data,
            quantity=form.quantity.data,
            chemical_formula=Fórmula,
            hazard_level=form.hazard_level.data,
            storage_conditions=form.storage_conditions.data,
            storage_place=form.storage_place.data,
            purchase_date=form.purchase_date.data,
            expiration_date=form.expiration_date.data,
            UUID=UUID,
            safety_sheet=sds,
        )

        qr_data = f"Name ({Nombre}), CAS ({cas_number}), Formula ({Fórmula}), UUID ({UUID}), Hazard Level ({form.hazard_level.data}), Storage({form.storage_place.data})"
        qr_code_data = GeneradorQR.generate_qr_code(new_chemical_substance, qr_data)
        qr_code_base64 = base64.b64encode(qr_code_data).decode('utf-8')  # Convert to base64

        new_qr_code = QRCode(code_data=qr_code_base64)
        new_qr_code.chemical_substance = new_chemical_substance
        db.session.add(new_qr_code)
        db.session.commit()

        return render_template('list_chemical_substances.html', chemicals=ChemicalSubstance.query.all())
    
    return render_template('add_chemical_substance.html', form=form)
@app.route('/list_chemical_substances', methods=['GET'])
def list_chemical_substances():
    search_query = request.args.get('search', '')  # Obtener la consulta de búsqueda de la URL

    if search_query:
        # Aplicar el filtro en la base de datos para buscar sustancias biológicas por nombre
        chemicals = ChemicalSubstance.query.filter(ChemicalSubstance.substance_name.ilike(f"%{search_query}%")).all()
    else:
        # Si no se proporciona una consulta de búsqueda, muestra todas las sustancias biológicas
        chemicals = ChemicalSubstance.query.all()

    return render_template('list_chemical_substances.html', chemicals=chemicals)

@app.route('/edit_chemical_substance/<int:substance_id>', methods=['GET', 'POST'])
def edit_chemical_substance(substance_id):
    substance = ChemicalSubstance.query.get_or_404(substance_id)
    form = EditChemicalForm(obj=substance)

    if form.validate_on_submit():
        print("Form is valid!")
        form.populate_obj(substance)
        try:
            db.session.commit()
            flash('Changes saved successfully', 'success')
            return redirect(url_for('list_chemical_substances'))
        except Exception as e:
            db.session.rollback()  # Rollback changes if an exception occurs
            flash(f'Error updating chemical substance: {str(e)}', 'error')
    else:
        print("Form is NOT valid!")
    return render_template('edit_chemical_substance.html', form=form, substance=substance)

@app.route('/delete_chemical_substance/<int:substance_id>', methods=['GET', 'POST'])
def delete_chemical_substance(substance_id):
    substance = ChemicalSubstance.query.get_or_404(substance_id)
    form = DeleteItemForm()
    
    if form.validate_on_submit():
        # Procesar la eliminación aquí
        db.session.delete(substance)
        db.session.commit()
        return redirect(url_for('list_chemical_substances'))
    
    # Renderizar la plantilla con el formulario y los datos de la sustancia
    return render_template('delete_chemical_substance.html', form=form, substance=substance)



