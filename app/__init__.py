from config.api import  redis_url
from config.containers import app, socketio
if __name__ == '__main__':
    if socketio is not None:
        socketio.run(app, async_mode="eventlet", cors_allowed_origins="*", message_queue=redis_url)
    app.run()
