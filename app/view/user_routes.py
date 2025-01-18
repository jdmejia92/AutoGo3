from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..controller.user_controller import add_user, check_user, delete_user, list_users_if_admin
from datetime import datetime
from app.extensions import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()  # Validar email
        password = request.form.get('password', '')  # Validar contraseña

        # 1. Verificar campos vacíos
        if not email or not password:
            flash('Por favor, completa ambos campos', 'warning')
            return redirect(url_for('users.login'))

        # 2. Validar formato de correo electrónico
        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Por favor, ingresa un correo electrónico válido', 'danger')
            return redirect(url_for('users.login'))

        # 3. Validar usuario
        result = check_user(email=email, password=password)

        #  Mensaje de error (string o tuple)
        if isinstance(result, tuple):
            flash(result[0], result[1])  # Mostrar mensaje flash
            return redirect(url_for('users.login'))

        # Usuario válido
        login_user(result)  # Log in exitoso
        flash('Inicio de sesión exitoso. ¡Bienvenido!', 'success')
        return redirect(url_for('base.base'))

    return render_template('users/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('base.base'))

@bp.route('/')
@login_required
def list_users():
    users = list_users_if_admin(current_user.tier)
    return render_template('users/list.html', user=users)


@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        dob = request.form.get('dob')  
        password = request.form.get('password')  
        tier = request.form.get('tier', 2)  

        if not dob or not password:
            flash('Date of birth and password are required!', 'error')
            return render_template('create_user.html', name=name, email=email, dob=dob, tier=tier)

        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for Date of Birth!', 'error')
            return render_template('create_user.html', name=name, email=email, dob=dob, tier=tier)

        # Create the user
        result = add_user(name=name, email=email, dob=dob, password=password, tier=int(tier))
        flash(result)
        return redirect(url_for('base.base'))

    
    return render_template('users/create.html')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user_route(id):
    delete_user(user_id=id)
    return redirect(url_for('users.list_users'))

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Página de "Mi Cuenta" para usuarios autenticados.
    """
    reservations = current_user.reservations  
    payment_methods = []  
    documents = [] 

   
    return render_template(
        'users/account.html', 
        user=current_user,
        reservations=reservations,
        payment_methods=payment_methods,
        documents=documents
    )

@bp.route('/update', methods=['POST'])
@login_required
def update_user():
    pass

# NUEVA RUTA: Dashboard
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.tier != 0:
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('base.base'))
    return render_template('reports/dashboard.html')

@bp.route('/create_admin', methods=['GET', 'POST'])
@login_required
def create_admin():
    # Verificar si el usuario actual tiene el nivel de acceso adecuado
    if current_user.tier != 0:  # Solo superadministradores (Tier 0)
        flash('No tienes permisos para registrar administradores.', 'error')
        return redirect(url_for('base.base'))

    if request.method == 'POST':
        # Obtener datos del formulario
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
            dni = request.form['dni']
            address = request.form['address']
            phone = request.form['phone']
            email = request.form['email']
            marital_status = request.form['marital_status']
            children = int(request.form['children'])
            position = request.form['position']
            department = request.form['department']
            join_date = datetime.strptime(request.form['join_date'], '%Y-%m-%d').date()
            contract_type = request.form['contract_type']
            salary = float(request.form['salary'])
            work_schedule = request.form['work_schedule']
            education_level = request.form['education_level']
            emergency_contact_name = request.form['emergency_contact_name']
            emergency_contact_phone = request.form['emergency_contact_phone']
            blood_group = request.form['blood_group']
            medical_conditions = request.form['medical_conditions']
            bank_account = request.form['bank_account']
            afp = request.form['afp']
            health_insurance = request.form['health_insurance']
            password = request.form['password']  # Contraseña inicial del administrador

            # Crear el nuevo administrador
            result = add_user(
                name=f"{first_name} {last_name}",
                email=email,
                dob=dob,
                password=password,
                tier=1  # Tier 1 es nivel de administrador
            )

            # Manejo de resultado
            if isinstance(result, tuple) and result[1] == 'success':
                flash('Administrador registrado con éxito.', 'success')
                return redirect(url_for('users.list_users'))
            else:
                flash(result[0], result[1])

        except Exception as e:
            flash(f"Error al registrar el administrador: {str(e)}", 'error')

    # Renderizar la plantilla de creación
    return render_template('users/create_admin.html')
