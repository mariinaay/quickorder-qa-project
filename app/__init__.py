from pathlib import Path
from flask import Flask, send_from_directory
from config import Config
from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.get("/openapi.yaml")
    def openapi_spec():
        return send_from_directory(Path(app.root_path).parent, "openapi.yaml", mimetype="application/yaml")

    @app.get("/docs/")
    def swagger_ui():
        return send_from_directory(app.static_folder, "swagger.html")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Connectez-vous pour accéder à cette page."

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.shop import shop_bp
    from .routes.api import api_bp
    from .routes.orders import orders_bp
    from .routes.admin import admin_bp
    from .routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(profile_bp)

    with app.app_context():
        db.create_all()

    return app
