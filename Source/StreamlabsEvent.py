import re as Regex
import json as Json
import traceback as Traceback


class StreamlabsEvent():
    handledEventTypes = {}

    def __init__(self, state, data):
        self.state = state
        self.logging = state.logging

        if "for" in data:
            self.platform = data["for"]
        else:
            self.platform = ""
        if "type" in data:
            self.type = data["type"]
        else:
            self.type = ""

        self.rawData = data
        self.id = ""
        self.handlerName = ""
        self.value = 0
        self.valueType = ""
        self.bestName = ""
        self.bestComment = ""
        self.rawMessage = {}
        self.errored = False
        self.ignored = False

        if self.ShouldIgnoreEvent():
            self.ignored = True
            return

        if "message" not in data:
            self.state.RecordActivity(
                self.state.translations.GetTranslation("StreamlabsEvent MissingEventPayloadCount"))
            self.errored = True
            return
        if len(data["message"]) != 1:
            self.state.RecordActivity(
                self.state.translations.GetTranslation("StreamlabsEvent BadEventPayloadCount") + str(
                    len(data["message"])))
            self.errored = True
            return
        rawMessage = data["message"][0]
        self.rawMessage = rawMessage

        self.id = self.rawMessage["_id"]
        if "display_name" in self.rawMessage.keys():
            self.bestName = self.rawMessage["display_name"]
        elif "name" in self.rawMessage.keys():
            self.bestName = self.rawMessage["name"]
        if "message" in self.rawMessage.keys():
            self.bestComment = self.rawMessage["message"]
        elif "comment" in self.rawMessage.keys():
            self.bestComment = self.rawMessage["comment"]

        if self.type == "donation" and self.platform == "":
            self.platform = "streamlabs"
        elif self.platform == "twitch_account" and self.type == "subscription" and "gifter" in self.rawMessage and self.rawMessage["gifter"] != None:
            self.type = "subscription_gift"
        self.handlerName = self.MakeHandlerString(
            self.platform, self.type)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = float(value)

    def GetValueForDisplay(self):
        if self._value.is_integer():
            return str(int(self._value))
        else:
            return self._value

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
        if (self.type == "streamlabels") or (self.type == "streamlabels.underlying") or (self.type == "alertPlaying") or (self.type == "subscription-playing") or (self.type == "rollEndCredits") or (self.type == "subMysteryGift"):
            return True
        if (self.platform == "widget"):
            return True
        if self.id in self.state.donationsIdsProcessed:
            self.logging.DebugLog(
                "Streamlabs donation event being ignored as in processed list: " + self.id)
            return True
        return False

    def PopulateNormalisedData(self):
        if (self.handlerName == "streamlabs-donation"):
            self.valueType = "money"
            self.value = self.state.currency.GetNormalisedValue(
                self.rawMessage["currency"], float(self.rawMessage["amount"]))
            self.state.donationsIdsProcessed[self.id] = True
        elif (self.handlerName == "youtube_account-superchat"):
            self.valueType = "money"
            self.value = self.state.currency.GetNormalisedValue(
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
                self.state.RecordActivity(
                    self.state.translations.GetTranslation("StreamlabsEvent UnrecognisedTwitchSubscriptionType") + subPlan)
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

    def GetEventRawTitlesAsPrettyString(self):
        eventDesc = ""
        if self.platform != "":
            eventDesc += self.platform
        if self.type != "":
            if eventDesc != "":
                eventDesc += " - "
            eventDesc += (self.type)
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
                dataKeyValue = self.GetValueForDisplay()
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
            elif dataKeyName == "BESTCOMMENT":
                dataKeyValue = self.bestComment
            elif dataKeyName in self.rawMessage:
                dataKeyValue = self.rawMessage[dataKeyName]
            string = string.replace(
                instance, StreamlabsEvent.EspaceStringForRcon(str(dataKeyValue)))
        return string

    @staticmethod
    def FindAttributeTagsInString(string):
        return Regex.findall(r"\[[a-z_A-Z0-9]+\]", string)

    @staticmethod
    def LoadEventDefinitions():
        with open("eventDefinitions.json", "r") as file:
            data = Json.load(file)
        file.closed
        StreamlabsEvent.handledEventTypes = data

    @staticmethod
    def IsBadEventAttritubeUsed(eventType, string, modValueAllowed):
        if string in ["", "[ALL]", "[NOTHING]"]:
            return ""
        instances = StreamlabsEvent.FindAttributeTagsInString(string)
        for instance in instances:
            dataKeyName = instance[1:-1]
            if dataKeyName == "MODVALUE" and not modValueAllowed:
                return "[MODVALUE] used when not allowed"
            if dataKeyName in StreamlabsEvent.handledEventTypes['[ALL]'].keys():
                continue
            if eventType == "" or dataKeyName not in StreamlabsEvent.handledEventTypes[eventType].keys():
                return instance + " not a valid attribute for this event"
        return ""

    @staticmethod
    def IsScriptValid(scriptString):
        if scriptString in ["", "[ALL]", "[NOTHING]"]:
            return ""
        instances = StreamlabsEvent.FindAttributeTagsInString(scriptString)
        testScriptString = scriptString
        for instance in instances:
            testScriptString = testScriptString.replace(instance, str(1))
        try:
            eval(testScriptString)
        except Exception:
            return "config value: " + scriptString + "\n" + Traceback.format_exc(limit=0, chain=False)
        return ""

    @staticmethod
    def EspaceStringForRcon(text):
        text = text.replace("\\", "\\\\")
        text = text.replace("'", "\\'")
        text = text.replace('"', '\\"')
        return text
