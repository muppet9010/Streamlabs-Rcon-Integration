class Translations:
    def __init__(self, state):
        self.state = state
        self.language = "en"
        self.currentTexts = self.LoadLocalisedTexts(self.language)

    def LoadLocalisedTexts(self, language):
        if language == "en":
            return {
                "Gui SelectProfile": "Select a profile",
                "Gui StartButton": "Start",
                "Gui StopButton": "Stop",
                "Gui QuitButton": "Quit",
                "Gui ActivityLogTitle": "Actvity Log",
                "Gui TestEventButton": "Test Event",
                "Gui SelectTestEventPlatform": "Select Platform",
                "Gui SelectTestEventType": "Select Type",
                "Message NeedProfileBeforeStart": "Must select a profile before starting",
                "Message Started": "Started",
                "Message StreamlabsUnexpectedStop": "Error Streamlabs Stopped Unexpectedly",
                "Message Stopped": "Stopped",
                "Status OBSConnecting": "OBS Connecting",
                "Status Running": "Running",
                "Status Stopped": "Stopped",
                "Currency WebsiteDownloadFailed": "ERROR: Can't get currency conversion data from website",
                "StreamlabsEvent ErrorProcessingEvent": "ERROR: event data not as expected: ",
                "StreamlabsEvent BadEventPayloadCount": "ERROR: wrong number of payloads in event: ",
                "StreamlabsEvent MissingEventPayloadCount": "ERROR: no payload in event",
                "StreamlabsEvent UnrecognisedEvent": "WARNING: Streamlabs event being ignored as not recognised: ",
                "StreamlabsEvent UnrecognisedTwitchSubscriptionType": "ERROR: unrecognised twitch subscription type: ",
                "StreamlabsEvent NoProfileAction": "WARNING: no reaction found for event: ",
                "StreamlabsEvent EventHandled": "Event Handled: ",
                "Rcon CommandError": "ERROR: Rcon command failed, run manually: ",
                "Rcon CommandResponseWarning": "WARNING: Rcon got response from server: ",
                "Rcon TestErrorMessage": "Rcon connection test message: ",
                "Rcon NoCommand": "Rcon Test Mode: ",
                "TestEvent InvalidTestEvent": "Invalid Test Event Selection: "
            }

    def GetTranslation(self, key):
        if key in self.currentTexts.keys():
            return self.currentTexts[key]
        else:
            self.state.logging.Log(
                "ERROR: Missing translation in '" + self.language + "': " + key)
            return "MISSING KEY"
