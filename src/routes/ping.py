import os

from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from config import settings
from config.api import app as current_app
from src.utils.responses import  response_success

@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/health"))
def get_health():
    return response_success({"status": "OK"})