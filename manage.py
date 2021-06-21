from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app
from src.commands import GunicornServer
from src.utils.common_methods import scan_routes, setup_owner_user, setup_accounts_user, setup_support_user, \
    init_system_settings, sync_system_settings
from src.utils.firebase_utils import login_user

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=3000)
@manager.option('-w', '--workers', dest='workers', type=int, default=2)
def server(host, port, workers):
    GunicornServer(host, port, workers)


@manager.command
def list_routes():
    scan_routes(app)


@manager.command
def sync_system():
    sync_system_settings()


@manager.command
def init_system():
    init_system_settings()


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
