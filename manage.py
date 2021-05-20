from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app
from src.utils.common_methods import scan_routes, setup_owner_user

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    scan_routes(app)


@manager.command
@manager.add_option("-e", "--email", dest="email", required=True)
@manager.add_option("-p", "--password", dest="password", required=True)
def setup_owner(email, password):
    setup_owner_user(email, password)


if __name__ == '__main__':
    manager.run()
