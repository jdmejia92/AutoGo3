from app.extensions import db
from ..model.admin_model import Admin
from ..model.user_model import User
from datetime import date
import os

def check_login(email, password):
    """Verifica las credenciales de un usuario o administrador."""
    user = User.query.filter_by(email=email).first()
    admin = Admin.query.filter_by(email=email).first()
    if user:
        if user.check_password(password):
            return user
        else:
            return ('Usuario o clave inválidos', 'danger')
    elif admin:
        if admin.check_password(password):
            return admin
        else:
            return ('Usuario o clave inválidos', 'danger')
    else:
        return ('Usuario o clave inválidos', 'danger')