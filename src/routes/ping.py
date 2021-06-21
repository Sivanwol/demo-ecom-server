import os
from config import settings
from config.containers import app as current_app
from src.utils.responses import  response_success

@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/ping/health"))
def get_health():
    return response_success({"status": "OK"})