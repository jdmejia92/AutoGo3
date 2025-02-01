from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from ..controller.car_controller import (
    list_all_cars,
    create_car,
    validate_car_data,
    handle_photos,
    get_car_by_id,
    update_car,
    list_cars_for_users,
    delete_car
)

bp = Blueprint('cars', __name__, url_prefix='/cars')

@bp.route('/')
def list_cars():
    cars = list_all_cars()
    print(f"Vehículos disponibles: {cars}") 
    return render_template('cars/list.html', cars=cars)

@bp.route('/user-cars')
def user_cars():
    cars = list_cars_for_users(request)
    return render_template('cars/user_cars.html', cars=cars.items, pagination=cars)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_car_route():
    if request.method == 'POST':
        form_data = {
            'brand': request.form.get('brand', '').strip(),
            'model': request.form.get('model', '').strip(),
            'fabrication_year': request.form.get('fabrication_year', '').strip(),
            'plate': request.form.get('plate', '').strip(),
            'color': request.form.get('color', '').strip(),
            'chairs': request.form.get('chairs', '').strip(),
            'car_type': request.form.get('type', '').strip(),
            'transmission': request.form.get('transmission', '').strip(),
            'fuel': request.form.get('fuel', '').strip(),
            'kilometer': request.form.get('kilometer', '').strip(),
            'power': request.form.get('power', '').strip(),
            'status': request.form.get('status', '').strip(),
            'category': request.form.get('category', '').strip(),
            'daily_rate': request.form.get('daily_rate', '').strip(),
            'insurance_date': request.form.get('insurance_date', '').strip(),
            'itv_date': request.form.get('itv_date', '').strip(),
            'description': request.form.get('description', '').strip()
        }

        errors = validate_car_data(form_data)
        if errors:
            flash(f"Por favor corrige los siguientes errores: {errors}", 'error')
            return render_template('cars/create.html', form=request.form)

        photos = request.files.getlist('photos')
        photo_paths = handle_photos(photos, current_app.config['UPLOAD_FOLDER'])

        create_car(**form_data, photos=photo_paths)

        flash('Auto creado exitosamente.', 'success')
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
            'fabrication_year': request.form.get('fabrication_year', '').strip(),
            'plate': request.form.get('plate', '').strip(),
            'color': request.form.get('color', '').strip(),
            'chairs': request.form.get('chairs', '').strip(),
            'car_type': request.form.get('type', '').strip(),
            'transmission': request.form.get('transmission', '').strip(),
            'fuel': request.form.get('fuel', '').strip(),
            'kilometer': request.form.get('kilometer', '').strip(),
            'power': request.form.get('power', '').strip(),
            'status': request.form.get('status', '').strip(),
            'category': request.form.get('category', '').strip(),
            'daily_rate': request.form.get('daily_rate', '').strip(),
            'insurance_date': request.form.get('insurance_date', '').strip(),
            'itv_date': request.form.get('itv_date', '').strip(),
            'description': request.form.get('description', '').strip()
        }

        errors = validate_car_data(form_data)
        if errors:
            flash(f"Por favor corrige los siguientes errores: {errors}", 'error')
            return render_template('cars/update.html', vehicle=vehicle, form=request.form)

        photos = request.files.getlist('photos')
        photo_paths = handle_photos(photos, current_app.config['UPLOAD_FOLDER'])

        update_car(
            id,
            brand=form_data.get('brand'),
            model=form_data.get('model'),
            fabrication_year=form_data.get('fabrication_year'),
            plate=form_data.get('plate'),
            color=form_data.get('color'),
            chairs=form_data.get('chairs'),
            car_type=form_data.get('car_type'),
            transmission=form_data.get('transmission'),
            fuel=form_data.get('fuel'),
            kilometer=form_data.get('kilometer'),
            power=form_data.get('power'),
            status=form_data.get('status'),
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
            description=form_data.get('description')
        )

        flash('Auto actualizado exitosamente.', 'success')
        return redirect(url_for('cars.list_cars'))

    return render_template('cars/update.html', vehicle=vehicle)

@bp.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_car_route(id):
    delete_car(id)
    flash('Auto eliminado exitosamente.', 'success')
    return redirect(url_for('cars.list_cars'))


@bp.route('/details/<int:id>')
def view_car(id):
    car = get_car_by_id(id)
    if not car:
        flash("El vehículo no existe.", "error")
        return redirect(url_for('cars.list_cars'))
    
    related_cars = list_all_cars()[:3]  # Ejemplo: obtener 3 autos relacionados

    return render_template('cars/detail.html', car=car, related_cars=related_cars)
















@bp.route('/pricing')
def pricing():
    """Ruta para mostrar la página de precios"""
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
