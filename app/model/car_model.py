from app.extensions import db

from app.extensions import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    car_type = db.Column(db.String(100), nullable=False)  # SUV, Sedán, etc.
    plate = db.Column(db.String(20), nullable=False)
    fabrication_year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    chairs = db.Column(db.Integer, nullable=False)  # Capacidad de pasajeros
    fuel = db.Column(db.String(100), nullable=False)  # Gasolina, Diesel, etc.
    kilometer = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(100), nullable=False)  # Automático, Manual
    power = db.Column(db.Integer, nullable=False)  # Potencia en HP
    status = db.Column(db.String(50), nullable=False)  # Disponible, Mantenimiento, etc.
    gps = db.Column(db.Boolean, default=False)
    ac = db.Column(db.Boolean, default=False)
    bluetooth = db.Column(db.Boolean, default=False)
    rear_camera = db.Column(db.Boolean, default=False)
    parking_sensors = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50), nullable=False)  # Económico, Premium, etc.
    daily_rate = db.Column(db.Float, nullable=False)  # Tarifa diaria
    insurance_date = db.Column(db.Date, nullable=False)  # Seguro vigente hasta
    itv_date = db.Column(db.Date, nullable=False)  # Fecha de ITV/Revisión
    photos = db.Column(db.String(500), nullable=True)  # Ruta(s) de las fotos del vehículo
    description = db.Column(db.Text, nullable=True)  # Descripción adicional