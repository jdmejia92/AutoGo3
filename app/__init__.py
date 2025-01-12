from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_reservation.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .view import user_routes, reservations_routes, cars_routes, base_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cars_routes.bp)
        app.register_blueprint(reservations_routes.bp)
        app.register_blueprint(base_routes.bp)
        db.create_all()

    return app