from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..model.car_model import Car
from ..controller.car_controller import list_cars_for_users
from ..controller.reservation_controller import create_reservation_controller, update_reservation, delete_reservation, get_reservation_by_id, list_reservations_controller, list_all_reservations

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/all')
@login_required
def list_all_reservations():
    if not current_user.is_super_admin():
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('reservations.list_reservations'))
    
    reservations = list_all_reservations(current_user.tier)
    if reservations == []:
        flash('El usuario no es admin o no hay reservas registradas.', 'info')
    return render_template('reservations/list.html', reservations=reservations)

@bp.route('/')
@login_required
def list_reservations():
    reservations = list_reservations_controller(current_user.id)
    return render_template('reservations/list.html', reservations=reservations)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_reservation():
    if request.method == 'POST':
        try:
            car_id = request.form.get('car_category')
            pickup_datetime = request.form.get('pickup_datetime')
            return_datetime = request.form.get('return_datetime')
            pickup_location = request.form.get('pickup_location')
            return_location = request.form.get('return_location')
            additional_driver = 'additional_driver' in request.form
            additional_driver_name = request.form.get('additional_driver_name', '')
            additional_driver_license = request.form.get('additional_driver_license', '')
            insurance_type = request.form.get('insurance_type')
            payment_method = request.form.get('payment_method', '')
            terms_accepted = 'terms_accepted' in request.form
            comments = request.form.get('comments', '')

            reservation = create_reservation_controller(
                user_id=current_user.id,
                car_id=car_id,
                pickup_datetime=pickup_datetime,
                return_datetime=return_datetime,
                pickup_location=pickup_location,
                return_location=return_location,
                additional_driver=additional_driver,
                additional_driver_name=additional_driver_name,
                additional_driver_license=additional_driver_license,
                insurance_type=insurance_type,
                payment_method=payment_method,
                terms_accepted=terms_accepted,
                comments=comments
            )

            flash(reservation[0], reservation[1])

            # Redirigir según el tipo de usuario
            return redirect(url_for('reservations.list_all_reservations' if current_user.is_super_admin() else 'reservations.list_reservations'))

        except Exception as e:
            flash(f'Error al crear la reserva: {str(e)}', 'danger')
            return redirect(url_for('reservations.create_reservation'))

    cars = list_cars_for_users(request)
    return render_template('reservations/create.html', user=current_user, cars=cars)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_reservation(id):
    reservation = get_reservation_by_id(id)
    
    if not reservation or reservation.user_id != current_user.id:
        flash('Reserva no encontrada o no autorizada.', 'danger')
        return redirect(url_for('reservations.list_reservations'))

    cars = list_cars_for_users(request)

    if request.method == 'POST':
        try:
            pickup_datetime = request.form['pickup_datetime']
            return_datetime = request.form['return_datetime']
            pickup_location = request.form['pickup_location']
            return_location = request.form['return_location']
            car_id = request.form['car_id']
            status = request.form.get('status')

            update_reservation(id, pickup_datetime, return_datetime, pickup_location, return_location, car_id, status)
            flash('Reserva actualizada con éxito.', 'success')
            return redirect(url_for('reservations.list_reservations'))
        except Exception as e:
            flash(f'Error al actualizar la reserva: {str(e)}', 'danger')
            return redirect(url_for('reservations.update_reservation', id=id))

    return render_template('reservations/update.html', reservation=reservation, cars=cars)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_reservation(id):
    try:
        reservation = get_reservation_by_id(id)
        if not reservation or reservation.user_id != current_user.id:
            flash('No tienes permiso para eliminar esta reserva.', 'danger')
            return redirect(url_for('reservations.list_reservations'))
        
        delete_reservation(id)
        flash('Reserva eliminada con éxito.', 'success')
        return redirect(url_for('reservations.list_reservations'))
    except Exception as e:
        flash(f'Error al eliminar la reserva: {str(e)}', 'danger')
        return redirect(url_for('reservations.list_reservations'))