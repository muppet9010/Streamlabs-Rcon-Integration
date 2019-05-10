import tkinter as tk


def Create(obs):
    root = tk.Tk()
    root.minsize(500, 400)
    app = Application(obs, master=root)
    return app


class Application(tk.Frame):
    def __init__(self, obs, master=None):
        super().__init__(master)
        self.master = master
        self.obs = obs
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.CreateStreamlabs(self.master)
        self.CreateActivityLog(self.master)
        self.CreateBottomBar(self.master)

    def CreateStreamlabs(self, parent):
        self.streamlabsContainer = tk.Frame(parent)
        self.streamlabsContainer.pack(fill="x", side="top")

        self.UpdateStreamlabsStatus(False)
        streamlabsStatusLabel = tk.Label(
            self.streamlabsContainer, textvariable=self.streamlabsStatusText, height=1)
        streamlabsStatusLabel.pack(side="left")

        streamlabsConnectButton = tk.Button(self.streamlabsContainer)
        streamlabsConnectButton["text"] = "Connect Streamlabs"
        streamlabsConnectButton["command"] = self.obs.Connect
        streamlabsConnectButton.pack(side="left")

        streamlabsDisconnectButton = tk.Button(self.streamlabsContainer)
        streamlabsDisconnectButton["text"] = "Disonnect Streamlabs"
        streamlabsDisconnectButton["command"] = self.obs.Disconnect
        streamlabsDisconnectButton.pack(side="left")

    def CreateActivityLog(self, parent):
        self.activityLog = tk.Label(parent, height=5)
        self.activityLog.pack(fill="both", expand=True, side="top")

    def CreateBottomBar(self, parent):
        self.bottomBarContainer = tk.Frame(parent)
        self.bottomBarContainer.pack(fill="x", side="top")

        quitButton = tk.Button(self.bottomBarContainer, text="QUIT", fg="red",
                               command=self.Quit)
        quitButton.pack(side="left")

    def Quit(self):
        self.master.destroy()

    def UpdateStreamlabsStatus(self, connected):
        if connected:
            self.streamlabsStatusText = "Streamlabs: Connected"
        else:
            self.streamlabsStatusText = "Streamlabs: Disconnected"
