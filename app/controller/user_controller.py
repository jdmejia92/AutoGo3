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

def add_user(name, email, dob, password, tier=2):
    user = User.query.filter_by(email=email).first()
    if user:
        result = ('User already exist', 'error')
    else:
        password_hash = generate_password_hash(password=password)
    
        new_user = User(name=name, email=email, dob=dob, password_hash=password_hash, tier=int(tier))

        try:
            db.session.add(new_user)
            db.session.commit()
            result = ('User created successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            result = ('Error creating user: ' + str(e.orig), 'error')

    return result

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