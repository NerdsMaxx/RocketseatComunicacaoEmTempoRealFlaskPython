from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    print("Client connected to the server")

@socketio.on('disconnect')
def handle_connect():
    print("Client has disconnected to the server")