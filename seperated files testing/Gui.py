from tkinter import *


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
