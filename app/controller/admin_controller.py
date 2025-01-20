from app.extensions import db
from werkzeug.security import generate_password_hash
from ..model.admin_model import Admin
from datetime import date
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

def add_admin(
    first_name, last_name, dob, dni, address, phone, email, marital_status, children, 
    department, position, work_schedule, salary, join_date, contract_type, education_level, 
    emergency_contact, emergency_phone, afp, password, tier=1
):
    """Agrega un nuevo administrador a la base de datos."""
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return ('El administrador ya existe', 'error')

    existing_dni = Admin.query.filter_by(dni=dni).first()
    if existing_dni:
        return ('El DNI ya está registrado', 'error')

    password_hash = generate_password_hash(password)

    new_admin = Admin(
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
        password_hash=password_hash,
        tier=tier
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

    # Obtiene los valores de las variables de entorno con valores predeterminados
    first_name = os.getenv("SUPER_ADMIN_FIRST_NAME", "Super")
    last_name = os.getenv("SUPER_ADMIN_LAST_NAME", "Admin")
    admin_password = os.getenv("SUPER_ADMIN_PASSWORD", "default_password")
    dob = os.getenv("SUPER_ADMIN_DOB", "1970-01-01")
    dni = os.getenv("SUPER_ADMIN_DNI", "00000000")
    address = os.getenv("SUPER_ADMIN_ADDRESS", "Direccion por defecto")
    phone = os.getenv("SUPER_ADMIN_PHONE", "999999999")
    marital_status = os.getenv("SUPER_ADMIN_MARITAL_STATUS", "Soltero")
    children = int(os.getenv("SUPER_ADMIN_CHILDREN", 0))
    department = os.getenv("SUPER_ADMIN_DEPARTMENT", "Administración")
    position = os.getenv("SUPER_ADMIN_POSITION", "Super Admin")
    work_schedule = os.getenv("SUPER_ADMIN_WORK_SCHEDULE", "Tiempo completo")
    salary = float(os.getenv("SUPER_ADMIN_SALARY", 0.0))
    join_date = os.getenv("SUPER_ADMIN_JOIN_DATE", "2025-01-01")
    contract_type = os.getenv("SUPER_ADMIN_CONTRACT_TYPE", "Indefinido")
    education_level = os.getenv("SUPER_ADMIN_EDUCATION_LEVEL", "Universitario")
    emergency_contact = os.getenv("SUPER_ADMIN_EMERGENCY_CONTACT", "Contacto de emergencia")
    emergency_phone = os.getenv("SUPER_ADMIN_EMERGENCY_PHONE", "888888888")
    afp = os.getenv("SUPER_ADMIN_AFP", "AFP Default")

    # Convierte las fechas de cadena a objetos date
    try:
        dob = date.fromisoformat(dob)
        join_date = date.fromisoformat(join_date)
    except ValueError as e:
        print("Error en el formato de fecha:", e)
        return

    # Crea el hash de la contraseña
    password_hash = generate_password_hash(admin_password)

    # Crea el objeto superadministrador
    super_admin = Admin(
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        dni=dni,
        address=address,
        phone=phone,
        email=admin_email,
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
        tier=0,  # Super Admin
        password_hash=password_hash
    )

    # Guarda el superadministrador en la base de datos
    try:
        db.session.add(super_admin)
        db.session.commit()
        print("Superadministrador creado con éxito.")
    except Exception as e:
        db.session.rollback()
        print("Error al crear el superadministrador:", e)