import socketio
from tkinter import *


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


class GuiWindow():
    def __init__(self):
        root = Tk()
        root.minsize(500, 400)
        self.app = Gui(master=root)


class Gui(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.CreateStreamlabs(self.master)
        self.CreateActivityLog(self.master)
        self.CreateBottomBar(self.master)

    def CreateStreamlabs(self, parent):
        self.streamlabsContainer = Frame(parent)
        self.streamlabsContainer.pack(fill="x", side="top")

        self.streamlabsStatusText = StringVar()
        self.UpdateStreamlabsStatus(False)
        streamlabsStatusLabel = Label(
            self.streamlabsContainer, textvariable=self.streamlabsStatusText, height=1, width=30)
        streamlabsStatusLabel.pack(side="left")

        streamlabsConnectButton = Button(self.streamlabsContainer)
        streamlabsConnectButton["text"] = "Connect Streamlabs"
        streamlabsConnectButton["command"] = obs.Connect
        streamlabsConnectButton.pack(side="left")

        streamlabsDisconnectButton = Button(self.streamlabsContainer)
        streamlabsDisconnectButton["text"] = "Disonnect Streamlabs"
        streamlabsDisconnectButton["command"] = obs.Disconnect
        streamlabsDisconnectButton.pack(side="left")

    def CreateActivityLog(self, parent):
        self.activityLog = Label(parent, height=5)
        self.activityLog.pack(fill="both", expand=True, side="top")

    def CreateBottomBar(self, parent):
        self.bottomBarContainer = Frame(parent)
        self.bottomBarContainer.pack(fill="x", side="top")

        quitButton = Button(self.bottomBarContainer, text="QUIT", fg="red",
                            command=self.Quit)
        quitButton.pack(side="left")

    def Quit(self):
        self.master.destroy()

    def UpdateStreamlabsStatus(self, connected):
        if connected:
            self.streamlabsStatusText.set("Streamlabs: Connected")
        else:
            self.streamlabsStatusText.set("Streamlabs: Disconnected")


obs = OBS()
app = GuiWindow().app
app.mainloop()
