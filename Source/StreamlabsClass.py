import socketio


class Streamlabs:
    sio = socketio.Client()

    @sio.on('connect')
    def on_connect(self):
        print('connected to server')

    @sio.on('disconnect')
    def on_disconnect(self):
        print('disconnected to server')

    @sio.on('event')
    def on_event(self, data):
        print(data)

    def connect(self):
        self.sio.connect('https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls')

    def disconnect(self):
        self.sio.disconnect()
