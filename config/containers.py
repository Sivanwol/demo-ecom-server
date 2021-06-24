import os

from flask_socketio import SocketIO
from lagom import Singleton, Container
from lagom.integrations.flask import FlaskIntegration
from .api import app
from src.services import FileSystemService, MediaService, RoleService, StoreService, UserService, SettingsService

container = Container()
fileSystemService = FileSystemService(app.logger)
mediaService = MediaService(app.logger, fileSystemService)
container[FileSystemService] = fileSystemService
container[RoleService] = RoleService(app.logger)
container[MediaService] = mediaService
container[UserService] = UserService(app.logger, fileSystemService, mediaService)
container[StoreService] = StoreService(app.logger, fileSystemService, mediaService)
container[SettingsService] = SettingsService(app.logger)
app = FlaskIntegration(app, container)
APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True
socketio = SocketIO(app.flask_app, logger=True, debug=APP_DEBUG_MODE, host="0.0.0.0", engineio_logger=APP_DEBUG_MODE)
