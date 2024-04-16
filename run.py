from app import createApp, socketio
app = createApp()
socketio.run(app, port=5432, host='0.0.0.0')
#app.run(port=5432)