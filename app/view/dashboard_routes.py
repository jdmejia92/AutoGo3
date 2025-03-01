from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.extensions import db
from app.model.car_model import Car
from app.model.reservation_model import Reservation
from sqlalchemy import func
import datetime

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def dashboard():
    today = datetime.date.today()
    first_day = today.replace(day=1)

    # Datos generales
    total_cars = db.session.query(func.count(Car.id)).scalar() or 0
    available_cars = db.session.query(func.count(Car.id)).filter(Car.status == 0).scalar() or 0
    reservations_this_month = db.session.query(func.count(Reservation.id)).filter(
        Reservation.pickup_datetime >= first_day
    ).scalar() or 0
    occupancy_rate = (reservations_this_month / total_cars * 100) if total_cars > 0 else 0

    monthly_income = db.session.query(
        func.sum(func.extract('day', Reservation.return_datetime - Reservation.pickup_datetime) * Car.daily_rate)
    ).select_from(Reservation).join(Car, Car.id == Reservation.car_id).filter(
        Reservation.pickup_datetime >= first_day
    ).scalar() or 0

    # Datos de reservas por categoría
    reservations_by_category = db.session.query(
        Car.car_type, func.count(Reservation.id)
    ).join(Reservation).group_by(Car.car_type).all()
    
    reservations_by_category_data = {row[0]: row[1] for row in reservations_by_category}

    return render_template('reports/dashboard.html',
                           available_cars=available_cars,
                           total_cars=total_cars,
                           reservations_this_month=reservations_this_month,
                           occupancy_rate=round(occupancy_rate, 2),
                           monthly_income=monthly_income,
                           reservations_by_category_data=reservations_by_category_data)

@bp.route('/data')
@login_required
def dashboard_data():
    total_cars = db.session.query(func.count(Car.id)).scalar() or 0
    available_cars = db.session.query(func.count(Car.id)).filter(Car.status == 0).scalar() or 0

    return jsonify({
        "available_cars": available_cars,
        "occupied_cars": total_cars - available_cars
    })

