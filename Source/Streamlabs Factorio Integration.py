import socketio as SocketIo
import tkinter as TK
import datetime as Datetime
import requests as Requests
import json as Json
import os as Os
from Logging import Logging


class Obs():
    disconnecting = False
    connecting = False

    def __init__(self):
        self.sio = SocketIo.Client()
        self.sio.on("event", self.EventHandler)
        self.sio.on("connect", self.ConnectHandler)
        self.sio.on("disconnect", self.DisconnectHandler)

    def ConnectHandler(self):
        Logging.DebugLog("Streamlabs Connected")
        self.disconnecting = False
        if self.connecting:
            Gui.StartPostObsConnection()

    def DisconnectHandler(self):
        Logging.DebugLog("Streamlabs Disconnected")
        if not self.disconnecting:
            Gui.AddToActivityLog("Error Streamlabs Stopped Unexpectedly")
        self.disconnecting = False
        Gui.UpdateStatus()

    def EventHandler(self, msg):
        print("Received message: ", msg)
        ObsEvent(msg)

    def Connect(self):
        if Obs.sio.eio.state != "disconnected":
            return
        Logging.DebugLog("Streamlabs Connecting")
        self.disconnecting = False
        self.connecting = True
        self.sio.connect("https://sockets.streamlabs.com?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkJFMzU5QjZFNTEzRjczOTk1NDlCIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiODk1NjMzNDMifQ.K4F-AFIqFkJPFXrcfSO9_aX8g449BNhRGSngHL40dls")

    def Disconnect(self):
        if Obs.sio.eio.state != "connected":
            return
        Logging.DebugLog("Streamlabs Disconnecting")
        self.disconnecting = True
        self.connecting = False
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
            Gui.AddToActivityLog("wrong number of payloads in event: " +
                                 len(data["message"]) + " data: " + str(data))
            return False
        message = data["message"][0]
        if (self.platform == "streamlabs" and self.type == "donation") or (self.platform == "youtube_account" and self.type == "superchat"):
            self.valueType = "money"
            self.value = Currency.GetNormalisedValue(
                message.currency, message.amount)
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
            Gui.AddToActivityLog("Event not recognised: " + str(data))
            return False
        else:
            return True


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
        self.statusContainer = TK.Frame(parent)
        self.statusContainer.pack(fill=TK.X, side=TK.TOP)

        self.statusText = TK.StringVar()
        self.UpdateStatus()
        statusLabel = TK.Label(
            self.statusContainer, textvariable=self.statusText, height=1, width=30)
        statusLabel.pack(side=TK.LEFT)

        startButton = TK.Button(self.statusContainer)
        startButton["text"] = "Start"
        startButton["command"] = self.Start
        startButton.pack(side=TK.LEFT)

        stopButton = TK.Button(self.statusContainer)
        stopButton["text"] = "Stop"
        stopButton["command"] = self.Stop
        stopButton.pack(side=TK.LEFT)

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
        Logging.Log("Quit Button")
        Obs.Disconnect()
        self.master.destroy()

    def UpdateStatus(self):
        if Obs.connecting:
            self.statusText.set("OBS Connecting")
        elif Obs.sio.eio.state == "connected":
            self.statusText.set("Running")
        else:
            self.statusText.set("Stopped")

    def AddToActivityLog(self, text):
        Logging.Log(text)
        self.activityLogText.configure(state="normal")
        self.activityLogText.insert(1.0, Logging.TimestampText(text) + "\n")
        self.activityLogText.configure(state="disabled")

    def Start(self):
        Logging.DebugLog("Start Button")
        if not Currency.GetRates():
            Logging.Log("Error: Get Rates for Currency failed")
            return
        Obs.Connect()
        Gui.UpdateStatus()

    def StartPostObsConnection(self):
        Obs.connecting = False
        Gui.UpdateStatus()
        Gui.AddToActivityLog("Started")

    def Stop(self):
        Logging.DebugLog("Stop Button")
        Obs.Disconnect()
        Gui.AddToActivityLog("Stopped")


class Currency():
    rates = {}
    cacheFileName = "CurrencyDataCache.json"

    def GetRates(self):
        if len(self.rates) > 0:
            return True
        if Os.path.isfile("./" + self.cacheFileName):
            Logging.DebugLog("Trying to get currancy rates from cache file")
            with open(self.cacheFileName, "r") as file:
                data = Json.load(file)
            file.closed
            cacheDateTime = Datetime.date.fromtimestamp(data["timestamp"])
            currentDateTime = Datetime.date.fromtimestamp(
                Datetime.datetime.utcnow().timestamp())
            if currentDateTime <= cacheDateTime:
                for name, rate in data["quotes"].items():
                    currency = name[3:]
                    self.rates[currency] = rate
                if len(self.rates) > 0:
                    Logging.DebugLog("Got currency rates from cache file")
                    return True

        self._SourceRateData()
        if len(self.rates) > 0:
            Logging.DebugLog("Got currency rates from website")
            return True
        else:
            Logging.DebugLog(
                "Failed to get any currency rates from website")
            return False

    def _SourceRateData(self):
        Logging.DebugLog("Sourcing currency rates from website")
        url = "http://www.apilayer.net/api/live"
        params = {"access_key": "bf92c65503f807f9abd65b83d39c2c6c"}
        request = Requests.get(url=url, params=params)
        response = request.json()
        if not response["success"]:
            Gui.AddToActivityLog("ERROR: Can't get currency conversion data")
            return False
        with open(self.cacheFileName, "w") as file:
            file.write(Json.dumps(response))
        file.closed
        for name, rate in response["quotes"].items():
            currency = name[3:]
            self.rates[currency] = rate

    def GetNormalisedValue(self, currency, amount):
        return amount / self.rates[currency]


Obs = Obs()
Currency = Currency()
Gui = GuiWindow().gui
Logging.DebugLog("App Started")
Gui.mainloop()
