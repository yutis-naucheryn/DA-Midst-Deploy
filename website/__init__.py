from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, static_folder='static', static_url_path='/static')
db = SQLAlchemy()
mail = Mail()  # Initialize Mail object
DB_NAME = "da-midst_database.db"


def create_app():
    app.config['SECRET_KEY'] = 'uumfyp281205'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    mail.init_app(app)  # Configure Mail with the Flask app

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
            return User.query.get(int(id))  #look for the primary key

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():     #extra line of code to settle [TypeError: SQLAlchemy.create_all() got an unexpected keyword argument 'app'] issues
            db.create_all()     #modified line of code, original code can refer to the tutotial video
        print('Created Database!')