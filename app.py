from flask import Flask
from websocket.socketio import socketio
from repository.database import db
from route.payment_pix_route import payment_pix_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/pix-python'
app.register_blueprint(payment_pix_bp)

db.init_app(app)
socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)