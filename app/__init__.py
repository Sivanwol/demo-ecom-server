from config.app import redis_url, app, socketio

if __name__ == '__main__':
    if socketio is not None:
        socketio.run(app, async_mode="eventlet", cors_allowed_origins="*", message_queue=redis_url)
    app.run()
