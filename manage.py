from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app
from src.utils.common_methods import scan_routes, setup_owner_user
from src.utils.firebase_utils import login_user

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    scan_routes(app)


@manager.command
@manager.option("-e", "--email", dest="email", required=True)
@manager.option("-p", "--password", dest="password", required=True)
def setup_owner(email, password):
    setup_owner_user(email, password)


@manager.command
@manager.option("-e", "--email", dest="email", required=True)
@manager.option("-p", "--password", dest="password", required=True)
def get_id_token(email, password):
    user = login_user(email, password)
    print(user)


if __name__ == '__main__':
    manager.run()
