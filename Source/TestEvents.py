from uuid import uuid4 as Uuid4
import random as Random
import datetime as DateTime


class TestEventUtils:
    _types = {
        "Streamlabs": {
            "Donation": {
                "valueInput": True,
                "quantityInput": False
            }
        },
        "Patreon": {
            "Pledge": {
                "valueInput": True,
                "quantityInput": False
            }
        },
        "Twitch": {
            "Follow": {
                "valueInput": False,
                "quantityInput": False
            },
            "Subscribe": {
                "valueInput": True,
                "quantityInput": False
            },
            "Give Specific Gift Subscription": {
                "valueInput": True,
                "quantityInput": False
            },
            "Give Random Gift Subscriptions": {
                "valueInput": True,
                "quantityInput": True
            },
            "Bits": {
                "valueInput": True,
                "quantityInput": False
            },
            "Host": {
                "valueInput": True,
                "quantityInput": False
            },
            "Raid": {
                "valueInput": True,
                "quantityInput": False
            }
        },
        "Youtube": {

        },
        "Mixer": {

        }
    }

    @staticmethod
    def GenerateTestEventArray(eventPlatform, eventType, value, special, payloadCount):
        primaryEvent = TestEventUtils.GenerateTestEvent(
            eventPlatform, eventType, value, special, payloadCount)
        testEventArray = [primaryEvent]
        if eventPlatform == "Twitch" and eventType == "Give Random Gift Subscriptions":
            for i in range(special):
                childEvent = TestEventUtils.GenerateTestEvent(
                    eventPlatform, "Give Specific Gift Subscription", value, i+2, 1)
                testEventArray.append(childEvent)
        return testEventArray

    @staticmethod
    def GenerateTestEvent(eventPlatform, eventType, value, special, payloadCount):
        eventTypeString = ""
        eventForString = ""
        eventMessageConstructor = None

        if eventPlatform == "Streamlabs":
            eventForString = "streamlabs"
            if eventType == "Donation":
                eventTypeString = "donation"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    id8Digits = TestEventUtils.GenerateRandomDigits(8)
                    return {
                        'id': id8Digits,
                        'name': 'UsEr' + str(iterator),
                        'amount': value,
                        'formatted_amount': '$' + "{:.2f}".format(value),
                        'formattedAmount': '$' + "{:.2f}".format(value),
                        'message': 'Test donation',
                        'currency': 'USD',
                        'emotes': '',
                        'iconClassName': 'fab paypal',
                        'to': {
                            'name': 'StreamerNaMe'
                        },
                        'from': 'UsEr' + str(iterator),
                        'from_user_id': None,
                        'donation_currency': 'USD',
                        '_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
        elif eventPlatform == "Patreon":
            eventForString = "patreon"
            if eventType == "Pledge":
                eventTypeString = "pledge"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    return {
                        'name': 'UsEr' + str(iterator),
                        'isTest': False,
                        'formatted_amount': '$' + "{:.2f}".format(value),
                        'amount': value,
                        'currency': 'USD',
                        'to': {
                            'name': 'StReAmErNaMe'
                        },
                        'from': 'Users Real Name',
                        '_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
        elif eventPlatform == "Twitch":
            eventForString = "twitch_account"
            if eventType == "Follow":
                eventTypeString = "follow"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    id8Digits = TestEventUtils.GenerateRandomDigits(8)
                    return {
                        'created_at': DateTime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'id': id8Digits,
                        'name': 'UsEr' + str(iterator),
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Subscribe":
                eventTypeString = "subscription"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    id8Digits = TestEventUtils.GenerateRandomDigits(8)
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
                        'subscriber_twitch_id': id8Digits,
                        'streak_months': '2',
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Give Specific Gift Subscription":
                eventTypeString = "subscription"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    giver = iterator + 1
                    if special != None and special != "":
                        iterator = special
                        giver = 1
                    eventId = TestEventUtils.GenerateUuid()
                    receiver8Digits = TestEventUtils.GenerateRandomDigits(8)
                    giver8Digits = TestEventUtils.GenerateRandomDigits(8)
                    return {
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'months': '2',
                        'message': 'a test subscription gift received',
                        'emotes': '1:25-26',
                        'sub_plan': str(int(value)),
                        'sub_plan_name': 'Channel\\sSubscription\\s(streamer)',
                        'sub_type': 'subgift',
                        'gifter': 'user' + str(giver),
                        'gifter_display_name': 'UsEr' + str(giver),
                        'gifter_twitch_id': giver8Digits,
                        'subscriber_twitch_id': receiver8Digits,
                        'streak_months': '2',
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Give Random Gift Subscriptions":
                eventTypeString = "subMysteryGift"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    return {
                        'sub_plan': str(int(value)),
                        'sub_type': 'submysterygift',
                        'gifter': 'user' + str(iterator),
                        'gifter_display_name': 'UsEr' + str(iterator),
                        'name': 'user' + str(iterator),
                        'amount': special,
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Bits":
                eventTypeString = "bits"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    idGuid = TestEventUtils.GenerateUuid()
                    return {
                        'id': idGuid,
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'amount': value,
                        'emotes': None,
                        'message': 'test bits',
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Host":
                eventTypeString = "host"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    return {
                        'name': 'UsEr' + str(iterator),
                        'viewers': int(value),
                        'type': 'manual',
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Raid":
                eventTypeString = "raid"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    eventId = TestEventUtils.GenerateUuid()
                    return {
                        'id': eventId,
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'raiders': int(value),
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor

        return TestEventUtils._ConstructTestEventDict(eventForString, eventTypeString, eventMessageConstructor, value, special, payloadCount)

    @staticmethod
    def _ConstructTestEventDict(forString, typeString, messageConstructor, value, special, payloadCount):
        eventDict = {
            "for": forString,
            "type": typeString,
            "message": []
        }
        for i in range(payloadCount):
            eventDict["message"].append(messageConstructor(value, special, i))

        return eventDict

    @staticmethod
    def GetAttribute(platformString, typeString, attributeName):
        return TestEventUtils._types[platformString][typeString][attributeName]

    @staticmethod
    def GetPlatforms():
        return list(TestEventUtils._types.keys())

    @staticmethod
    def GetPlatformTypes(platformString):
        return list(TestEventUtils._types[platformString].keys())

    @staticmethod
    def GenerateUuid():
        return Uuid4().hex

    @staticmethod
    def GenerateRandomDigits(count):
        number = ""
        for _ in range(count):
            number += str(Random.randint(0, 9))
        return number
