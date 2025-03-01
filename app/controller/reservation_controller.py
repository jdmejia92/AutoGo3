from app.extensions import db
from ..model.reservation_model import Reservation
from datetime import datetime

def list_all_reservations(superadmin=False):
    if superadmin:
        return Reservation.query.all()
    return []

def list_reservations_controller(id):
    return Reservation.query.filter_by(user_id=id).all()

def create_reservation_controller(user_id, car_id, pickup_datetime, return_datetime, pickup_location, return_location, additional_driver=False, additional_driver_name=None, additional_driver_license=None, insurance_type='', payment_method='', terms_accepted=False, comments=None):
    try:
        pickup_datetime = datetime.fromisoformat(pickup_datetime)
        return_datetime = datetime.fromisoformat(return_datetime)
    except ValueError as e:
        print(e)
        return ('Error en el formato de fecha', 'warning')
    try:
        reservation = Reservation(
            user_id=user_id,
            car_id=car_id,
            pickup_datetime=pickup_datetime,
            return_datetime=return_datetime,
            pickup_location=pickup_location,
            return_location=return_location,
            additional_driver=additional_driver,
            additional_driver_name=additional_driver_name,
            additional_driver_license=additional_driver_license,
            insurance_type=insurance_type,
            payment_method=payment_method,
            terms_accepted=terms_accepted,
            comments=comments,
            status='pendiente'
        )
        db.session.add(reservation)
        db.session.commit()
    except Exception as e:
        return ('Error al crear la reserva', 'danger')
    return ('Reserva exitosa', 'success')

def get_reservation_by_id(reservation_id):
    return Reservation.query.get(reservation_id)

def update_reservation(reservation_id, pickup_datetime=None, return_datetime=None, pickup_location=None, return_location=None, status=None):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        if pickup_datetime:
            reservation.pickup_datetime = pickup_datetime
        if return_datetime:
            reservation.return_datetime = return_datetime
        if pickup_location:
            reservation.pickup_location = pickup_location
        if return_location:
            reservation.return_location = return_location
        if status:
            reservation.status = status
        db.session.commit()
    return reservation

def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()