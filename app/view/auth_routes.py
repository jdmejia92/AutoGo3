from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..controller.auth_controller import check_login
from ..controller.admin_controller import check_admin

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = check_login(email=email, password=password)
        print(result)
        if type(result) != tuple:
            login_user(result)
            return redirect(url_for('base.base'))
        else:
            flash(result[0], result[1])
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('base.base'))

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    Página de "Mi Cuenta" para usuarios autenticados.
    """
    admin = check_admin(current_user.email, current_user.password_hash)

    if admin:
        print(current_user)
        payment_methods = []  
        documents = []

        reservations = [1,2,3,4]

        return render_template(
            'users/account.html', 
            user=current_user,
            reservations=reservations,
            payment_methods=payment_methods,
            documents=documents
        )
    else:
        reservations = current_user.reservations  
        payment_methods = []  
        documents = [] 

        return render_template(
            'users/account.html', 
            user=current_user,
            reservations=reservations,
            payment_methods=payment_methods,
            documents=documents
        )