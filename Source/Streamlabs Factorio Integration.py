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

    def Setup(self):
        self.Currency = Currency(self)
        self.Profiles = Profiles(self)
        self.Obs = Obs(self)
        self.GuiWindow = GuiWindow(self)
        self.Gui = self.GuiWindow.Gui
        self.Gui.CreateWidgets()

    def OnStartButtonHandler(self):
        try:
            self.Logging.DebugLog("Start Button")
            if not self.Currency.GetRates():
                self.Logging.Log("Error: Get Rates for Currency failed")
                return
            self.Obs.Connect()
            self.UpdateStatus()
        except Exception as ex:
            self.Logging.RecordException(ex, "Start Button Critical Error")

    def OnObsConnectHandler(self):
        try:
            self.Logging.DebugLog("Streamlabs Connected")
            self.Obs.disconnecting = False
            if self.Obs.connecting:
                self._OnStartButtonPostObsConnection()
        except Exception as ex:
            self.Logging.RecordException(ex, "OBS Connected Critical Error")

    def _OnStartButtonPostObsConnection(self):
        self.Obs.connecting = False
        self.UpdateStatus()
        self.RecordActivity("Started")

    def OnStopButtonHandler(self):
        try:
            self.Logging.DebugLog("Stop Button")
            self.Obs.Disconnect()
            self.RecordActivity("Stopped")
        except Exception as ex:
            self.Logging.RecordException(ex, "Stop Button Critical Error")

    def OnObsDisconnectHandler(self):
        try:
            self.Logging.DebugLog("Streamlabs Disconnected")
            if not self.Obs.disconnecting:
                self.RecordActivity("Error Streamlabs Stopped Unexpectedly")
            self.Obs.disconnecting = False
            self.UpdateStatus()
        except Exception as ex:
            self.Logging.RecordException(ex, "OBS Disconnected Critical Error")

    def OnQuitButtonHandler(self):
        try:
            self.Logging.Log("Quit Button")
            self.Obs.Disconnect()
            self.Gui.master.destroy()
        except Exception as ex:
            self.Logging.RecordException(ex, "Quit Button Critical Error")

    def RecordActivity(self, text):
        self.Logging.Log(text)
        self.Gui.AddToActivityLog(text)

    def OnObsEventHandler(self, data):
        try:
            self.Logging.DebugLog(
                "Streamlabs raw event received: " + str(data))
            event = ObsEvent(self, data)
            self.Logging.DebugLog(
                "Streamlabs processed event: " + str(event))
            if event.errored:
                return
            event.Process()
        except Exception as ex:
            self.Logging.RecordException(
                ex, "OBS Event Handler Critical Error - This event won't be processed")

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


try:
    state = State()
    state.Setup()
    state.Run()
except Exception as ex:
    try:
        self.Obs.Disconnect()
    except:
        pass
    try:
        state.Logging.RecordException(
            ex, "Application Critical Error - Application has been stopped")
    except:
        pass
    raise ex
