import os
import win10toast

from collections import deque

from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)
toaster=win10toast.ToastNotifier()

channelsCreated = []
usersLogged = []
channelsMessages = dict()

@app.route("/")
@login_required
def index():

    return render_template("index.html", channels=channelsCreated)

@app.route("/signin", methods=['GET','POST'])
def signin():
    ''' Save the username on a Flask session 
    after the user submit the sign in form '''

    
    session.clear()

    username = request.form.get("username")
    
    if request.method == "POST":

        if len(username) < 1 or username is '':
            return render_template("error.html", message="username can't be empty.")

        if username in usersLogged:
            return render_template("error.html", message="that username already exists!")                   
        
        usersLogged.append(username)

        session['username'] = username

        # Remember the user session on a cookie if the browser is closed.
        session.permanent = True

        return redirect("/")
    else:
        return render_template("signin.html")

@app.route("/logout", methods=['GET'])
def logout():
    """ Logout user from list and delete cookie."""

    
    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass

    
    session.clear()

    return redirect("/")

@app.route("/create", methods=['GET','POST'])
def create():
    """ Create a channel and redirect to its page """

    # Get channel name from form
    newChannel = request.form.get("channel")

    if request.method == "POST":

        if newChannel in channelsCreated:
            return render_template("error.html", message="that channel already exists!")
        
        # Add channel to global list of channels
        channelsCreated.append(newChannel)

        channelsMessages[newChannel] = deque()

        return redirect("/channels/" + newChannel)
    
    else:

        return render_template("create.html", channels = channelsCreated)

@app.route("/channel_list", methods=['GET','POST'])
@login_required
def get_channelList():
    return render_template("channel_list.html", channels = channelsCreated)

@app.route("/channels/<channel>", methods=['GET','POST'])
@login_required
def enter_channel(channel):
    """ Show channel page to send and receive messages """

    session['current_channel'] = channel

    if request.method == "POST":
        
        return redirect("/")
    else:
        return render_template("channel.html", channels= channelsCreated, messages=channelsMessages[channel])

@socketio.on("joined", namespace='/')
def joined():
    """ Send message to announce that user has entered the channel """
    
    # Save current channel to join room.
    room = session.get('current_channel')

    join_room(room)
    # toast_msg=session.get('username') + ' has entered the channel '+room
    # toaster.show_toast('Flack',toast_msg,icon_path="/static/images/favicon-16x16.png", duration=10)
    emit('status', {
        'userJoined': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' has entered the channel'}, 
        room=room)

@socketio.on("left", namespace='/')
def left():
    """ Send message to announce that user has left the channel """

    room = session.get('current_channel')

    leave_room(room)
    # toast_msg=session.get('username') + ' has left the channel '+room
    # toaster.show_toast('Flack',toast_msg,icon_path="/static/images/favicon-16x16.png", duration=10)
    emit('status', {
        'msg': session.get('username') + ' has left the channel'}, 
        room=room)

@socketio.on('send message')
def send_msg(msg, timestamp):
    """ Receive message with timestamp and broadcast on the channel """

    # Broadcast only to users on the same channel.
    room = session.get('current_channel')

    # Save 100 messages and display them when a user joins a specific channel.
    if len(channelsMessages[room]) > 100:
        channelsMessages[room].popleft()

    channelsMessages[room].append([timestamp, session.get('username'), msg])
    # toast_msg=session.get('username') + ' says..'+'\n'+msg
    # toaster.show_toast('Flack',toast_msg,icon_path="/static/images/favicon-16x16.png", duration=10)
    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg}, 
        room=room)



if __name__ == '__main__':
    socketio.run(app, debug=True)