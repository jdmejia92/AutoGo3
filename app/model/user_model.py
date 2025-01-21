from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Store hashed password
    phone = db.Column(db.String(15), nullable=True)

    # Driving Information
    license_number = db.Column(db.String(20), nullable=True)
    license_expiration = db.Column(db.Date, nullable=True)
    license_country = db.Column(db.String(100), nullable=False)

    # Address Information
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)

    # Verification
    terms_accepted = db.Column(db.Boolean, nullable=False, default=True)
    privacy_policy_accepted = db.Column(db.Boolean, nullable=False, default=True)
    offers_accepted = db.Column(db.Boolean, nullable=True, default=False)

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password."""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.email

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

def load_user_model(email):
    return User.query.filter_by(email=email).first()
