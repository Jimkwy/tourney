from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# set database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    #Development config
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config["CACHE_TYPE"] = "null"

    #database config
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    #import database
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #import user models
    from .auth_mod.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # query with primary keys
        return User.query.get(int(user_id))

    # blueprint for non-auth routes
    from .main import main as main_module
    app.register_blueprint(main_module)

    # blueprint for auth routes
    from .auth_mod.auth import auth as auth_module
    app.register_blueprint(auth_module)

    return app

db.create_all(app=create_app())
