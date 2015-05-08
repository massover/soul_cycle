from flask import Flask
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.debug = True

    login_manager.init_app(app)

    from flask_bootstrap import Bootstrap
    Bootstrap(app)

    from flask_admin import Admin
    admin = Admin(app)
    
    from . import user
    app.register_blueprint(user.bp)

    return app
