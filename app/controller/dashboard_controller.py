from app.extensions import db
from app.model.user_model import User
from app.model.reservation_model import Reservation
from app.model.car_model import Car
from sqlalchemy import func

def get_dashboard_data():
    """ Obtiene los datos clave para el dashboard """

    # Contar reservas según estado
    active_reservations = Reservation.query.filter(Reservation.status == 'activa').count()
    completed_reservations = Reservation.query.filter(Reservation.status == 'completada').count()
    canceled_reservations = Reservation.query.filter(Reservation.status == 'cancelada').count()

    # Estado de los vehículos
    available_cars = Car.query.filter_by(status=0).count()
    in_use_cars = Car.query.filter_by(status=1).count()

    # Calcular ingresos mensuales basados en las reservas
    monthly_income = (
        db.session.query(
            func.sum(Car.daily_rate * (func.extract('epoch', Reservation.return_datetime - Reservation.pickup_datetime) / 86400))
        )
        .select_from(Reservation)  # 🔹 Se especifica que la consulta parte de Reservation
        .join(Car, Car.id == Reservation.car_id)
        .scalar()
    ) or 0

    # Datos para gráficos
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    reservations_data = [30, 45, 55, 40, 60, 70]  # Esto debería extraerse de la BD según reservas por mes

    return {
        "active_reservations": active_reservations,
        "completed_reservations": completed_reservations,
        "canceled_reservations": canceled_reservations,
        "available_cars": available_cars,
        "in_use_cars": in_use_cars,
        "monthly_income": monthly_income,
        "months": months,
        "reservations_data": reservations_data
    }