import os

from flask import Flask, render_template
from flask_socketio import SocketIO, send

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=BASE_DIR)
app.config['SECRET_KEY'] = 'secret!'


# socketio = SocketIO(app)
socketio = SocketIO()
socketio.init_app(app)

ns = '/chat'

@socketio.on('connect', namespace = ns)
def handle_connect():
    print('==connect==')
    pass
@socketio.on('message', namespace = ns)
def handle_message(msg):
    print('==message==')
    # send(msg, namespace = ns, broadcast=True)
    socketio.emit(msg, namespace = ns, broadcast=True)
@socketio.on('disconnect', namespace=ns)
def handle_disconnect():
    print('==disconnect==')
    pass


@app.route('/index')
def index():
    return render_template('chat.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

