import socketio


sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connected to server')


@sio.on('disconnect')
def on_disconnect():
    print('disconnected to server')


@sio.on('event')
def on_event(data):
    print(data)


def connect():
    sio.connect('https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls')


def disconnect():
    sio.disconnect()
