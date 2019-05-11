import socketio as SocketIo
from ObsEvent import ObsEvent


class Obs():
    disconnecting = False
    connecting = False

    def __init__(self, logging):
        self.logging = logging
        self.sio = SocketIo.Client()
        self.sio.on("event", self.EventHandler)
        self.sio.on("connect", self.ConnectHandler)
        self.sio.on("disconnect", self.DisconnectHandler)

    def UpdateGuiReference(self, gui):
        self.gui = gui

    def ConnectHandler(self):
        self.logging.DebugLog("Streamlabs Connected")
        self.disconnecting = False
        if self.connecting:
            self.gui.StartPostObsConnection()

    def DisconnectHandler(self):
        self.logging.DebugLog("Streamlabs Disconnected")
        if not self.disconnecting:
            self.gui.AddToActivityLog("Error Streamlabs Stopped Unexpectedly")
        self.disconnecting = False
        self.gui.UpdateStatus()

    def EventHandler(self, msg):
        print("Received message: ", msg)
        ObsEvent(msg, self.gui, self.currency)

    def Connect(self, currency):
        self.currency = currency
        if self.sio.eio.state != "disconnected":
            return
        self.logging.DebugLog("Streamlabs Connecting")
        self.disconnecting = False
        self.connecting = True
        self.sio.connect("https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls")

    def Disconnect(self):
        if self.sio.eio.state != "connected":
            return
        self.logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
        self.sio.disconnect()
