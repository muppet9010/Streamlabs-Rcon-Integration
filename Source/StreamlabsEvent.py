class StreamlabsEvent():
    handledEventTypes = ["youtube_account-superchat", "youtube_account-subscription", "youtube_account-follow", "twitch_account-bits", "twitch_account-subscription",
                         "twitch_account-follow", "twitch_account-host", "twitch_account-raid", "mixer_account-subscription", "mixer_account-follow", "mixer_account-host", "streamlabs-donation"]

    def __init__(self, state, data):
        self.State = state
        self.Logging = state.Logging

        if "for" in data:
            self.platform = data["for"]
        else:
            self.platform = ""
        if "for" in data:
            self.type = data["type"]
        else:
            self.type = ""
        self.rawData = data
        self.id = ""
        self.handlerName = ""
        self.value = 0
        self.valueType = ""
        self.errored = False

        if len(data["message"]) != 1:
            self.State.RecordActivity(
                self.State.Translations.currentTexts["StreamlabsEvent BadEventPayloadCount"] + len(data["message"]))
            self.errored = True
            return
        message = data["message"][0]
        self.rawMessage = message
        self.id = message["_id"]

    @property
    def value(self):
        return "{:.2f}".format(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        str_list = []
        str_list.append("{")
        str_list.append("id: '" + str(self.id) + "', ")
        str_list.append("platform: '" + str(self.platform) + "', ")
        str_list.append("type: '" + str(self.type) + "', ")
        str_list.append("errored: '" + str(self.errored) + "', ")
        str_list.append("handlerName: '" + str(self.handlerName) + "', ")
        str_list.append("valueType: '" + str(self.valueType) + "', ")
        str_list.append("value: '" + str(self.value) + "'")
        str_list.append("}")
        return ''.join(str_list)

    def IsHandledEvent(self):
        if self.type == "donation":
            self.platform = "streamlabs"
        rawHandlerString = self.MakeHandlerString(
            self.platform, self.type)
        if rawHandlerString in self.handledEventTypes:
            self.handlerName = rawHandlerString
            return True
        else:
            return False

    @staticmethod
    def MakeHandlerString(platform, type):
        return platform + "-" + type

    def ShouldIgnoreEvent(self):
        if (self.platform == "streamlabs") and (self.type == "streamlabels" or self.type == "streamlabels.underlying" or self.type == "alertPlaying" or self.type == "subscription-playing" or self.type == "rollEndCredits" or self.type == "subMysteryGift"):
            return True
        if self.id in self.State.donationsIdsProcessed:
            self.Logging.DebugLog(
                "Streamlabs donation event being ignored as in processed list: " + self.id)
            return True
        return False

    def PopulateNormalisedData(self):
        if (self.handlerName == "streamlabs-donation"):
            self.valueType = "money"
            self.value = self.State.Currency.GetNormalisedValue(
                self.rawMessage["currency"], float(self.rawMessage["amount"]))
            self.State.donationsIdsProcessed[self.id] = True
        elif (self.handlerName == "youtube_account-superchat"):
            self.valueType = "money"
            self.value = self.State.Currency.GetNormalisedValue(
                self.rawMessage["currency"], float(self.rawMessage["amount"])/1000000)
        elif (self.handlerName == "twitch_account-bits"):
            self.valueType = "money"
            self.value = round(float(self.rawMessage["amount"]) / 100, 2)
        elif (self.handlerName == "twitch_account-subscription"):
            self.valueType = "money"
            subPlan = self.rawMessage["sub_plan"]
            if subPlan == "Prime" or subPlan == "1000":
                self.value = 5
            elif subPlan == "2000":
                self.value = 10
            elif subPlan == "3000":
                self.value = 25
            else:
                self.State.RecordActivity(
                    self.State.Translations.currentTexts["StreamlabsEvent UnrecognisedTwitchSubscriptionType"] + subPlan)
                return False
        elif (self.handlerName == "youtube_account-subscription"):
            self.valueType = "money"
            self.value = 5
        elif (self.handlerName == "mixer_account-subscription"):
            self.valueType = "money"
            self.value = 8
        elif (self.handlerName == "youtube_account-follow" or self.handlerName == "twitch_account-follow" or self.handlerName == "mixer_account-follow"):
            self.valueType = "follow"
            self.value = 1
        elif (self.handlerName == "twitch_account-host" or self.handlerName == "mixer_account-host"):
            self.valueType = "viewer"
            self.value = self.rawMessage["viewers"]
        elif (self.handlerName == "twitch_account-raid"):
            self.valueType = "viewer"
            self.value = self.rawMessage["raiders"]
        else:
            return False
        return True

    def GetEventTitlesAsPrettyString(self):
        eventDesc = ""
        if self.platform != "":
            eventDesc += ("for: '" + self.platform + "' ")
        if self.type != "":
            eventDesc += ("type: '" + self.type + "' ")
        if eventDesc == "":
            eventDesc = "No Title Details"
        return eventDesc

    def Process(self):
        print("doing event processing")
        actionText = self.State.Profiles.currentProfile.GetActionTextForEvent(
            self)
        # TODO needs to handle custom errors being thrown from within this search code
        if actionText == None:
            print("No action text found")
        else:
            print("actionText: " + actionText.text)
