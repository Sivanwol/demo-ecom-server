from flask import request
from socketio import Namespace

from config.api import socketio
from src.routes import userService


class CommonSocketConnection(Namespace):
    def on_connect(self, auth):
        pass

    def on_disconnect(self):
        pass

    def on_error(self, e):
        pass


class CommonAuthSocketConnection(CommonSocketConnection):
    def on_connect(self, auth):
        res = userService.check_user_auth_socket(auth, True)
        if res is None:
            raise ConnectionRefusedError('unauthorized!')


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)
