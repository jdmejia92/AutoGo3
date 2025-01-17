from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..controller.user_controller import add_user, check_user, delete_user, list_users_if_admin
from datetime import datetime
from app.extensions import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = check_user(email=email, password=password)
        if type(result) != tuple:
            login_user(result)  # Log in the user
            return redirect(url_for('base.base'))
        else:
            flash(result)
    return render_template('users/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('users.login'))

@bp.route('/')
@login_required
def list_users():
    users = list_users_if_admin(current_user.tier)
    return render_template('users/list.html', user=users)

@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        dob = request.form.get('dob')  # Ensure this is submitted
        password = request.form.get('password')  # Ensure this is submitted
        tier = request.form.get('tier', 2)  # Default to 'Client' if not provided

        if not dob or not password:
            flash('Date of birth and password are required!', 'error')
            return render_template('create_user.html', name=name, email=email, dob=dob, tier=tier)

        try:
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for Date of Birth!', 'error')
            return render_template('create_user.html', name=name, email=email, dob=dob, tier=tier)

        # Create the user
        result = add_user(name=name, email=email, dob=dob, password=password, tier=int(tier))
        flash(result)
        return redirect(url_for('base.base'))

    # Render the template for 'GET' requests
    return render_template('users/create.html')

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_user_route(id):
    delete_user(user_id=id)
    return redirect(url_for('users.list_users'))

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Página de "Mi Cuenta" para usuarios autenticados.
    """
    reservations = current_user.reservations  
    payment_methods = []  
    documents = []  

    # Renderizar la plantilla actualizada
    return render_template(
        'users/account.html', 
        user=current_user,
        reservations=reservations,
        payment_methods=payment_methods,
        documents=documents
    )


@bp.route('/update', methods=['POST'])
@login_required
def update_user():
   
    pass
