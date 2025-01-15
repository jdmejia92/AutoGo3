from flask import Flask
from app.extensions import db, migrate, login
from .controller.user_controller import admin_user
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración básica de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')  # Clave secreta predeterminada



    # Inicialización de extensiones
    from .model.user_model import load_user
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Configuración de Flask-Login
    login.user_loader(load_user)
    login.login_view = "users.login"

    # Registro de blueprints y tareas iniciales
    with app.app_context():
        from .view import user_routes, reservations_routes, cars_routes, base_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cars_routes.bp)
        app.register_blueprint(reservations_routes.bp)
        app.register_blueprint(base_routes.bp)
        db.create_all()  # Crear tablas en la base de datos si no existen
        admin_user()  # Crear usuario administrador

    return app
