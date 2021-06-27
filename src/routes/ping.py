from config.app import app as current_app
from src.utils.responses import  response_success

@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/ping/health"))
def get_health():
    return response_success({"status": "OK"})