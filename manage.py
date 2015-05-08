from soul_cycle import create_app

from flask_script import Manager

manager = Manager(create_app)

@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == '__main__':
    manager.run()
