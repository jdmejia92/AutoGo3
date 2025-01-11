from app.extensions import db
from model.car_model import Car

def create_car(brand, model, availability=True):
    car = Car(brand=brand, model=model, availability=availability)
    db.session.add(car)
    db.session.commit()
    return car

def get_car_by_id(car_id):
    return Car.query.get(car_id)

def update_car(car_id, brand=None, model=None, availability=None):
    car = Car.query.get(car_id)
    if car:
        if brand:
            car.brand = brand
        if model:
            car.model = model
        if availability is not None:
            car.availability = availability
        db.session.commit()
    return car

def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()