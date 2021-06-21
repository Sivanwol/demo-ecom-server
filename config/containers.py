import os
from socket import SocketIO

from lagom import Singleton
from config import app
from src.services.filesystem import FileSystemService
from src.services.media import MediaService
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService
from lagom.integrations.flask import FlaskContainer


app = FlaskContainer(app)
app[FileSystemService] = Singleton(lambda: FileSystemService())
app[RolesService] = Singleton(lambda: RolesService())
app[UserService] = Singleton(lambda: UserService())
app[StoreService] = Singleton(lambda: StoreService())
app[MediaService] = Singleton(lambda: MediaService())

APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True
socketio = SocketIO(app, logger=True, debug=APP_DEBUG_MODE, host="0.0.0.0", engineio_logger=APP_DEBUG_MODE)