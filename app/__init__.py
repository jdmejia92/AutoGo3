from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_reservation.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .view import user_routes
        from .view import reservations_routes
        from .view import cars_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cars_routes.bp)
        app.register_blueprint(reservations_routes.bp)
        db.create_all()

    return app