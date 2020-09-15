import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")#'00f57468910ca98811868fdf0d7e26ac'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('home.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@app.route('/example')
def example():
    return render_template('example.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)