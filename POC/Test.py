import tkinter as tk
import socketio


sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('connected to server')


@sio.on('event')
def on_event(data):
    print(data)


def connect():
    sio.connect('https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls')


def disconnect():
    sio.disconnect()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.streamlabsConnectButton = tk.Button(self)
        self.streamlabsConnectButton["text"] = "Connect Streamlabs"
        self.streamlabsConnectButton["command"] = connect
        self.streamlabsConnectButton.pack(side="top")

        self.streamlabsDisconnectButton = tk.Button(self)
        self.streamlabsDisconnectButton["text"] = "Disonnect Streamlabs"
        self.streamlabsDisconnectButton["command"] = disconnect
        self.streamlabsDisconnectButton.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
