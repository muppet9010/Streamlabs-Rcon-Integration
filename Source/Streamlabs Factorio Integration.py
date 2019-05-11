import socketio
import tkinter as TK
import datetime


class Obs():
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.on('event', self.EventHandler)
        self.sio.on('connect', self.ConnectHandler)
        self.sio.on('disconnect', self.DisconnectHandler)

    def ConnectHandler(self):
        print('Connected')
        gui.UpdateStreamlabsStatus()
        gui.AddToActivityLog("Streamlabs Connected")

    def DisconnectHandler(self):
        print('Disconnected')
        gui.UpdateStreamlabsStatus()
        gui.AddToActivityLog("Streamlabs Disconnected")

    def EventHandler(self, msg):
        print('Received message: ', msg)
        ObsEvent(msg)

    def Connect(self):
        if obs.sio.eio.state != "disconnected":
            return
        gui.AddToActivityLog("Connecting")
        self.sio.connect('https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls')

    def Disconnect(self):
        self.sio.disconnect()


class ObsEvent():
    def __init__(self, data):
        self.id = data["event_id"]
        self.platform = data["for"]
        self.type = data["type"]
        if not self.GetNormalisedData(data):
            return

    def GetNormalisedData(self, data):
        if len(data["message"]) != 1:
            gui.AddToActivityLog("wrong number of payloads in event: " +
                                 len(data["message"]) + " data: " + str(data))
            return False
        message = data["message"][0]
        if (self.platform == "streamlabs" and self.type == "donation") or (self.platform == "youtube_account" and self.type == "superchat"):
            self.valueType = "money"
            self.value = self.GetNormalisedValue(message)
        elif (self.platform == "twitch_account" and self.type == "bits"):
            self.valueType = "money"
            self.value = message["amount"] / 100
        elif (self.platform == "twitch_account" and self.type == "subscription"):
            self.valueType = "money"
            subPlan = message["sub_plan"]
            if subPlan == "Prime" or subPlan == "1000":
                self.value = 5
            elif subPlan == "2000":
                self.value = 10
            elif subPlan == "3000":
                self.value = 25
        elif (self.platform == "youtube_account" and self.type == "subscription"):
            self.valueType = "money"
            self.value = 5
        elif (self.platform == "mixer_account" and self.type == "subscription"):
            self.valueType = "money"
            self.value = 8
        elif (self.type == "follow"):
            self.valueType = "follow"
            self.value = 1
        elif (self.type == "host"):
            self.valueType = "viewer"
            self.value = message["viewers"]

        if self.value == None or self.valueType == None:
            gui.AddToActivityLog("Event not recognised: " + str(data))
            return False
        else:
            return True

    def GetNormalisedValue(self, message):
        if message["currency"] == "USD":
            return message["amount"]
        return 1  # TODO use a web service to convert from other currencies to USD


class GuiWindow():
    def __init__(self):
        root = TK.Tk()
        root.minsize(500, 400)
        self.gui = Gui(master=root)


class Gui(TK.Frame):
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
        self.streamlabsContainer = TK.Frame(parent)
        self.streamlabsContainer.pack(fill=TK.X, side=TK.TOP)

        self.streamlabsStatusText = TK.StringVar()
        self.UpdateStreamlabsStatus()
        streamlabsStatusLabel = TK.Label(
            self.streamlabsContainer, textvariable=self.streamlabsStatusText, height=1, width=30)
        streamlabsStatusLabel.pack(side=TK.LEFT)

        streamlabsConnectButton = TK.Button(self.streamlabsContainer)
        streamlabsConnectButton["text"] = "Connect Streamlabs"
        streamlabsConnectButton["command"] = obs.Connect
        streamlabsConnectButton.pack(side=TK.LEFT)

        streamlabsDisconnectButton = TK.Button(self.streamlabsContainer)
        streamlabsDisconnectButton["text"] = "Disonnect Streamlabs"
        streamlabsDisconnectButton["command"] = obs.Disconnect
        streamlabsDisconnectButton.pack(side=TK.LEFT)

    def CreateActivityLog(self, parent):
        titleFrame = TK.LabelFrame(parent, text="Activity Log")
        titleFrame.pack(fill=TK.BOTH, expand=True, side=TK.TOP, padx=3, pady=3)
        yScroll = TK.Scrollbar(titleFrame, orient=TK.VERTICAL)
        yScroll.pack(fill=TK.Y, expand=True, side=TK.RIGHT)
        self.activityLogText = TK.Text(
            titleFrame, height=5, wrap=TK.WORD, yscrollcommand=yScroll.set, state=TK.DISABLED)
        self.activityLogText.pack(fill=TK.BOTH, expand=True, side=TK.LEFT)

    def CreateBottomBar(self, parent):
        self.bottomBarContainer = TK.Frame(parent)
        self.bottomBarContainer.pack(fill=TK.X, side=TK.TOP)

        quitButton = TK.Button(self.bottomBarContainer, text="QUIT", fg="red",
                               command=self.Quit)
        quitButton.pack(side=TK.LEFT)

    def Quit(self):
        obs.Disconnect()
        logging.Log("Quit")
        self.master.destroy()

    def UpdateStreamlabsStatus(self):
        if obs.sio.eio.state == "connected":
            self.streamlabsStatusText.set("Streamlabs: Connected")
        else:
            self.streamlabsStatusText.set("Streamlabs: Disconnected")

    def AddToActivityLog(self, text):
        currentDT = datetime.datetime.now()
        dtString = currentDT.strftime("%H:%M:%S")
        activityLine = dtString + " : " + text
        logging.Log(activityLine)
        self.activityLogText.configure(state="normal")
        self.activityLogText.insert(1.0, activityLine + "\n")
        self.activityLogText.configure(state="disabled")


class Logging():
    def __init__(self):
        currentDT = datetime.datetime.now()
        dtString = currentDT.strftime("%Y_%m_%d %H_%M_%S")
        self.logFileName = "Log " + dtString + ".log"

    def Log(self, text):
        fileName = self.logFileName
        file = open(fileName, "a")
        file.write(text + "\n")
        file.close


logging = Logging()
obs = Obs()
gui = GuiWindow().gui
gui.mainloop()
