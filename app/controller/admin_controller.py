from app.extensions import db
from werkzeug.security import generate_password_hash
from ..model.admin_model import Admin
import os

def list_admins_if_super_admin(user_role):
    """Lista todos los administradores si el usuario es superadministrador."""
    if user_role == 0:  # Super Admin
        try:
            admins = Admin.query.all()
            return admins
        except Exception as e:
            return f"Error al obtener la lista de administradores: {str(e)}"
    else:
        return "Acceso denegado. Solo los superadministradores pueden listar administradores."

def check_admin(email, password):
    """Verifica las credenciales de un administrador."""
    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return ('Usuario o clave inválidos', 'danger')
    if admin.check_password(password):
        return admin
    else:
        return ('Usuario o clave inválidos', 'danger')

def add_admin(first_name, last_name, email, password, phone=None, role=1):
    """Agrega un nuevo administrador a la base de datos."""
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return ('El administrador ya existe', 'error')

    password_hash = generate_password_hash(password)

    new_admin = Admin(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
        phone=phone,
        role=int(role)
    )

    try:
        db.session.add(new_admin)
        db.session.commit()
        return ('Administrador creado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        return ('Error al crear el administrador: ' + str(e.orig), 'error')

def get_admin_by_id(admin_id):
    """Obtiene un administrador por su ID."""
    return Admin.query.get(admin_id)

def update_admin(admin_id, first_name=None, last_name=None, email=None, phone=None, password=None):
    """Actualiza los datos de un administrador."""
    admin = Admin.query.get(admin_id)
    if not admin:
        return ('Administrador no encontrado', 'error')

    if first_name:
        admin.first_name = first_name
    if last_name:
        admin.last_name = last_name
    if email:
        admin.email = email
    if phone:
        admin.phone = phone
    if password:
        admin.set_password(password)

    try:
        db.session.commit()
        return ('Administrador actualizado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        return ('Error al actualizar el administrador: ' + str(e.orig), 'error')

def delete_admin(admin_id):
    """Elimina un administrador de la base de datos."""
    admin = Admin.query.get(admin_id)
    if not admin:
        return ('Administrador no encontrado', 'error')

    try:
        db.session.delete(admin)
        db.session.commit()
        return ('Administrador eliminado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        return ('Error al eliminar el administrador: ' + str(e.orig), 'error')

def create_default_super_admin():
    """Crea un superadministrador por defecto usando variables de entorno."""
    admin_email = os.getenv("SUPER_ADMIN_EMAIL")
    if not admin_email:
        print("Error: SUPER_ADMIN_EMAIL no está configurado en las variables de entorno.")
        return

    existing_admin = Admin.query.filter_by(email=admin_email).first()
    if existing_admin:
        print("El superadministrador ya existe.")
        return

    first_name = os.getenv("SUPER_ADMIN_FIRST_NAME", "Super")
    last_name = os.getenv("SUPER_ADMIN_LAST_NAME", "Admin")
    admin_password = os.getenv("SUPER_ADMIN_PASSWORD", "default_password")

    password_hash = generate_password_hash(admin_password)

    super_admin = Admin(
        first_name=first_name,
        last_name=last_name,
        email=admin_email,
        password_hash=password_hash,
        role=0  # Super Admin
    )

    try:
        db.session.add(super_admin)
        db.session.commit()
        print("Superadministrador creado con éxito.")
    except Exception as e:
        db.session.rollback()
        print("Error al crear el superadministrador:", e)
