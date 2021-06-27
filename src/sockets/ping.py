from flask_socketio import emit
from config.app import socketio
from src.sockets.common import CommonSocketConnection
from src.utils.responses import response_success

namespace = '/ping'


class PingSocketLogic(CommonSocketConnection):

    def on_connect(self):
        emit('user_connect', {'data': 'Connected'}, namespace=namespace)

    def on_pong(self, data):
        # emit('my_response', data)
        emit('pong', response_success(data, True), namespace=namespace)
        # return response_success(data)


logic = PingSocketLogic()


@socketio.on('connect', namespace=namespace)
def on_connect():
    logic.on_connect()


@socketio.on_error(namespace)  # Handles the default namespace
def error_handler(e):
    logic.on_error(e)


@socketio.on('pong', namespace=namespace)
def on_pong(data):
    logic.on_pong(data)
