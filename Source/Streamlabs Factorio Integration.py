from Logging import Logging
from Streamlabs import Streamlabs
from Gui import Gui, GuiWindow
from Currency import Currency
from StreamlabsEvent import StreamlabsEvent
import json as Json
from Config import Config
from Profiles import Profiles
from Translations import Translations


class State():
    def __init__(self):
        self.Config = Config(self)
        self.Logging = Logging(self)

    def Setup(self):
        self.Translations = Translations(self)
        self.Currency = Currency(self)
        self.Profiles = Profiles(self)
        self.Streamlabs = Streamlabs(self)
        self.GuiWindow = GuiWindow(self)
        self.Gui = self.GuiWindow.Gui
        self.Gui.CreateWidgets()

    def OnStartButtonHandler(self):
        try:
            self.Logging.DebugLog("Start Button Pressed")
            if self.Gui.selectedProfileName.get() == self.Translations.currentTexts["Gui SelectProfile"]:
                self.RecordActivity(
                    self.Translations.currentTexts["Message NeedProfileBeforeStart"])
                return
            if not self.Currency.GetRates():
                self.Logging.Log("Error: Get Rates for Currency failed")
                return
            self.Streamlabs.Connect()
            self.UpdateStatus()
        except Exception as ex:
            self.Logging.RecordException(ex, "Start Button Critical Error")

    def OnStreamlabsConnectHandler(self):
        try:
            self.Logging.DebugLog("Streamlabs Connected")
            self.Streamlabs.disconnecting = False
            if self.Streamlabs.connecting:
                self._OnStartButtonPostStreamlabsConnection()
        except Exception as ex:
            self.Logging.RecordException(ex, "OBS Connected Critical Error")

    def _OnStartButtonPostStreamlabsConnection(self):
        self.Streamlabs.connecting = False
        self.UpdateStatus()
        self.RecordActivity(self.Translations.currentTexts["Message Started"])

    def OnStopButtonHandler(self):
        try:
            self.Logging.DebugLog("Stop Button Pressed")
            self.Streamlabs.Disconnect()
        except Exception as ex:
            self.Logging.RecordException(ex, "Stop Button Critical Error")

    def OnStreamlabsDisconnectHandler(self):
        try:
            self.Logging.DebugLog("Streamlabs Disconnected Pressed")
            if not self.Streamlabs.disconnecting:
                self.RecordActivity(
                    self.Translations.currentTexts["Message StreamlabsUnexpectedStop"])
            else:
                self.RecordActivity(
                    self.Translations.currentTexts["Message Stopped"])
            self.Streamlabs.disconnecting = False
            self.UpdateStatus()
        except Exception as ex:
            self.Logging.RecordException(ex, "OBS Disconnected Critical Error")

    def OnQuitButtonHandler(self):
        try:
            self.Logging.Log("Quit Button")
            self.Streamlabs.Disconnect()
            self.Gui.master.destroy()
        except Exception as ex:
            self.Logging.RecordException(ex, "Quit Button Critical Error")

    def RecordActivity(self, text):
        self.Logging.Log(text)
        self.Gui.AddToActivityLog(text)

    def OnStreamlabsEventHandler(self, data):
        try:
            self.Logging.DebugLog(
                "Streamlabs raw event received: " + str(data))
            event = StreamlabsEvent(self, data)
            self.Logging.DebugLog(
                "Streamlabs processed event: " + str(event))
            if event.errored:
                return
            event.Process()
        except Exception as ex:
            self.Logging.RecordException(
                ex, "OBS Event Handler Critical Error - This event won't be processed")

    def UpdateStatus(self):
        if self.Streamlabs.connecting:
            self.Gui.UpdateStatusText(
                self.Translations.currentTexts["Status OBSConnecting"])
        elif self.Streamlabs.sio.eio.state == "connected":
            self.Gui.UpdateStatusText(
                self.Translations.currentTexts["Status Running"])
        else:
            self.Gui.UpdateStatusText(
                self.Translations.currentTexts["Status Stopped"])

    def Run(self):
        self.Logging.DebugLog("App Started")
        self.Gui.mainloop()


try:
    state = State()
    state.Setup()
    state.Run()
except Exception as ex:
    try:
        self.Streamlabs.Disconnect()
    except:
        pass
    try:
        state.Logging.RecordException(
            ex, "Application Critical Error - Application has been stopped")
    except:
        pass
    raise ex
