from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from ..model.car_model import Car
from app.extensions import db

bp = Blueprint('cars', __name__, url_prefix='/cars')

@bp.route('/')
def list_cars():
    vehicles = Car.query.all()
    return render_template('cars/list.html', vehicles=vehicles)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        plate = request.form['plate']
        color = request.form['color']
        capacity = request.form['capacity']
        type_ = request.form['type']
        transmission = request.form['transmission']
        fuel = request.form['fuel']
        kilometer = request.form['kilometer']
        power = request.form['power']
        status = request.form['status']
        gps = 'gps' in request.form
        ac = 'ac' in request.form
        bluetooth = 'bluetooth' in request.form
        rear_camera = 'rear_camera' in request.form
        parking_sensors = 'parking_sensors' in request.form
        category = request.form['category']
        daily_rate = request.form['daily_rate']
        insurance_date = request.form['insurance_date']
        itv_date = request.form['itv_date']
        
        # Subir las fotos si existen
        photos = request.files.getlist('photos')
        # Aquí podrías guardar las fotos en una carpeta y agregar las rutas a la base de datos

        # Crear el vehículo
        vehicle = Car(
            brand=brand,
            model=model,
            fabrication_year=year,
            plate=plate,
            color=color,
            capacity=capacity,
            type=type_,
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
            itv_date=itv_date
        )

        # Guardar el vehículo en la base de datos
        db.session.add(vehicle)
        db.session.commit()

        return redirect(url_for('cars.list_cars'))
    
    return render_template('cars/create.html')

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_car(id):
    vehicle = Car.query.get_or_404(id)
    if request.method == 'POST':
        vehicle.brand = request.form['brand']
        vehicle.model = request.form['model']
        db.session.commit()
        return redirect(url_for('cars.list_cars'))
    return render_template('cars/update.html', vehicle=vehicle)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_car(id):
    vehicle = Car.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('cars.list_cars'))

@bp.route('/user-cars')
def user_cars():
    page = request.args.get('page', 1, type=int)
    cars = Car.query.paginate(page=page, per_page=12)
    return render_template('cars/user_cars.html', cars=cars.items, pagination=cars)

@bp.route('/pricing')
def pricing():
    cars = [
        {
            'id': 1,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-1.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
        {
            'id': 2,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-2.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
        {
            'id': 3,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-3.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
        {
            'id': 4,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-4.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
        {
            'id': 5,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-5.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
        {
            'id': 6,
            'name': 'Chevrolet SUV Car',
            'image': 'images/car-6.jpg',
            'rating': 5,
            'hourly_rate': 10.99,
            'daily_rate': 60.99,
            'monthly_rate': 995.99,
        },
    ]
    return render_template('cars/pricing.html', cars=cars)
