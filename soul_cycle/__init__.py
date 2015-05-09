from flask import Flask
import logging

from extensions import db, login_manager, bcrypt, admin, bootstrap

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    formatter = logging.Formatter(app.config['LOG_FORMAT'])
    logger_handle = logging.FileHandler(filename=app.config['LOG_FILENAME'])
    logger_handle.setFormatter(formatter)
    logger_handle.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(logger_handle)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    db.init_app(app)

    bcrypt.init_app(app)

    bootstrap.init_app(app)

    admin.init_app(app)

    from . import user
    app.register_blueprint(user.bp)

    return app
