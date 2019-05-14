class Translations:
    def __init__(self, state):
        self.State = state
        language = "en"
        self.currentTexts = self.GetLocalisedTexts(language)

    def GetLocalisedTexts(self, language):
        if language == "en":
            return {
                "Gui SelectProfile": "Select a profile",
                "Gui StartButton": "Start",
                "Gui StopButton": "Stop",
                "Gui QuitButton": "Quit",
                "Gui ActivityLogTitle": "Actvity Log",
                "Message NeedProfileBeforeStart": "Must select a profile before starting",
                "Message Started": "Started",
                "Message StreamlabsUnexepctedStop": "Error Streamlabs Stopped Unexpectedly",
                "Message Stopped": "Stopped",
                "Status OBSConnecting": "OBS Connecting",
                "Status Running": "Running",
                "Status Stopped": "Stopped",
                "Currency WebsiteDownloadFailed": "ERROR: Can't get currency conversion data from website",
                "SteamlabsEvent UnrecognisedEvent": "ERROR: Event not recognised: ",
                "SteamlabsEvent BadEventPayloadCount": "ERROR: wrong number of payloads in event: "
            }
