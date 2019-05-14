class StreamlabsEvent():
    def __init__(self, state, data):
        self.State = state
        self.Logging = state.Logging
        self.platform = "streamlabs"
        if "for" in data:
            self.platform = data["for"]
        self.type = data["type"]
        self.value = 0
        self.valueType = ""
        self.errored = False
        if not self._GetNormalisedData(data):
            self.State.RecordActivity(
                self.State.Translations.currentTexts["SteamlabsEvent UnrecognisedEvent"] + str(data))
            self.errored = True
            return

    def __str__(self):
        str_list = []
        str_list.append("{")
        str_list.append("id: '" + str(self.id) + "', ")
        str_list.append("platform: '" + str(self.platform) + "', ")
        str_list.append("type: '" + str(self.type) + "', ")
        str_list.append("errored: '" + str(self.errored) + "', ")
        str_list.append("valueType: '" + str(self.valueType) + "', ")
        str_list.append("value: '" + str(self.value) + "'")
        str_list.append("}")
        return ''.join(str_list)

    def _GetNormalisedData(self, data):
        if len(data["message"]) != 1:
            self.State.RecordActivity(
                self.State.Translations.currentTexts["SteamlabsEvent BadEventPayloadCount"] + len(data["message"]) + " data: " + str(data))
            return False
        message = data["message"][0]
        self.rawData = message
        self.id = message["_id"]
        if (self.platform == "streamlabs" and self.type == "donation"):
            self.valueType = "money"
            self.value = self.State.Currency.GetNormalisedValue(
                message["currency"], float(message["amount"]))
        elif (self.platform == "youtube_account" and self.type == "superchat"):
            self.valueType = "money"
            self.value = self.State.Currency.GetNormalisedValue(
                message["currency"], float(message["amount"])/1000000)
        elif (self.platform == "twitch_account" and self.type == "bits"):
            self.valueType = "money"
            self.value = float(message["amount"]) / 100
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
            return False
        else:
            return True

    @staticmethod
    def ShouldHandleEvent(data):
        if "for" in data:
            platform = data["for"]
            if not (platform == "streamlabs" or platform == "twitch_account" or platform == "youtube_account" or platform == "mixer_account"):
                return False
        elif "type" in data:
            type = data["type"]
            if not type == "donation":
                return False
        else:
            return False
        return True

    @staticmethod
    def ShouldIgnoreEvent(data):
        if "type" in data:
            type = data["type"]
            if (type == "streamlabels" or type == "streamlabels.underlying" or type == "alertPlaying" or type == "subscription-playing"):
                return True
        return False

    @staticmethod
    def GetEventTitles(data):
        eventDesc = ""
        if "for" in data:
            eventDesc += (" " + data["for"])
        if "type" in data:
            eventDesc += (" " + data["type"])
        if eventDesc == "":
            eventDesc = "No Title Details"
        return eventDesc

    def Process(self):
        # do stuff
        print("do event processing")
