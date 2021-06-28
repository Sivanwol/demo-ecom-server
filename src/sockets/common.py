from flask import request

from config.app import socketio
from src.services.user import UserService


class CommonSocketConnection():
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_error(self, e):
        pass


class CommonAuthSocketConnection():
    def on_connect(self, auth, userService: UserService):
        res = userService.check_user_auth_socket(auth, True)
        if res is None:
            raise ConnectionRefusedError('unauthorized!')


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)
