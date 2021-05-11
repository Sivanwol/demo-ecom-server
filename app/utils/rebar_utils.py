import os

from flask_rebar import Rebar

from app import main
from app.utils.singleton import singleton


@singleton
class RebarUtils:
    def __init__(self):
        rebar = Rebar()
        self.registry = rebar.create_handler_registry(prefix=main.settings[os.environ.get("FLASK_ENV", "development")].API_PERFIX)

    def setup(self, config):
        rebar = Rebar()
        self.registry = rebar.create_handler_registry(prefix=config.API_PERFIX)
