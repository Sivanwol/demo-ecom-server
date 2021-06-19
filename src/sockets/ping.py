from flask_socketio import emit

from config.api import socketio
from src.sockets.common import CommonSocketConnection


class PingSocket(CommonSocketConnection):
    def ping(self, data):
        emit('my_response', data)


socketio.on_namespace(PingSocket('/ping'))
