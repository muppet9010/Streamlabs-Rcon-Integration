from uuid import uuid4 as Uuid4
import random as Random
import datetime as DateTime


class TestEvents:
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
    def GenerateTestEvent(eventPlatform, eventType, value, quantity, payloadCount):
        eventTypeString = ""
        eventForString = ""
        eventMessageConstructor = None

        if eventPlatform == "Streamlabs":
            eventForString = "streamlabs"
            if eventType == "Donation":
                eventTypeString = "donation"

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
                    id8Digits = TestEvents.GenerateRandomDigits(8)
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
                    id8Digits = TestEvents.GenerateRandomDigits(8)
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
                    id8Digits = TestEvents.GenerateRandomDigits(8)
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    giver = iterator + 1
                    eventId = TestEvents.GenerateUuid()
                    receiver8Digits = TestEvents.GenerateRandomDigits(8)
                    giver8Digits = TestEvents.GenerateRandomDigits(8)
                    return {
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'months': '2',
                        'message': 'a test subscription gift',
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
                    return {
                        'sub_plan': str(int(value)),
                        'sub_type': 'submysterygift',
                        'gifter': 'user' + str(iterator),
                        'gifter_display_name': 'UsEr' + str(iterator),
                        'name': 'user' + str(iterator),
                        'amount': quantity,
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Host":
                eventTypeString = "host"

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
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

                def EventMessageConstructor(value, quantity, iterator):
                    iterator += 1
                    eventId = TestEvents.GenerateUuid()
                    return {
                        'id': eventId,
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'raiders': int(value),
                        '_id': eventId,
                        'event_id': eventId
                    }
                eventMessageConstructor = EventMessageConstructor

        return TestEvents._ConstructTestEventDict(eventForString, eventTypeString, eventMessageConstructor, value, quantity, payloadCount)

    @staticmethod
    def _ConstructTestEventDict(forString, typeString, messageConstructor, value, quantity, payloadCount):
        eventDict = {
            "for": forString,
            "type": typeString,
            "message": []
        }
        for i in range(payloadCount):
            eventDict["message"].append(messageConstructor(value, quantity, i))

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

    @staticmethod
    def GenerateUuid():
        return Uuid4().hex

    @staticmethod
    def GenerateRandomDigits(count):
        number = ""
        for _ in range(count):
            number += str(Random.randint(0, 9))
        return number
