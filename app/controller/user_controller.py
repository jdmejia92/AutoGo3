from app.extensions import db
from werkzeug.security import generate_password_hash
from ..model.user_model import User

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
        terms_accepted=terms_accepted,
        privacy_policy_accepted=privacy_policy_accepted,
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

def update_user(user_id, name=None, email=None):
    user = User.query.get(user_id)
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()