from flask import current_app as app

from soul_cycle import create_app
from soul_cycle.user.models import User
from extensions import db
import config

from flask_script import Manager

manager = Manager(create_app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)


@manager.command
def create():
    db.create_all()

@manager.command
def recreate():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    manager.add_option("-c", "--config", dest="config", required=False, default=config.DevConfig)
    manager.run()
