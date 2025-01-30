from app.extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    pickup_datetime = db.Column(db.DateTime, nullable=False)
    return_datetime = db.Column(db.DateTime, nullable=False)
    pickup_location = db.Column(db.String(50), nullable=False)
    return_location = db.Column(db.String(50), nullable=False)
    additional_driver = db.Column(db.Boolean, default=False)
    additional_driver_name = db.Column(db.String(100), nullable=True)
    additional_driver_license = db.Column(db.String(20), nullable=True)
    insurance_type = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    terms_accepted = db.Column(db.Boolean, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendiente')

    user = db.relationship('User', backref='reservations')
    car = db.relationship('Car', backref='reservations')
