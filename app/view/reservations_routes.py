from flask import Blueprint, render_template, request, redirect, url_for
from ..model.reservation_model import Reservation
from ..model.user_model import User
from ..model.car_model import Car
from app.extensions import db

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/')
def list_reservations():
    reservations = Reservation.query.all()
    return render_template('reservations/list.html', reservations=reservations)

@bp.route('/create', methods=['GET', 'POST'])
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

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    db.session.delete(reservation)
    db.session.commit()
    return redirect(url_for('reservations.list_reservations'))