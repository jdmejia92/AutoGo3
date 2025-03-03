from flask import Flask
from app.extensions import db, migrate, login
from .controller.admin_controller import create_default_super_admin
from flask import render_template
import os

def create_app():
    app = Flask(__name__)

    # Configuración básica de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicialización de extensiones
    from .model.user_model import load_user_model
    from .model.admin_model import load_admin
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Configuración de Flask-Login
    @login.user_loader
    def load_user(email):
        user = load_user_model(email)
        if user:
            return user
        return load_admin(email)

    login.login_view = "auth.login"
    login.login_message = "Inicia sesión para acceder a esta página."
    login.login_message_category = "warning"

    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('404.html'), 404

    # Registro de blueprints y tareas iniciales
    from .view import user_routes, reservations_routes, cars_routes, base_routes, auth_routes, dashboard_routes 
    with app.app_context():
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cars_routes.bp)
        app.register_blueprint(reservations_routes.bp)
        app.register_blueprint(base_routes.bp)
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(dashboard_routes.bp)  
        db.create_all()  
        create_default_super_admin()  

    return app
