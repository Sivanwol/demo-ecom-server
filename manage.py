from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app
from src.utils.common_methods import scan_routes, setup_owner_user, setup_accounts_user, setup_support_user
from src.utils.firebase_utils import login_user

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    scan_routes(app)


@manager.command
def setup_owner(email, password):
    setup_owner_user(email, password)

@manager.command
def setup_support(email, password):
    setup_support_user(email, password)

@manager.command
def setup_accounts(email, password):
    setup_accounts_user(email, password)


@manager.command
def get_id_token(email, password):
    user = login_user(email, password)
    print(user)


if __name__ == '__main__':
    manager.run()
