import socketio as SocketIo


class Obs():

    def __init__(self, state):
        self.State = state
        self.Logging = state.Logging
        self.disconnecting = False
        self.connecting = False
        self.sio = SocketIo.Client()
        self.sio.on("event", self.State.OnObsEvent)
        self.sio.on("connect", self.State.OnObsConnect)
        self.sio.on("disconnect", self.State.OnObsDisconnect)

    def Connect(self):
        if self.sio.eio.state != "disconnected":
            return
        self.Logging.DebugLog("Streamlabs Connecting")
        self.disconnecting = False
        self.connecting = True
        self.sio.connect("https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjI3OEFBMDk5NEJFNkE0QTkyQzgzIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.WetcleHOyyhBMv16q04y3mi2XXiBDMzML8JM3kHvbfk")  # TODO move to config file

    def Disconnect(self):
        if self.sio.eio.state != "connected":
            return
        self.Logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
        self.sio.disconnect()
