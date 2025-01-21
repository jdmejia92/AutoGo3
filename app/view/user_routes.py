from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..controller.user_controller import add_user, delete_user, list_users_if_admin, get_user_by_id, update_user_info
from ..controller.admin_controller import add_admin, get_admin_by_id
from app.extensions import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
@login_required
def list_users():
    users = list_users_if_admin(current_user.tier)
    return render_template('users/list.html', user=users)

@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dni = request.form.get('dni')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        license_number = request.form.get('license_number')
        license_expiration = request.form.get('license_expiration')
        license_country = request.form.get('license_country')
        address = request.form.get('address')
        city = request.form.get('city')
        postal_code = request.form.get('postal_code')
        country = request.form.get('country')
        state = request.form.get('state')
        terms_accepted = request.form.get('terms_accepted', 'on') == 'on'
        privacy_policy_accepted = request.form.get('privacy_policy_accepted', 'on') == 'on'
        offers_accepted = request.form.get('offers_accepted', 'on') == 'on'

        # Validate required fields
        if not dni or not password or not first_name or not last_name or not email or not license_country or not address or not city or not postal_code or not country or not state:
            flash('Todos los campos obligatorios deben ser completados!', 'error')
            return render_template('users/create.html', first_name=first_name, last_name=last_name, dni=dni, email=email, phone=phone, 
                                    license_number=license_number, license_expiration=license_expiration, license_country=license_country, 
                                    address=address, city=city, postal_code=postal_code, country=country, state=state, 
                                    terms_accepted=terms_accepted, privacy_policy_accepted=privacy_policy_accepted, offers_accepted=offers_accepted)

        # Create the user
        result = add_user(
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            email=email,
            password=password,
            phone=phone,
            license_number=license_number,
            license_expiration=license_expiration,
            license_country=license_country,
            address=address,
            city=city,
            postal_code=postal_code,
            country=country,
            state=state,
            terms_accepted=terms_accepted,
            privacy_policy_accepted=privacy_policy_accepted,
            offers_accepted=offers_accepted
        )

        flash(result[0], result[1])
        return redirect(url_for('base.base'))

    return render_template('users/create.html')


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user_route(id):
    delete_user(user_id=id)
    return redirect(url_for('users.list_users'))


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    # Fetch the user from the database
    user = get_user_by_id(id)  # Replace with your actual function to fetch the user
    if not user:
        flash('Usuario no encontrado!', 'error')
        return redirect(url_for('base.base'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', user.first_name)
        last_name = request.form.get('last_name', user.last_name)
        dni = request.form.get('dni', user.dni)
        email = request.form.get('email', user.email)
        password = request.form.get('password')
        phone = request.form.get('phone', user.phone)
        license_number = request.form.get('license_number', user.license_number)
        license_expiration = request.form.get('license_expiration', user.license_expiration)
        license_country = request.form.get('license_country', user.license_country)
        address = request.form.get('address', user.address)
        city = request.form.get('city', user.city)
        postal_code = request.form.get('postal_code', user.postal_code)
        country = request.form.get('country', user.country)
        state = request.form.get('state', user.state)
        offers_accepted = request.form.get('offers_accepted', True)

        # Validate required fields
        if not dni or not first_name or not last_name or not email or not license_country or not address or not city or not postal_code or not country or not state:
            flash('Todos los campos obligatorios deben ser completados!', 'error')
            return render_template('users/create.html', user=user)

        # Update the user
        result = update_user_info(
            user_id=current_user.id,
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            email=email,
            password=password,
            phone=phone,
            license_number=license_number,
            license_expiration=license_expiration,
            license_country=license_country,
            address=address,
            city=city,
            postal_code=postal_code,
            country=country,
            state=state,
            offers_accepted=offers_accepted
        )

        flash(result[0], result[1])
        return redirect(url_for('auth.account'))

    return render_template('users/create.html', user=user)


# NUEVA RUTA: Dashboard
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    admin = get_admin_by_id(current_user.id)
    if admin:
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
        try:
            # Obtener datos del formulario
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            dob = request.form['dob']
            dni = request.form['dni']
            address = request.form['address']
            phone = request.form['phone']
            email = request.form['email']
            marital_status = request.form['marital_status']
            children = int(request.form['children'])
            department = request.form['department']
            position = request.form['position']
            work_schedule = request.form['work_schedule']
            salary = float(request.form['salary'])
            join_date = request.form['join_date']
            contract_type = request.form['contract_type']
            education_level = request.form['education_level']
            emergency_contact = request.form['emergency_contact']
            emergency_phone = request.form['emergency_phone']
            afp = request.form['afp']
            password = request.form['password']  # Contraseña inicial del administrador

            # Crear el nuevo administrador
            result = add_admin(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                dni=dni,
                address=address,
                phone=phone,
                email=email,
                marital_status=marital_status,
                children=children,
                department=department,
                position=position,
                work_schedule=work_schedule,
                salary=salary,
                join_date=join_date,
                contract_type=contract_type,
                education_level=education_level,
                emergency_contact=emergency_contact,
                emergency_phone=emergency_phone,
                afp=afp,
                password=password,
                tier=1  # Nivel de administrador
            )

            # Manejo del resultado
            if isinstance(result, tuple) and result[1] == 'success':
                flash('Administrador registrado con éxito.', 'success')
                return redirect(url_for('users.list_users'))
            else:
                flash(result[0], result[1])

        except Exception as e:
            flash(f"Error al registrar el administrador: {str(e)}", 'error')

    # Renderizar la plantilla de creación
    return render_template('admin/create_admin.html')