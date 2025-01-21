from app.extensions import db
from ..model.car_model import Car
from werkzeug.utils import secure_filename
from datetime import datetime
import os

def list_all_cars():
    try:
        users = Car.query.all()  # Obtiene todos los usuarios
        return users
    except Exception as e:
        return f"Error al obtener la lista de carros: {str(e)}", 'error'
    
def list_cars_for_users(request):
    page = request.args.get('page', 1, type=int)
    cars = Car.query.paginate(page=page, per_page=12)
    return cars

def get_car_by_id(car_id):
    return Car.query.get(car_id)

def create_car(
    brand, model, fabrication_year, plate, color, chairs, car_type, transmission, fuel,
    kilometer, power, status, category, daily_rate, insurance_date, itv_date, gps=False, 
    ac=False, bluetooth=False, rear_camera=False, parking_sensors=False, photos=None, description=None
):
    car = Car(
        brand=brand,
        model=model,
        fabrication_year=fabrication_year,
        plate=plate,
        color=color,
        chairs=chairs,
        car_type=car_type,
        transmission=transmission,
        fuel=fuel,
        kilometer=kilometer,
        power=power,
        status=status,
        gps=gps,
        ac=ac,
        bluetooth=bluetooth,
        rear_camera=rear_camera,
        parking_sensors=parking_sensors,
        category=category,
        daily_rate=daily_rate,
        insurance_date=insurance_date,
        itv_date=itv_date,
        photos=photos,
        description=description
    )
    db.session.add(car)
    db.session.commit()
    return car


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_car_data(form_data):
    """Validate form data and return errors if any."""
    errors = []
    
    # Form validation logic (same as before)
    if not form_data['brand']:
        errors.append("Brand is required.")
    if not form_data['model']:
        errors.append("Model is required.")
    if not form_data['year'].isdigit() or int(form_data['year']) < 1900 or int(form_data['year']) > 2100:
        errors.append("Invalid year.")
    # Add other validation checks here...

    try:
        # Validating date format
        insurance_date = datetime.strptime(form_data['insurance_date'], '%Y-%m-%d')
        itv_date = datetime.strptime(form_data['itv_date'], '%Y-%m-%d')
    except ValueError:
        errors.append("Dates must be in YYYY-MM-DD format.")
    
    return errors

def handle_photos(photos, upload_folder):
    """Handle photo uploads."""
    photo_paths = []
    for photo in photos:
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(upload_folder, filename)
            photo.save(photo_path)
            photo_paths.append(photo_path)
    return photo_paths

def update_car(car_id, brand=None, model=None, status=None, car_type=None, transmission=None, fuel=None,
                kilometer=None, power=None, gps=None, ac=None, bluetooth=None, rear_camera=None, 
                parking_sensors=None, category=None, daily_rate=None, insurance_date=None, itv_date=None, 
                photos=None, description=None):
    car = Car.query.get(car_id)
    if car:
        if brand:
            car.brand = brand
        if model:
            car.model = model
        if status is not None:
            car.status = status
        if car_type:
            car.car_type = car_type
        if transmission:
            car.transmission = transmission
        if fuel:
            car.fuel = fuel
        if kilometer is not None:
            car.kilometer = kilometer
        if power is not None:
            car.power = power
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
        if category:
            car.category = category
        if daily_rate is not None:
            car.daily_rate = daily_rate
        if insurance_date:
            car.insurance_date = insurance_date
        if itv_date:
            car.itv_date = itv_date
        if photos:
            car.photos = photos
        if description:
            car.description = description

        db.session.commit()
    return car


def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()