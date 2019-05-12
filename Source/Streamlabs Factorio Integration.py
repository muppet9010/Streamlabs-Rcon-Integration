from Logging import Logging
from Obs import Obs
from Gui import Gui, GuiWindow
from Currency import Currency
from ObsEvent import ObsEvent
import json as Json


class State():
    def Start(self):
        self.Logging.DebugLog("Start Button")
        if not self.Currency.GetRates():
            self.Logging.Log("Error: Get Rates for Currency failed")
            return
        self.Obs.Connect()
        self.UpdateStatus()

    def Quit(self):
        self.Logging.Log("Quit Button")
        self.Obs.Disconnect()
        self.Gui.master.destroy()

    def RecordActivity(self, text):
        self.Logging.Log(text)
        self.Gui.AddToActivityLog(text)

    def StartPostObsConnection(self):
        self.Obs.connecting = False
        self.UpdateStatus()
        self.RecordActivity("Started")

    def Stop(self):
        self.Logging.DebugLog("Stop Button")
        self.Obs.Disconnect()
        self.RecordActivity("Stopped")

    def ObsConnectHandler(self):
        self.Logging.DebugLog("Streamlabs Connected")
        self.Obs.disconnecting = False
        if self.Obs.connecting:
            self.StartPostObsConnection()

    def ObsDisconnectHandler(self):
        self.Logging.DebugLog("Streamlabs Disconnected")
        if not self.Obs.disconnecting:
            self.RecordActivity("Error Streamlabs Stopped Unexpectedly")
        self.Obs.disconnecting = False
        self.UpdateStatus()

    def ObsEventHandler(self, data):
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


State = State()
State.Logging = Logging(True)
State.Currency = Currency(State)
State.Obs = Obs(State)
State.GuiWindow = GuiWindow(State)
State.Gui = State.GuiWindow.Gui
State.Gui.CreateWidgets()
State.Logging.DebugLog("App Started")
State.Gui.mainloop()
