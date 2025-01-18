from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Almacena la contraseña encriptada
    phone = db.Column(db.String(15), nullable=True)

    # Roles: 0 = Admin, 1 = Worker
    role = db.Column(db.Integer, nullable=False, default=1)

    # Métodos de utilidad para contraseñas
    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password."""
        return check_password_hash(self.password_hash, password)

    def is_super_admin(self):
        """Check if the user is an admin."""
        return self.role == 0

    def is_admin(self):
        """Check if the user is a worker."""
        return self.role == 1

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} (Role: {'Admin' if self.role == 0 else 'Worker'})>"

# Carga de usuario para Flask-Login
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))
