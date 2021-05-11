import os

from flask_restful import Api

from app import main
from app.controllers.user import UserList
from app.main.errors import errors

# Flask API Configuration
api = Api(
    catch_all_404s=True,
    errors=errors,
    prefix=main.settings[os.environ.get("FLASK_ENV", "development")].API_PERFIX
)

api.add_resource(UserList, '/users')

