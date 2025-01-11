from flask import Blueprint, render_template, request, redirect, url_for
from ..model.car_model import Car
from app.extensions import db

bp = Blueprint('vehicles', __name__, url_prefix='/cars')

@bp.route('/')
def list_cars():
    vehicles = Car.query.all()
    return render_template('cars/list.html', vehicles=vehicles)

@bp.route('/create', methods=['GET', 'POST'])
def create_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        vehicle = Car(brand=brand, model=model)
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('car.list_cars'))
    return render_template('cars/create.html')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_car(id):
    vehicle = Car.query.get(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('cars.list_car'))