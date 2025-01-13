from app.extensions import db
from werkzeug.security import generate_password_hash
from ..model.user_model import User
from datetime import datetime

def check_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        result = ('User not found', 'error')
    else:
        if user and user.check_password(password):
            result = user
        else:
            result = ('Invalid email or password', 'danger')
    return result

def add_user(name, email, dob, password, tier=2):
    user = User.query.filter_by(email=email).first()
    if user:
        result = ('User already exist', 'error')
    else:
        password_hash = generate_password_hash(password=password)
    
        new_user = User(name=name, email=email, dob=dob, password_hash=password_hash, tier=int(tier), active=True)

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

def admin_user():
    query = User.query.filter_by(name="admin").first()
    if query is None:
        dob = datetime.strptime("1992-08-12", '%Y-%m-%d').date()
        password_hash = generate_password_hash("123456")  # Hash the admin password
        admin = User(
            name="admin",
            email="admin@admin.com",
            password_hash=password_hash,
            dob=dob,
            tier=0
        )
        try:
            db.session.add(admin)
            db.session.commit()
            print("Admin created")
        except Exception as e:
            db.session.rollback()
            print("Error creating admin:", e)
    else:
        print("Admin already exists")