import os

from flask_socketio import SocketIO
from lagom import Singleton, Container
from lagom.integrations.flask import FlaskIntegration
from .api import app
from src.services.filesystem import FileSystemService
from src.services.media import MediaService
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService

container = Container()
container[FileSystemService] = FileSystemService(app.logger)
container[RolesService] = Singleton(lambda: RolesService())
container[UserService] = Singleton(lambda: UserService())
container[StoreService] = Singleton(lambda: StoreService())
container[MediaService] = Singleton(lambda: MediaService())
app = FlaskIntegration(app, container)
APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True
socketio = SocketIO(app.flask_app, logger=True, debug=APP_DEBUG_MODE, host="0.0.0.0", engineio_logger=APP_DEBUG_MODE)
