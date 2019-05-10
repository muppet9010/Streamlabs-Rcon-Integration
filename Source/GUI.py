import tkinter as tk


class Application(tk.Frame):
    def __init__(self, obs, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets(obs)

    def create_widgets(self, obs):
        self.streamlabsConnectButton = tk.Button(self)
        self.streamlabsConnectButton["text"] = "Connect Streamlabs"
        self.streamlabsConnectButton["command"] = obs.connect
        self.streamlabsConnectButton.pack(side="top")

        self.streamlabsDisconnectButton = tk.Button(self)
        self.streamlabsDisconnectButton["text"] = "Disonnect Streamlabs"
        self.streamlabsDisconnectButton["command"] = obs.disconnect
        self.streamlabsDisconnectButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
