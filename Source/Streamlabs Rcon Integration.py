from Logging import Logging
from Streamlabs import Streamlabs
from Gui import Gui, GuiWindow
from Currency import Currency
from StreamlabsEvent import StreamlabsEvent, StreamlabsEventUtils
import json as Json
from Config import Config
from Profiles import Profiles
from Rcon import Rcon
from Translations import Translations
from TestEvents import TestEventUtils
import datetime as Datetime
import random as Random
import time as Time
import threading as Threading


class State():
    def __init__(self):
        self.version = "0.1.5"
        self.config = Config(self)
        self.logging = Logging(self)
        self.config.LogMissingSettings()

    def Setup(self):
        self.eventIdsProcessed = {}
        self.mysterySubGifts = {}
        self.translations = Translations(self)
        self.currency = Currency(self)
        StreamlabsEventUtils.LoadEventDefinitions()
        self.profiles = Profiles(self)
        self.streamlabs = Streamlabs(self)
        self.rcon = Rcon(self)
        self.testEventUtils = TestEventUtils()
        self.guiWindow = GuiWindow(self)
        self.gui = self.guiWindow.gui
        self.gui.Setup()
        self.sequentialEventId = 0

    def OnStartButtonHandler(self):
        try:
            self.logging.DebugLog("Start Button Pressed")
            if self.gui.selectedProfileName.get() == "" or self.gui.selectedProfileName.get() == self.translations.GetTranslation("Gui SelectProfile"):
                self.RecordActivity(
                    self.translations.GetTranslation("Message NeedProfileBeforeStart"))
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
                self.translations.GetTranslation("Message Started"))
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
                    self.translations.GetTranslation("Message StreamlabsUnexpectedStop"))
            else:
                self.RecordActivity(
                    self.translations.GetTranslation("Message Stopped"))
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
            # The random small delay (up to 0.1 seconds) is to handle duplicate events coming in at the same moment from StreamLabs. In the past this would cause double firing of events as they would both be processed in parallel. This isn't perfect still as the duplicate events could end up with the same delay and thus be processed in parallel, however this is very unlikely.
            # It does have an issue in that if the Twitch MysteryGiftSub event is delayed after the subscription events then they will be double counted. Set as very small delay to try and avoid this issue. The subscription gift events do come in after the mystery gift event, but it is only a delay of a part of a second. The ideal fix is to move to a event queue processing system, but that's far more work for a dead project.
            random = Random.Random()
            random.seed(Threading.get_ident())
            sleepTime = random.randrange(1,1000)/10000

            self.sequentialEventId = self.sequentialEventId + 1
            self.logging.DebugLog("Sleeping event number " + str(self.sequentialEventId) + " for: " + str(sleepTime) + ". Received time: " + Datetime.datetime.now().strftime("%H:%M:%S.%f"))
            Time.sleep(sleepTime)
            self.logging.DebugLog(
                "Streamlabs raw event number " + str(self.sequentialEventId) + " data: " + str(data))
            events = StreamlabsEventUtils.GenerateEventPerPayload(self, data)
            if events == None:
                return
            for event in events:
                if event.errored:
                    self.logging.DebugLog(
                        "Streamlabs event errored during initial handling: " + str(event))
                    return
                if event.ignored:
                    self.logging.DebugLog(
                        "Streamlabs event being ignored: " + event.GetEventRawTitlesAsPrettyString())
                    return
                if not event.IsHandledEvent():
                    self.RecordActivity(
                        self.translations.GetTranslation("StreamlabsEvent UnrecognisedEvent") + event.GetEventRawTitlesAsPrettyString())
                    return
                if not event.PopulateNormalisedData():
                    self.RecordActivity(
                        self.translations.GetTranslation("StreamlabsEvent ErrorProcessingEvent") + event.GetEventRawTitlesAsPrettyString())
                    return
                self.logging.DebugLog(
                    "Streamlabs processed event: " + str(event))

                actionTexts = self.profiles.currentProfile.GetActionTextsForEvent(
                    event)
                if len(actionTexts) == 0:
                    self.RecordActivity(
                        self.translations.GetTranslation("StreamlabsEvent NoProfileAction") + event.GetEventRawTitlesAsPrettyString())
                    self.logging.DebugLog(
                        "No profile action for: " + event.GetEventRawTitlesAsPrettyString())
                    return
                for actionText in actionTexts:
                    actionType = ""
                    response = ""
                    if actionText == "":
                        actionType = "Ignore event"
                        self.logging.DebugLog(
                            "NOTHING action specified for: " + event.GetEventRawTitlesAsPrettyString())
                    else:
                        actionType = "Rcon command"
                        try:
                            self.logging.DebugLog(
                                "Doing Rcon command: " + actionText)
                            response = self.rcon.SendCommand(actionText)
                        except Exception as ex:
                            self.logging.RecordException(
                                ex, "Rcon event failed")
                            self.RecordActivity(
                                self.translations.GetTranslation("Rcon CommandError") + actionText)
                            return
                    if response != "":
                        self.RecordActivity(
                            self.translations.GetTranslation("Rcon CommandResponseWarning") + response)
                    self.logging.DebugLog("Action done: " + actionText)
                self.RecordActivity(
                    self.translations.GetTranslation("StreamlabsEvent EventHandled") + event.GetEventRawTitlesAsPrettyString() + " : " + event.bestName + " : value " + str(event.value) + " : " + actionType)
        except Exception as ex:
            self.logging.RecordException(
                ex, "OBS Event Handler Critical Error - This event won't be processed")

    def OnTestEventButtonHandler(self):
        try:
            testEventPlatform = self.gui.selectedTestEventPlatform.get()
            testEventType = self.gui.selectedTestEventType.get()
            testEventValue = ""
            if TestEventUtils.GetAttribute(testEventPlatform, testEventType, "valueInput"):
                testEventValue = self.gui.testEventValue.get()
                # Twitch Subscribe events allow special values.
                if testEventPlatform == "Twitch" and testEventType == "Subscribe":
                    # If the value is "Prime" then just accept it.
                    if testEventValue != "Prime":
                        # Value isn't "Prime" so make sure its a number.
                        try:
                            testEventValue = float(testEventValue)
                        except:
                            self.RecordActivity(
                                self.translations.GetTranslation("TestEvent ValueNotFloatOrPrime") + str(testEventValue))
                            return
                else:
                    # As a standard event type the value must be a number
                    try:
                        testEventValue = float(testEventValue)
                    except:
                        self.RecordActivity(
                            self.translations.GetTranslation("TestEvent ValueNotFloat") + str(testEventValue))
                        return
            testEventQuantity = ""
            if TestEventUtils.GetAttribute(testEventPlatform, testEventType, "quantityInput"):
                try:
                    testEventQuantity = self.gui.testEventQuantity.get()
                    testEventQuantity = int(testEventQuantity)
                    if testEventQuantity <= 0:
                        raise ValueError()
                except:
                    self.RecordActivity(
                        self.translations.GetTranslation("TestEvent QuantityCountNotInt") + str(testEventQuantity))
                    return
            testEventPayloadCount = 1
            if TestEventUtils.GetAttribute(testEventPlatform, testEventType, "payloadInput"):
                try:
                    testEventPayloadCount = self.gui.testEventPayloadCount.get()
                    testEventPayloadCount = int(testEventPayloadCount)
                    if testEventPayloadCount <= 0:
                        raise ValueError()
                except:
                    self.RecordActivity(self.translations.GetTranslation(
                        "TestEvent PayloadCountNotInt") + str(testEventPayloadCount))
                    return
            testEventArray = self.testEventUtils.GenerateTestEventArray(
                testEventPlatform, testEventType, testEventValue, testEventQuantity, testEventPayloadCount)
            if len(testEventArray) > 0:
                for testEvent in testEventArray:
                    self.OnStreamlabsEventHandler(testEvent)

                # Run each event in its own thread as this is how they come in from external partners.
                # In real world Twitch multi sub gift the first mysteryGiftSub comes in and then some time later (part of a second) all of the recipient events come in with near 0 gap between each each. This is very hard to setup test for, so commented out for now.

                #def testEventTask(self, testEvent):
                #    self.OnStreamlabsEventHandler(testEvent)

                #for testEvent in testEventArray:
                #    thread = Threading.Thread(target=testEventTask, args=(self, testEvent))
                #    thread.start()
            else:
                self.RecordActivity(
                    self.translations.GetTranslation("TestEvent InvalidTestEvent") + testEventPlatform + " - " + testEventType)
        except Exception as ex:
            self.logging.RecordException(
                ex, "Test Event Critical Error - Failed to run test event")

    def UpdateStatus(self):
        if self.streamlabs.connecting:
            self.gui.UpdateStatusText(
                self.translations.GetTranslation("Status OBSConnecting"))
        elif self.streamlabs.sio.eio.state == "connected":
            self.gui.UpdateStatusText(
                self.translations.GetTranslation("Status Running"))
        else:
            self.gui.UpdateStatusText(
                self.translations.GetTranslation("Status Stopped"))

    def Run(self):
        self.logging.Log("App Started")
        self.gui.mainloop()


try:
    state = State()
    state.Setup()
    state.Run()
except Exception as ex:
    try:
        state.streamlabs.Disconnect()
    except:
        pass
    try:
        state.logging.RecordException(
            ex, "Application Critical Error - Application has been stopped")
    except:
        pass
