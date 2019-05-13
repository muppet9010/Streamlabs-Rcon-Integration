from Logging import Logging
from Obs import Obs
from Gui import Gui, GuiWindow
from Currency import Currency
from ObsEvent import ObsEvent
import json as Json
from Config import Config
from Profiles import Profiles


class State():
    def __init__(self):
        self.Config = Config(self)
        self.Logging = Logging(self)
        self.Currency = Currency(self)
        self.Profiles = Profiles(self)
        self.Obs = Obs(self)
        self.GuiWindow = GuiWindow(self)
        self.Gui = self.GuiWindow.Gui
        self.Gui.CreateWidgets()

    def OnStartButton(self):
        self.Logging.DebugLog("Start Button")
        if not self.Currency.GetRates():
            self.Logging.Log("Error: Get Rates for Currency failed")
            return
        self.Obs.Connect()
        self.UpdateStatus()

    def OnObsConnect(self):
        self.Logging.DebugLog("Streamlabs Connected")
        self.Obs.disconnecting = False
        if self.Obs.connecting:
            self._OnStartButtonPostObsConnection()

    def _OnStartButtonPostObsConnection(self):
        self.Obs.connecting = False
        self.UpdateStatus()
        self.RecordActivity("Started")

    def OnStopButton(self):
        self.Logging.DebugLog("Stop Button")
        self.Obs.Disconnect()
        self.RecordActivity("Stopped")

    def OnObsDisconnect(self):
        self.Logging.DebugLog("Streamlabs Disconnected")
        if not self.Obs.disconnecting:
            self.RecordActivity("Error Streamlabs Stopped Unexpectedly")
        self.Obs.disconnecting = False
        self.UpdateStatus()

    def OnQuitButton(self):
        self.Logging.Log("Quit Button")
        self.Obs.Disconnect()
        self.Gui.master.destroy()

    def RecordActivity(self, text):
        self.Logging.Log(text)
        self.Gui.AddToActivityLog(text)

    def OnObsEvent(self, data):
        self.Logging.DebugLog("Streamlabs raw event received: " + str(data))
        event = ObsEvent(self, data)
        self.Logging.DebugLog(
            "Streamlabs processed event: " + str(event))
        if event.errored:
            return
        event.Process()

    def UpdateStatus(self):
        if self.Obs.connecting:
            self.Gui.UpdateStatusText("OBS Connecting")
        elif self.Obs.sio.eio.state == "connected":
            self.Gui.UpdateStatusText("Running")
        else:
            self.Gui.UpdateStatusText("Stopped")

    def Run(self):
        self.Logging.DebugLog("App Started")
        self.Gui.mainloop()


State = State()
State.Run()
