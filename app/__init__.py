from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from celery import Celery
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)

    with app.app_context():
        db.create_all()

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.instructor import instructor_bp
    from app.routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(student_bp)

    return app

@celery.task
def send_reminder_email(email, message):
    # Task to send reminder emails
    pass