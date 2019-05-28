import re as Regex
import json as Json


class StreamlabsEvent():
    handledEventTypes = {}

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
        self.bestName = ""
        self.rawMessage = {}
        self.errored = False
        self.ignored = False

        if self.ShouldIgnoreEvent():
            self.ignored = True
            return

        if len(data["message"]) != 1:
            self.State.RecordActivity(
                self.State.Translations.currentTexts["StreamlabsEvent BadEventPayloadCount"] + str(
                    len(data["message"])))
            self.errored = True
            return
        message = data["message"][0]
        self.rawMessage = message
        self.id = message["_id"]
        if "display_name" in self.rawMessage.keys():
            self.bestName = self.rawMessage["display_name"]
        else:
            self.bestName = self.rawMessage["name"]

        if self.type == "donation":
            self.platform = "streamlabs"
        elif self.platform == "twitch_account" and self.type == "subscription" and "gifter" in self.rawMessage and self.rawMessage["gifter"] != None:
            self.type = "subscription_gift"
        self.handlerName = self.MakeHandlerString(
            self.platform, self.type)

    @property
    def value(self):
        return "{:.2f}".format(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        str_list = []
        str_list.append("{")
        str_list.append("id: '" + self.id + "', ")
        str_list.append("platform: '" + self.platform + "', ")
        str_list.append("type: '" + self.type + "', ")
        str_list.append("errored: '" + str(self.errored) + "', ")
        str_list.append("ignored: '" + str(self.ignored) + "', ")
        str_list.append("handlerName: '" + self.handlerName + "', ")
        str_list.append("valueType: '" + self.valueType + "', ")
        str_list.append("value: '" + str(self.value) + "', ")
        str_list.append("bestName: '" + self.bestName + "', ")
        str_list.append("rawData: " + str(self.rawData))
        str_list.append("}")
        return ''.join(str_list)

    def IsHandledEvent(self):
        if self.handlerName in self.handledEventTypes.keys():
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
        elif (self.handlerName == "twitch_account-subscription") or (self.handlerName == "twitch_account-subscription-gift"):
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

    def SubstituteEventDataIntoString(self, string, modValue="''"):
        instances = StreamlabsEvent.FindAttributeTagsInString(string)
        for instance in instances:
            dataKeyName = instance[1:-1]
            dataKeyValue = "''"
            if dataKeyName == "MODVALUE":
                dataKeyValue = modValue
            elif dataKeyName == "VALUE":
                dataKeyValue = self.value
            elif dataKeyName == "PLATFORM":
                dataKeyValue = self.platform
            elif dataKeyName == "TYPE":
                dataKeyValue = self.type
            elif dataKeyName == "VALUETYPE":
                dataKeyValue = self.valueType
            elif dataKeyName == "ID":
                dataKeyValue = self.id
            elif dataKeyName == "BESTNAME":
                dataKeyValue = self.bestName
            elif dataKeyName in self.rawMessage:
                dataKeyValue = self.rawMessage[dataKeyName]
            string = string.replace(instance, str(dataKeyValue))
        return string

    @staticmethod
    def FindAttributeTagsInString(string):
        return Regex.findall(r"\[[a-z_A-Z]+\]", string)

    @staticmethod
    def LoadEventDefinitions():
        with open("eventDefinitions.json", "r") as file:
            data = Json.load(file)
        file.closed
        StreamlabsEvent.handledEventTypes = data

    @staticmethod
    def IsBadEventAttritubeUsed(eventType, string, modValueAllowed):
        instances = StreamlabsEvent.FindAttributeTagsInString(string)
        for instance in instances:
            dataKeyName = instance[1:-1]
            if dataKeyName in ["ALL", "NOTHING"]:
                continue
            if dataKeyName == "MODVALUE" and not modValueAllowed:
                return "MODVALUE used when not allowed"
            if dataKeyName in StreamlabsEvent.handledEventTypes['[ALL]'].keys():
                continue
            if dataKeyName not in StreamlabsEvent.handledEventTypes[eventType].keys():
                return instance + " invalid in " + eventType
        return ""
