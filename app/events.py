from flask import request
from flask_socketio import emit

from .extensions import socketio
users ={}

@socketio.on("connect")
def handleConnect():
    print('Client connect')
    
@socketio.on("user_join")
def handle_user_join(username):
    print(f'user {username} joined')
    users[username] = request.sid

@socketio.on("message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message":message, "username":username}, broadcast=False)

def emitir_uid(uid):
    socketio.emit("uid_update",{'uid':uid})
    