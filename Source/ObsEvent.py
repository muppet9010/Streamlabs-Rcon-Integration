class ObsEvent():
    def __init__(self, data, gui, currency):
        self.gui = gui
        self.currency = currency
        self.id = data["event_id"]
        self.platform = data["for"]
        self.type = data["type"]
        if not self.GetNormalisedData(data):
            return

    def GetNormalisedData(self, data):
        if len(data["message"]) != 1:
            self.gui.AddToActivityLog("wrong number of payloads in event: " +
                                      len(data["message"]) + " data: " + str(data))
            return False
        message = data["message"][0]
        if (self.platform == "streamlabs" and self.type == "donation") or (self.platform == "youtube_account" and self.type == "superchat"):
            self.valueType = "money"
            self.value = self.currency.GetNormalisedValue(
                message.currency, message.amount)
        elif (self.platform == "twitch_account" and self.type == "bits"):
            self.valueType = "money"
            self.value = message["amount"] / 100
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
            self.gui.AddToActivityLog("Event not recognised: " + str(data))
            return False
        else:
            return True
