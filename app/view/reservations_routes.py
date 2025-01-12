from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..model.reservation_model import Reservation
from ..model.user_model import User
from ..model.car_model import Car
from app.extensions import db

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/')
@login_required
def list_reservations():
    reservations = Reservation.query.all()
    return render_template('reservations/list.html', reservations=reservations)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_reservation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        car_id = request.form['car_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reservation = Reservation(user_id=user_id, car_id=car_id, start_date=start_date, end_date=end_date)
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('reservations.list_reservations'))
    users = User.query.all()
    cars = Car.query.filter_by(availability=True).all()
    return render_template('reservations/create.html', users=users, cars=cars)

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_reservation(id):
    reservation = Reservation.query.get(id)
    if request.method == 'POST':
        reservation.user_id = request.form['user_id']
        reservation.car_id = request.form['car_id']
        reservation.start_date = request.form['start_date']
        reservation.end_date = request.form['end_date']
        db.session.commit()
        return redirect(url_for('reservations.list_reservations'))
    users = User.query.all()
    cars = Car.query.filter_by(availability=True).all()
    return render_template('reservations/update.html', reservation=reservation, users=users, cars=cars)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()
    return redirect(url_for('reservations.list_reservations'))