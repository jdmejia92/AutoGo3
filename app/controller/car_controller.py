from app.extensions import db
from ..model.car_model import Car
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app  # <--- Importa current_app
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_all_cars():
    """Fetch all cars from the database."""
    try:
        cars = Car.query.all()
        return cars
    except Exception as e:
        # Retorna un mensaje de error o lanza la excepción según tu manejo global
        return f"Error al obtener la lista de carros: {str(e)}", 'error'

def list_cars_for_users(request):
    """Fetch paginated cars for users."""
    page = request.args.get('page', 1, type=int)
    try:
        # Se filtran los carros con status==0 (disponibles) y se aplican 6 elementos por página
        cars = Car.query.filter(Car.status == 0).paginate(page=page, per_page=6)
        return cars
    except Exception as e:
        # Registra el error y devuelve None para manejarlo en la vista
        current_app.logger.error(f"Error al obtener la lista de carros paginada: {str(e)}")
        return None

def get_car_by_id(car_id):
    """Fetch a single car by ID."""
    return Car.query.get(car_id)

def create_car(
    brand, model, car_type, plate, fabrication_year, color, chairs, fuel,
    kilometer, transmission, power, status, category, daily_rate, insurance_date, itv_date,
    gps=False, ac=False, bluetooth=False, rear_camera=False, parking_sensors=False,
    photos=None, description=None
):
    """Create a new car in the database."""
    try:
        car = Car(
            brand=brand,
            model=model,
            car_type=car_type,
            plate=plate,
            fabrication_year=fabrication_year,
            color=color,
            chairs=chairs,
            fuel=fuel,
            kilometer=kilometer,
            transmission=transmission,
            power=power,
            status=status,
            gps=gps,
            ac=ac,
            bluetooth=bluetooth,
            rear_camera=rear_camera,
            parking_sensors=parking_sensors,
            category=category,
            daily_rate=daily_rate,
            insurance_date=datetime.strptime(insurance_date, '%Y-%m-%d'),
            itv_date=datetime.strptime(itv_date, '%Y-%m-%d'),
            photos=",".join(photos) if photos else None,
            description=description
        )
        db.session.add(car)
        db.session.commit()
        return car
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al crear el vehículo: {str(e)}")

def validate_car_data(form_data):
    """Validate form data and return errors if any."""
    errors = []

    if not form_data['brand']:
        errors.append("La marca es requerida.")
    if not form_data['model']:
        errors.append("El modelo es requerido.")
    if (not str(form_data['fabrication_year']).isdigit() or 
        int(form_data['fabrication_year']) < 1900 or 
        int(form_data['fabrication_year']) > datetime.now().year):
        errors.append("El año de fabricación debe estar entre 1900 y el año actual.")
    if not form_data['plate']:
        errors.append("La matrícula es requerida.")
    try:
        datetime.strptime(form_data['insurance_date'], '%Y-%m-%d')
        datetime.strptime(form_data['itv_date'], '%Y-%m-%d')
    except ValueError:
        errors.append("Las fechas deben estar en el formato AAAA-MM-DD.")

    return errors

def handle_photos(photos, upload_folder):
    """Handle photo uploads."""
    photo_paths = []
    for photo in photos:
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(upload_folder, filename)
            try:
                photo.save(photo_path)
                photo_paths.append(f"/static/uploads/{filename}")  # Ruta accesible desde el servidor
            except Exception as e:
                raise ValueError(f"Error al guardar la foto {filename}: {str(e)}")
    return photo_paths

def update_car(
    car_id, brand=None, model=None, car_type=None, plate=None, fabrication_year=None, color=None, chairs=None,
    fuel=None, kilometer=None, transmission=None, power=None, status=None, category=None,
    daily_rate=None, insurance_date=None, itv_date=None, gps=None, ac=None, bluetooth=None,
    rear_camera=None, parking_sensors=None, photos=None, description=None
):
    """Update an existing car in the database."""
    car = Car.query.get(car_id)
    if car:
        try:
            if brand:
                car.brand = brand
            if model:
                car.model = model
            if car_type:
                car.car_type = car_type
            if plate:
                car.plate = plate
            if fabrication_year is not None:
                car.fabrication_year = fabrication_year
            if color:
                car.color = color
            if chairs is not None:
                car.chairs = chairs
            if fuel:
                car.fuel = fuel
            if kilometer is not None:
                car.kilometer = kilometer
            if transmission:
                car.transmission = transmission
            if power is not None:
                car.power = power
            if status:
                car.status = status
            if category:
                car.category = category
            if daily_rate is not None:
                car.daily_rate = daily_rate
            if insurance_date:
                car.insurance_date = datetime.strptime(insurance_date, '%Y-%m-%d')
            if itv_date:
                car.itv_date = datetime.strptime(itv_date, '%Y-%m-%d')
            if photos:
                car.photos = ",".join(photos)
            if description:
                car.description = description
            if gps is not None:
                car.gps = gps
            if ac is not None:
                car.ac = ac
            if bluetooth is not None:
                car.bluetooth = bluetooth
            if rear_camera is not None:
                car.rear_camera = rear_camera
            if parking_sensors is not None:
                car.parking_sensors = parking_sensors

            db.session.commit()
            return car
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al actualizar el vehículo: {str(e)}")
    else:
        raise ValueError("El vehículo no fue encontrado.")

def delete_car(car_id):
    """Delete a car from the database."""
    car = Car.query.get(car_id)
    if car:
        try:
            db.session.delete(car)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al eliminar el vehículo: {str(e)}")
