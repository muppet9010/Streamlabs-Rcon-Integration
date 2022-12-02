import socketio as SocketIo


class Streamlabs():

    def __init__(self, state):
        self.state = state
        self.logging = state.logging
        self.disconnecting = False
        self.connecting = False
        self.sio = SocketIo.Client()
        self.sio.on("event", self.state.OnStreamlabsEventHandler)
        self.sio.on("connect", self.state.OnStreamlabsConnectHandler)
        self.sio.on("disconnect", self.state.OnStreamlabsDisconnectHandler)

    def Connect(self):
        if self.sio.eio.state != "disconnected":
            return
        self.logging.DebugLog("Streamlabs Connecting")
        self.disconnecting = False
        self.connecting = True
        self.sio.connect("https://sockets.streamlabs.com?token=" + self.state.config.GetSetting("Streamlabs SocketApiToken"))

    def Disconnect(self):
        if self.sio.eio.state != "connected":
            return
        self.logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
        self.sio.disconnect()
