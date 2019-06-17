class TestEvents:
    _types = {
        "Streamlabs": {
            "Donation": {
                "valueInput": True,
                "listOptions": []
            }
        },
        "Patreon": {
            "Pledge": {
                "valueInput": True,
                "listOptions": []
            }
        },
        "Twitch": {
            "Follow": {
                "valueInput": False,
                "listOptions": []
            },
            "Subscribe": {
                "valueInput": True,  # TODO: this should use a listOptions when coded for
                "listOptions": []
            },
            "Receive Gift Subscription": {
                "valueInput": False,
                "listOptions": []
            },
            "Give Subscription Gifts": {
                "valueInput": True,
                "listOptions": []
            },
            "Host": {
                "valueInput": True,
                "listOptions": []
            },
            "Raid": {
                "valueInput": True,
                "listOptions": []
            }
        },
        "Youtube": {

        },
        "Mixer": {

        }
    }

    @staticmethod
    def GenerateTestEvent(eventPlatform, eventType, value, payloadCount):
        eventTypeString = ""
        eventForString = ""
        eventMessageConstructor = None
        if eventPlatform == "Twitch":
            if eventType == "Subscribe":
                eventTypeString = "subscription"
                eventForString = "twitch_account"

                def EventMessageConstructor(value, iterator):
                    iterator += 1
                    return {
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'months': '2',
                        'message': 'a test subscription',
                        'emotes': '1:25-26',
                        'sub_plan': str(int(value)),
                        'sub_plan_name': 'Channel\\sSubscription\\s(streamer)',
                        'sub_type': 'resub',
                        'gifter': None,
                        'subscriber_twitch_id': '12345678',
                        'streak_months': '2',
                        '_id': 'f5b4860c38313d4564d277ccc521a4a0',
                        'event_id': 'f5b4860c38313d4564d277ccc521a4a0'
                    }
                eventMessageConstructor = EventMessageConstructor

        return TestEvents._ConstructTestEventDict(eventForString, eventTypeString, eventMessageConstructor, value, payloadCount)

    @staticmethod
    def _ConstructTestEventDict(forString, typeString, messageConstructor, value, payloadCount):
        eventDict = {
            "for": forString,
            "type": typeString,
            "message": []
        }
        for i in range(payloadCount):
            eventDict["message"].append(messageConstructor(value, i))

        return eventDict

    @staticmethod
    def GetAttribute(platformString, typeString, attributeName):
        return TestEvents._types[platformString][typeString][attributeName]

    @staticmethod
    def GetPlatforms():
        return list(TestEvents._types.keys())

    @staticmethod
    def GetPlatformTypes(platformString):
        return list(TestEvents._types[platformString].keys())
