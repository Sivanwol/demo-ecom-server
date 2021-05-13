from flask_migrate import MigrateCommand
from flask_script import Manager
from app import app
from src.utils.common_methods import scan_routes

manager = Manager(app)

# Database migrations command
manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    scan_routes(app)


if __name__ == '__main__':
    manager.run()
