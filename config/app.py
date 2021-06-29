import os

from lagom.integrations.flask import FlaskIntegration
from lagom import Singleton, Container
from src.services import FileSystemService, MediaService, RoleService, StoreService, UserService, SettingsService
from .setup import app

APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True

containers = Container()
settingsService = SettingsService(app)
fileSystemService = FileSystemService(app, settingsService)
mediaService = MediaService(app, fileSystemService)
containers[FileSystemService] = fileSystemService
containers[RoleService] = RoleService(app)
containers[MediaService] = mediaService
containers[UserService] = UserService(app, fileSystemService, mediaService)
containers[StoreService] = StoreService(app, fileSystemService, mediaService)
containers[SettingsService] = settingsService

app = FlaskIntegration(app, containers)
