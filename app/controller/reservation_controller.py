from app import db
from model.reservation_model import Reservation

def create_reservation(user_id, vehicle_id, start_date, end_date):
    reservation = Reservation(user_id=user_id, vehicle_id=vehicle_id, start_date=start_date, end_date=end_date)
    db.session.add(reservation)
    db.session.commit()
    return reservation

def get_reservation_by_id(reservation_id):
    return Reservation.query.get(reservation_id)

def update_reservation(reservation_id, start_date=None, end_date=None):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        if start_date:
            reservation.start_date = start_date
        if end_date:
            reservation.end_date = end_date
        db.session.commit()
    return reservation

def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
