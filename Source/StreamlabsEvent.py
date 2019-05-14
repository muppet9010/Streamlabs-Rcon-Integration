class StreamlabsEvent():
    def __init__(self, state, data):
        self.State = state
        self.Logging = state.Logging
        self.id = data["event_id"]
        self.platform = data["for"]
        self.type = data["type"]
        self.value = 0
        self.valueType = ""
        if not (self.platform == "streamlabs" or self.platform == "twitch_account" or self.platform == "youtube_account" or self.platform == "mixer_account"):
            self.errored = True
            return
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

    def Process(self):
        # do stuff
        print("do event processing")
