from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..model.user_model import User
from app.extensions import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)  # Log in the user
            return redirect(url_for('users.list_users'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('users/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('users.login'))

@bp.route('/')
def list_users():
    users = User.query.all()
    template = 'users/list_users.html'
    print(template)
    return render_template(template, users=users)

@bp.route('/login')
def login():
    users = User.query.all()
    template = 'users/login.html'
    print(template)
    return render_template(template, users=users)

@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.list_users'))
    return render_template('users/create.html')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_users'))