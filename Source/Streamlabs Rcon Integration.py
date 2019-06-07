from Logging import Logging
from Streamlabs import Streamlabs
from Gui import Gui, GuiWindow
from Currency import Currency
from StreamlabsEvent import StreamlabsEvent
import json as Json
from Config import Config
from Profiles import Profiles
from Rcon import Rcon
from Translations import Translations


class State():
    def __init__(self):
        self.config = Config(self)
        self.logging = Logging(self)
        self.config.LogMissingSettings()
        self.donationsIdsProcessed = {}

    def Setup(self):
        self.translations = Translations(self)
        self.currency = Currency(self)
        StreamlabsEvent.LoadEventDefinitions()
        self.profiles = Profiles(self)
        self.streamlabs = Streamlabs(self)
        self.rcon = Rcon(self)
        self.guiWindow = GuiWindow(self)
        self.gui = self.guiWindow.gui
        self.gui.CreateWidgets()

    def OnStartButtonHandler(self):
        try:
            self.logging.DebugLog("Start Button Pressed")
            if self.gui.selectedProfileName.get() == "" or self.gui.selectedProfileName.get() == self.translations.currentTexts["Gui SelectProfile"]:
                self.RecordActivity(
                    self.translations.currentTexts["Message NeedProfileBeforeStart"])
                return
            self.profiles.SetCurrentProfile(self.gui.selectedProfileName.get())
            self.gui.OnStarted()
            if not self.currency.GetRates():
                self.logging.Log("Error: Get Rates for Currency failed")
                self.gui.OnStopped()
                return
            if not self.rcon.TestConnection():
                self.gui.OnStopped()
                return
            self.streamlabs.Connect()
            self.UpdateStatus()
        except Exception as ex:
            self.logging.RecordException(ex, "Start Button Critical Error")
            self.gui.OnStopped()

    def OnStreamlabsConnectHandler(self):
        try:
            self.logging.DebugLog("Streamlabs Connected")
            self.streamlabs.disconnecting = False
            if self.streamlabs.connecting:
                self._OnStartButtonPostStreamlabsConnection()
        except Exception as ex:
            self.logging.RecordException(ex, "OBS Connected Critical Error")

    def _OnStartButtonPostStreamlabsConnection(self):
        try:
            self.streamlabs.connecting = False
            self.UpdateStatus()
            self.RecordActivity(
                self.translations.currentTexts["Message Started"])
        except Exception as ex:
            self.logging.RecordException(
                ex, "Start Button Post Connection Critical Error")
            self.gui.OnStopped()

    def OnStopButtonHandler(self):
        try:
            self.logging.DebugLog("Stop Button Pressed")
            self.streamlabs.Disconnect()
        except Exception as ex:
            self.logging.RecordException(ex, "Stop Button Critical Error")

    def OnStreamlabsDisconnectHandler(self):
        try:
            self.logging.DebugLog("Streamlabs Disconnected Pressed")
            self.gui.OnStopped()
            if not self.streamlabs.disconnecting:
                self.RecordActivity(
                    self.translations.currentTexts["Message StreamlabsUnexpectedStop"])
            else:
                self.RecordActivity(
                    self.translations.currentTexts["Message Stopped"])
            self.streamlabs.disconnecting = False
            self.UpdateStatus()
        except Exception as ex:
            self.logging.RecordException(ex, "OBS Disconnected Critical Error")

    def OnQuitButtonHandler(self):
        try:
            self.logging.Log("Quit Button")
            self.streamlabs.Disconnect()
            self.gui.master.destroy()
        except Exception as ex:
            self.logging.RecordException(ex, "Quit Button Critical Error")

    def RecordActivity(self, text):
        self.logging.Log(text)
        self.gui.AddToActivityLog(text)

    def OnStreamlabsEventHandler(self, data):
        try:
            event = StreamlabsEvent(self, data)
            if event.errored:
                self.logging.DebugLog(
                    "Streamlabs event errored during initial handling: " + str(event))
                return
            if event.ignored:
                self.logging.DebugLog(
                    "Streamlabs event being ignored: " + event.GetEventRawTitlesAsPrettyString())
                return
            self.logging.DebugLog(
                "Streamlabs raw event data: " + str(data))
            if not event.IsHandledEvent():
                self.RecordActivity(
                    self.translations.currentTexts["StreamlabsEvent UnrecognisedEvent"] + event.GetEventRawTitlesAsPrettyString())
                return
            if not event.PopulateNormalisedData():
                self.RecordActivity(
                    self.translations.currentTexts["StreamlabsEvent ErrorProcessingEvent"] + event.GetEventRawTitlesAsPrettyString())
                return
            self.logging.DebugLog(
                "Streamlabs processed event: " + str(event))

            actionText = self.profiles.currentProfile.GetActionTextForEvent(
                event)
            if actionText == None:
                self.RecordActivity(
                    self.translations.currentTexts["StreamlabsEvent NoProfileAction"] + event.GetEventRawTitlesAsPrettyString())
                self.logging.DebugLog(
                    "No profile action for: " + event.GetEventRawTitlesAsPrettyString())
                return
            actionType = ""
            response = ""
            if actionText == "":
                actionType = "Ignore event"
                self.logging.DebugLog(
                    "NOTHING action specified for: " + event.GetEventRawTitlesAsPrettyString())
            else:
                actionType = "Rcon command"
                try:
                    response = self.rcon.SendCommand(actionText)
                except Exception as ex:
                    self.logging.RecordException(ex, "Rcon event failed")
                    self.RecordActivity(
                        self.translations.currentTexts["Rcon CommandError"] + actionText)
                    return
            self.RecordActivity(
                self.translations.currentTexts["StreamlabsEvent EventHandled"] + event.GetEventRawTitlesAsPrettyString() + " : " + event.bestName + " : value " + str(event.value) + " : " + actionType)
            if response != "":
                self.RecordActivity(
                    self.translations.currentTexts["Rcon CommandResponseWarning"] + response)
            self.logging.DebugLog("Action done: " + actionText)
        except Exception as ex:
            self.logging.RecordException(
                ex, "OBS Event Handler Critical Error - This event won't be processed")

    def UpdateStatus(self):
        if self.streamlabs.connecting:
            self.gui.UpdateStatusText(
                self.translations.currentTexts["Status OBSConnecting"])
        elif self.streamlabs.sio.eio.state == "connected":
            self.gui.UpdateStatusText(
                self.translations.currentTexts["Status Running"])
        else:
            self.gui.UpdateStatusText(
                self.translations.currentTexts["Status Stopped"])

    def Run(self):
        self.logging.DebugLog("App Started")
        self.gui.mainloop()


try:
    state = State()
    state.Setup()
    state.Run()
except Exception as ex:
    try:
        self.streamlabs.Disconnect()
    except:
        pass
    try:
        state.logging.RecordException(
            ex, "Application Critical Error - Application has been stopped")
    except:
        pass
