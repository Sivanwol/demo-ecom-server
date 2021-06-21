import os

from flask_socketio import SocketIO
from lagom import Singleton, Container
from lagom.integrations.flask import FlaskIntegration
from .api import app
from src.services import FileSystemService, MediaService, RolesService, StoreService, UserService, SettingsService

container = Container()
container[FileSystemService] = FileSystemService(app.logger)
container[RolesService] = RolesService(app.logger)
container[UserService] = UserService(app.logger, container[FileSystemService])
container[StoreService] = StoreService(app.logger, container[FileSystemService])
container[SettingsService] = SettingsService(app.logger)
container[MediaService] = MediaService(app.logger)
app = FlaskIntegration(app, container)
APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True
socketio = SocketIO(app.flask_app, logger=True, debug=APP_DEBUG_MODE, host="0.0.0.0", engineio_logger=APP_DEBUG_MODE)
