from flask_login import LoginManager
login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_admin import Admin
admin = Admin()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap()
