from app import db
from model.user_model import User

def create_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return user

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