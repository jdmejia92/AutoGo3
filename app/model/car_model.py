from app.extensions import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    car_type = db.Column(db.String(100), nullable=False)  
    plate = db.Column(db.String(20), nullable=False, unique=True)
    fabrication_year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    chairs = db.Column(db.Integer, nullable=False)  
    fuel = db.Column(db.String(100), nullable=False)  
    kilometer = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(100), nullable=False)  
    power = db.Column(db.Integer, nullable=False)  
    status = db.Column(db.Integer, nullable=False, default=0)  
    gps = db.Column(db.Boolean, default=False)
    ac = db.Column(db.Boolean, default=False)
    bluetooth = db.Column(db.Boolean, default=False)
    rear_camera = db.Column(db.Boolean, default=False)
    parking_sensors = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), nullable=False)  
    daily_rate = db.Column(db.Float, nullable=False)  
    insurance_date = db.Column(db.Date, nullable=False)  
    itv_date = db.Column(db.Date, nullable=False)  
    photo_url = db.Column(db.String(500), nullable=True)  # URL de la imagen en S3 o Cloudinary
    description = db.Column(db.Text, nullable=True)  

class CarPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)  # URL de la imagen
    car = db.relationship('Car', backref=db.backref('photos', lazy=True))