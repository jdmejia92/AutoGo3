from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..controller.user_controller import check_user

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result = check_user(email=email, password=password)
        if type(result) != tuple:
            login_user(result)  # Log in the user
            return redirect(url_for('base.base'))
        else:
            flash(result[0])
    return render_template('login/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('base.base'))