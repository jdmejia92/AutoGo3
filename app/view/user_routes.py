from flask import Blueprint, render_template, request, redirect, url_for
from ..model.user_model import User
from .. import db

bp = Blueprint('users', __name__, url_prefix='/')

@bp.route('/')
def list_users():
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