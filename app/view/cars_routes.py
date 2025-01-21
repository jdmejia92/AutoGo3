from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..controller.car_controller import list_all_cars, create_car, validate_car_data, handle_photos, get_car_by_id, update_car, list_cars_for_users
from app.extensions import db
from ..extensions import app

bp = Blueprint('cars', __name__, url_prefix='/cars')

@bp.route('/')
def list_cars():
    return list_all_cars()

@bp.route('/cars')
def user_cars():
    cars = list_cars_for_users(request=request)
    return render_template('cars/user_cars.html', cars=cars.items, pagination=cars)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_car_route():
    if request.method == 'POST':
        form_data = {
            'brand': request.form.get('brand', '').strip(),
            'model': request.form.get('model', '').strip(),
            'year': request.form.get('year', '').strip(),
            'plate': request.form.get('plate', '').strip(),
            'color': request.form.get('color', '').strip(),
            'capacity': request.form.get('capacity', '').strip(),
            'type': request.form.get('type', '').strip(),
            'transmission': request.form.get('transmission', '').strip(),
            'fuel': request.form.get('fuel', '').strip(),
            'kilometer': request.form.get('kilometer', '').strip(),
            'power': request.form.get('power', '').strip(),
            'status': request.form.get('status', '').strip(),
            'category': request.form.get('category', '').strip(),
            'daily_rate': request.form.get('daily_rate', '').strip(),
            'insurance_date': request.form.get('insurance_date', '').strip(),
            'itv_date': request.form.get('itv_date', '').strip()
        }

        # Validate the form data
        errors = validate_car_data(form_data)
        if errors:
            flash('Por favor corregir los siguientes errores: ' & errors, 'error')
            return render_template('cars/create.html', form=request.form)

        # Process photos
        photos = request.files.getlist('photos')
        photo_paths = handle_photos(photos, app.config['UPLOAD_FOLDER'])

        # Create the car object
        vehicle = create_car(**form_data)

        # Handle successful creation and redirect
        return redirect(url_for('cars.list_cars'))

    return render_template('cars/create.html')

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_car_route(id):
    vehicle = get_car_by_id(id)
    
    if request.method == 'POST':
        form_data = {
            'brand': request.form.get('brand', '').strip(),
            'model': request.form.get('model', '').strip(),
            'year': request.form.get('year', '').strip(),
            'plate': request.form.get('plate', '').strip(),
            'color': request.form.get('color', '').strip(),
            'capacity': request.form.get('capacity', '').strip(),
            'type': request.form.get('type', '').strip(),
            'transmission': request.form.get('transmission', '').strip(),
            'fuel': request.form.get('fuel', '').strip(),
            'kilometer': request.form.get('kilometer', '').strip(),
            'power': request.form.get('power', '').strip(),
            'status': request.form.get('status', '').strip(),
            'category': request.form.get('category', '').strip(),
            'daily_rate': request.form.get('daily_rate', '').strip(),
            'insurance_date': request.form.get('insurance_date', '').strip(),
            'itv_date': request.form.get('itv_date', '').strip()
        }

        # Validate the form data
        errors = validate_car_data(form_data)
        if errors:
            flash('Por favor corregir los siguientes errores: ' & errors, 'error')
            return render_template('cars/update.html', vehicle=vehicle, form=request.form)

        # Process photos
        photos = request.files.getlist('photos')
        photo_paths = handle_photos(photos, app.config['UPLOAD_FOLDER'])

        update_car(
            id, 
            brand=form_data.get('brand'), 
            model=form_data.get('model'), 
            status=form_data.get('status'), 
            car_type=form_data.get('type'), 
            transmission=form_data.get('transmission'), 
            fuel=form_data.get('fuel'), 
            kilometer=form_data.get('kilometer'), 
            power=form_data.get('power'), 
            gps=request.form.get('gps') == 'on',
            ac=request.form.get('ac') == 'on', 
            bluetooth=request.form.get('bluetooth') == 'on', 
            rear_camera=request.form.get('rear_camera') == 'on', 
            parking_sensors=request.form.get('parking_sensors') == 'on', 
            category=form_data.get('category'), 
            daily_rate=form_data.get('daily_rate'), 
            insurance_date=form_data.get('insurance_date'), 
            itv_date=form_data.get('itv_date'), 
            photos=photo_paths,
            description=request.form.get('description')
        )

        return redirect(url_for('cars.list_cars'))

    return render_template('cars/update.html', vehicle=vehicle)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_car(id):
    vehicle = Car.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('cars.list_cars'))

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
