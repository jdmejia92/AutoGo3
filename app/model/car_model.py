from app.extensions import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    car_type = db.Column(db.String(100), nullable=False) # sedan, suv, van
    plate = db.Column(db.String(20), nullable=False)
    fabrication_year = db.Column(db.Integer, nullable=False)
    chairs = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.String(100), nullable=False) # electric, gas, gnv
    kilometer = db.Column(db.Integer, nullable=False)
    transmision = db.Column(db.String(100), nullable=False) # automatic, manual
    availability = db.Column(db.Boolean, default=True)