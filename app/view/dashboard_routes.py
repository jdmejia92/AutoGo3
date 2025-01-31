from flask import Blueprint, render_template
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

    # 1️⃣ Cantidad total de vehículos y disponibles
    total_cars = db.session.query(func.count(Car.id)).scalar() or 0
    available_cars = db.session.query(func.count(Car.id)).filter(Car.status == 0).scalar() or 0  # 0 = Disponible

    # 2️⃣ Total de reservas en el mes actual
    reservations_this_month = db.session.query(func.count(Reservation.id)).filter(
        Reservation.pickup_datetime >= first_day
    ).scalar() or 0

    # 3️⃣ Tasa de ocupación
    occupancy_rate = (reservations_this_month / total_cars * 100) if total_cars > 0 else 0

    # 4️⃣ Ingresos del mes (sin `price`, usando `daily_rate`)
    monthly_income = db.session.query(
        func.sum(func.extract('day', Reservation.return_datetime - Reservation.pickup_datetime) * Car.daily_rate)
    ).select_from(Reservation).join(Car, Car.id == Reservation.car_id).filter(
        Reservation.pickup_datetime >= first_day
    ).scalar() or 0

    # 5️⃣ Distribución de flota por tipo de vehículo
    fleet_distribution = {
        "Sedán": db.session.query(func.count(Car.id)).filter(Car.car_type.ilike("sedan")).scalar() or 0,
        "SUV": db.session.query(func.count(Car.id)).filter(Car.car_type.ilike("suv")).scalar() or 0,
        "Compacto": db.session.query(func.count(Car.id)).filter(Car.car_type.ilike("compact")).scalar() or 0,
        "Van": db.session.query(func.count(Car.id)).filter(Car.car_type.ilike("van")).scalar() or 0
    }

    # 6️⃣ Ingresos históricos por mes sin usar `price`
    income_by_month = db.session.query(
        func.date_trunc('month', Reservation.pickup_datetime).label("month"),
        func.sum(func.extract('day', Reservation.return_datetime - Reservation.pickup_datetime) * Car.daily_rate).label("income")
    ).select_from(Reservation).join(Car, Car.id == Reservation.car_id).group_by("month").all()

    # Convertir en listas para gráficos
    months = [row.month.strftime('%Y-%m') for row in income_by_month]
    income_values = [row.income for row in income_by_month]

    return render_template('reports/dashboard.html',
                           available_cars=available_cars,
                           total_cars=total_cars,
                           reservations_this_month=reservations_this_month,
                           occupancy_rate=round(occupancy_rate, 2),
                           monthly_income=monthly_income,
                           fleet_distribution=list(fleet_distribution.values()),
                           months=months,
                           income_values=income_values)
