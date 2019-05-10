import socketio


class OBS():
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.on('event', self.event_handler)
        self.sio.on('connect', self.connect_handler)
        self.sio.on('disconnect', self.disconnect_handler)

    def connect_handler(self):
        print('Connected')
        app.UpdateStreamlabsStatus(True)

    def disconnect_handler(self):
        print('Disconnected')
        app.UpdateStreamlabsStatus(False)

    def event_handler(self, msg):
        print('Received message: ', msg)

    def Connect(self):
        self.sio.connect('https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls')

    def Disconnect(self):
        self.sio.disconnect()
