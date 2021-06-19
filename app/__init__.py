from config.api import app, socketio

if __name__ == '__main__':
    app.run()
    if socketio is not None:
        socketio.run(app)
