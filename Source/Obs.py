import socketio as SocketIo
from ObsEvent import ObsEvent


class Obs():
    disconnecting = False
    connecting = False

    def __init__(self, state):
        self.State = state
        self.sio = SocketIo.Client()
        self.sio.on("event", self.EventHandler)
        self.sio.on("connect", self.ConnectHandler)
        self.sio.on("disconnect", self.DisconnectHandler)

    def UpdateReferences(self):
        self.Gui = self.State.Gui

    def ConnectHandler(self):
        self.State.Logging.DebugLog("Streamlabs Connected")
        self.disconnecting = False
        if self.connecting:
            self.Gui.StartPostObsConnection()

    def DisconnectHandler(self):
        self.State.Logging.DebugLog("Streamlabs Disconnected")
        if not self.disconnecting:
            self.Gui.AddToActivityLog("Error Streamlabs Stopped Unexpectedly")
        self.disconnecting = False
        self.Gui.UpdateStatus()

    def EventHandler(self, msg):
        print("Received message: ", msg)
        ObsEvent(msg, self.State)

    def Connect(self):
        if self.sio.eio.state != "disconnected":
            return
        self.State.Logging.DebugLog("Streamlabs Connecting")
        self.disconnecting = False
        self.connecting = True
        self.sio.connect("https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjI3OEFBMDk5NEJFNkE0QTkyQzgzIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.WetcleHOyyhBMv16q04y3mi2XXiBDMzML8JM3kHvbfk")

    def Disconnect(self):
        if self.sio.eio.state != "connected":
            return
        self.State.Logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
        self.sio.disconnect()
