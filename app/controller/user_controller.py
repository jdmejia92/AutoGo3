from app.extensions import db
from ..model.user_model import User
from datetime import date

def list_users_if_admin(user_tier):
    if user_tier == 0:  # Verifica si el usuario es administrador
        try:
            users = User.query.all()  # Obtiene todos los usuarios
            return users
        except Exception as e:
            return f"Error al obtener la lista de usuarios: {str(e)}"
    else:
        return "Acceso denegado. Solo los administradores pueden listar usuarios."

def check_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        result = ('Usuario o clave invalido', 'danger')
    else:
        if user and user.check_password(password):
            result = user
        else:
            result = ('Usuario o clave invalido', 'danger')
    return result

def add_user(first_name, last_name, dni, email, password, phone=None, license_number=None, 
            license_expiration=None, license_country=None, address=None, city=None, 
            postal_code=None, country=None, state=None, terms_accepted=True, 
            privacy_policy_accepted=True, offers_accepted=False):
    # Check if a user with the same email or DNI already exists
    user = User.query.filter((User.email == email) | (User.dni == dni)).first()
    if user:
        return ('User already exists', 'error')

    # Convierte las fechas de cadena a objetos date
    try:
        license_expiration = date.fromisoformat(license_expiration)
    except ValueError as e:
        return ('Error en el formato de fecha', 'error')

    # Create a new user instance
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        email=email,
        phone=phone,
        license_number=license_number,
        license_expiration=license_expiration,
        license_country=license_country,
        address=address,
        city=city,
        postal_code=postal_code,
        country=country,
        state=state,
        terms_accepted=True,
        privacy_policy_accepted=True,
        offers_accepted=offers_accepted
    )
    
    # Set the hashed password
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return ('Usuario creado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        return (f'Error al crear el usuario: {str(e.orig)}', 'error')

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user_info(user_id, first_name=None, last_name=None, dni=None, email=None, password=None, phone=None, license_number=None, 
                    license_expiration=None, license_country=None, address=None, city=None, 
                    postal_code=None, country=None, state=None, offers_accepted=None):
    
    try:
        user = User.query.get(user_id)
    except Exception as e:
        return ('Error al obtener el usuario', 'error')
    
    if user:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if dni:
            user.dni = dni
        if email:
            user.email = email
        if password:
            user.set_password(password)
        if phone:
            user.phone = phone
        if license_number:
            user.license_number = license_number
        if license_expiration:
            try:
                if type(license_expiration) == str:
                    license_expiration = date.fromisoformat(license_expiration)
                    user.license_expiration = license_expiration
                else:
                    user.license_expiration = license_expiration
            except ValueError as e:
                return ('Error en el formato de fecha', 'error')
        if license_country:
            user.license_country = license_country
        if address:
            user.address = address
        if city:
            user.city = city
        if postal_code:
            user.postal_code = postal_code
        if country:
            user.country = country
        if state:
            user.state = state
        if offers_accepted is not None:
            user.offers_accepted = offers_accepted

        db.session.commit()
    return "Usuario actualizado con éxito", 'success'


def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()