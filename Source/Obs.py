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
        self.sio.connect("https://sockets.streamlabs.com?token=" +
                         self.State.Config.GetSetting("Obs SocketApiToken"))

    def Disconnect(self):
        if self.sio.eio.state != "connected":
            return
        self.Logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
        self.sio.disconnect()
