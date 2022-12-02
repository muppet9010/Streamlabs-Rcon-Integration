from uuid import uuid4 as Uuid4
from uuid import UUID as Uuid
import random as Random
import datetime as DateTime
import string as String
import random as Random
import json as Json


class TestEventUtils:
    _types = {
        "Streamlabs": {
            "Donation - Generic": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            },
            "Donation - Paypal": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            }
        },
        "Patreon": {
            "Pledge": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            }
        },
        "Twitch": {
            "Follow": {
                "valueInput": False,
                "quantityInput": False,
                "payloadInput": True
            },
            "Subscribe": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            },
            "Give Specific Gift Subscription": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            },
            "Give Random Gift Subscriptions": {
                "valueInput": True,
                "quantityInput": True,
                "payloadInput": True
            },
            "Bits": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            },
            "Host": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            },
            "Raid": {
                "valueInput": True,
                "quantityInput": False,
                "payloadInput": True
            }
        },
        "Youtube": {

        },
        "Mixer": {

        }
    }

    @staticmethod
    def GenerateTestEventArray(eventPlatform, eventType, value, special, payloadCount):
        primaryEvent = TestEventUtils._GenerateTestEvent(
            eventPlatform, eventType, value, special, payloadCount)
        testEventArray = [primaryEvent]

        # Twitch sends events for the giver and also each receiver.
        if eventPlatform == "Twitch" and eventType == "Give Random Gift Subscriptions":
           for i in range(special):
                childEvent = TestEventUtils._GenerateTestEvent(
                    eventPlatform, "Give Specific Gift Subscription", value, i+2, 1)
                testEventArray.append(childEvent)

        return testEventArray

    @staticmethod
    def _GenerateTestEvent(eventPlatform, eventType, value, special, payloadCount):
        eventTypeString = ""
        eventForString = ""
        eventMessageConstructor = None
        messageIsTypeList = True

        if eventPlatform == "Streamlabs":
            eventForString = "streamlabs"
            if eventType == "Donation - Generic":
                eventTypeString = "donation"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    return {
                        'name': usernameCamelCase,
                        'from': usernameCamelCase,
                        'amount': value,
                        'crate_item': None,
                        'message': 'Test donation',
                        'formatted_amount': '$' + "{:.2f}".format(value)
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            if eventType == "Donation - Paypal":
                eventTypeString = "donation"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    return {
                        'id': TestEventUtils.GenerateRandomDigits(8),
                        'name': usernameCamelCase,
                        'amount': value,
                        'formatted_amount': '$' + "{:.2f}".format(value),
                        'formattedAmount': '$' + "{:.2f}".format(value),
                        'message': 'Test donation',
                        'currency': 'USD',
                        'emotes': '',
                        'iconClassName': 'fab paypal',
                        'to': {'name': 'JDPlays'},
                        'from': usernameCamelCase,
                        'from_user_id': None,
                        'donation_currency': 'USD',
                        'source': 'paypal',
                        '_id': TestEventUtils.GenerateUuidNoHyphens()
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
        elif eventPlatform == "Patreon":
            eventForString = "patreon"
            if eventType == "Pledge":
                eventTypeString = "pledge"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    return {
                        'name': usernameCamelCase,
                        'from': usernameCamelCase,
                        'amount': value,
                        'formatted_amount': '$' + "{:.2f}".format(value)
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
        elif eventPlatform == "Twitch":
            eventForString = "twitch_account"
            if eventType == "Follow":
                eventTypeString = "follow"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    return {
                        'name': usernameCamelCase,
                        'from': usernameCamelCase
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Subscribe":
                eventTypeString = "subscription"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    usernameLowerCase = 'user' + str(iterator)
                    return {
                        'name': usernameLowerCase,
                        'from': usernameLowerCase,
                        'display_name': usernameCamelCase,
                        'from_display_name': usernameCamelCase,
                        'message': 'a test subscription',
                        'sub_plan': TestEventUtils.TwitchSubscriptionSubPlanValueToString(value),
                        'months': '2',
                        'streak_months': '2',
                        'gifter': None
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Give Specific Gift Subscription":
                eventTypeString = "subscription"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    giver = iterator + 1
                    if special != None and special != "":
                        iterator = special
                        giver = 1
                    receiverUsernameCamelCase = 'UsEr' + str(iterator)
                    receiverUsernameLowerCase = 'user' + str(iterator)
                    gifterUsernameLowerCase = 'user' + str(giver)
                    return {
                        'name': receiverUsernameLowerCase,
                        'from': receiverUsernameLowerCase,
                        'display_name': receiverUsernameCamelCase,
                        'from_display_name': receiverUsernameCamelCase,
                        'message': 'a test subscription',
                        'sub_plan': TestEventUtils.TwitchSubscriptionSubPlanValueToString(value),
                        'months': '2',
                        'streak_months': '2',
                        'gifter': gifterUsernameLowerCase
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Give Random Gift Subscriptions":
                eventTypeString = "subMysteryGift"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    usernameLowerCase = 'user' + str(iterator)
                    messageEventId = TestEventUtils.GenerateUuidNoHyphens()
                    return {
                        'sub_plan': TestEventUtils.TwitchSubscriptionSubPlanValueToString(value),
                        'sub_type': 'submysterygift',
                        'gifter': usernameLowerCase,
                        'gifter_display_name': usernameCamelCase,
                        'name': usernameCamelCase,
                        'amount': special,
                        '_id': messageEventId,
                        'event_id': messageEventId
                    }
                eventOptions = TestEventOptions()
                eventOptions.globalEventId = False
                eventOptions.eventDefaultAttributes = False
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Bits":
                eventTypeString = "bits"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    usernameCamelCase = 'UsEr' + str(iterator)
                    usernameLowerCase = 'user' + str(iterator)
                    return {
                        'name': usernameLowerCase,
                        'from': usernameLowerCase,
                        'display_name': usernameCamelCase,
                        'from_display_name': usernameCamelCase,
                        'amount': value,
                        'message': 'test bits'
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Host":
                # NOTE: NOT UPDATED WITH OTHER TWITCH CHANGES AS NO SAMPLE DATA: 2021-04-09
                eventTypeString = "host"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    messageEventId = TestEventUtils.GenerateUuid()
                    return {
                        'name': 'UsEr' + str(iterator),
                        'viewers': int(value),
                        'type': 'manual',
                        '_id': messageEventId,
                        'event_id': messageEventId
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor
            elif eventType == "Raid":
                # NOTE: NOT UPDATED WITH OTHER TWITCH CHANGES AS NO SAMPLE DATA: 2021-04-09
                eventTypeString = "raid"

                def EventMessageConstructor(value, special, iterator):
                    iterator += 1
                    messageEventId = TestEventUtils.GenerateUuid()
                    return {
                        'id': messageEventId,
                        'name': 'user' + str(iterator),
                        'display_name': 'UsEr' + str(iterator),
                        'raiders': int(value),
                        '_id': messageEventId,
                        'event_id': messageEventId
                    }
                eventOptions = TestEventOptions()
                eventMessageConstructor = EventMessageConstructor

        return TestEventUtils._ConstructTestEventDict(eventForString, eventTypeString, eventMessageConstructor, value, special, payloadCount, messageIsTypeList, eventOptions)

    @staticmethod
    def _ConstructTestEventDict(forString, typeString, messageConstructor, value, special, payloadCount, messageIsTypeList, eventOptions):
        eventDict = {
            "for": forString,
            "type": typeString
        }
        if eventOptions.globalEventId == None or eventOptions.globalEventId == True:
            eventDict["event_id"] = TestEventUtils.GenerateEventUuid()
        if messageIsTypeList:
            eventDict["message"] = []
            for i in range(payloadCount):
                messageEntry = messageConstructor(value, special, i)
                eventDict["message"].append(TestEventUtils._MakeTestEventMessageEntry(
                    messageEntry, forString, typeString, eventOptions))
        else:
            messageEntry = messageConstructor(value, special, 1)
            eventDict["message"] = TestEventUtils._MakeTestEventMessageEntry(
                messageEntry, forString, typeString, eventOptions)
        return eventDict

    @staticmethod
    def _MakeTestEventMessageEntry(messageEntry, forString, typeString, eventOptions):
        if eventOptions.eventDefaultAttributes == False:
            return messageEntry

        nowDateTime = DateTime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pastDateTime = (DateTime.datetime.now() -
                        DateTime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        messageEntry["type"] = typeString
        messageEntry["platform"] = forString
        messageEntry["created_at"] = pastDateTime

        hashString = typeString + ":" + messageEntry["name"]
        if "message" in messageEntry.keys():
            hashString += ":"
            if messageEntry["message"] != None:
                hashString += messageEntry["message"]
        if "amount" in messageEntry.keys():
            hashString += ":"
            if messageEntry["amount"] != None:
                hashString += "{:.0f}".format(messageEntry["amount"])
        messageEntry["hash"] = hashString

        messageEntry["uuid"] = TestEventUtils.GenerateUuid()
        messageEntry["read"] = False
        messageEntry["createdAt"] = str(nowDateTime)
        messageEntry["repeat"] = True
        messageEntry["_id"] = TestEventUtils.GenerateRandomAlphaDigits(13)
        messageEntry["priority"] = 10

        return messageEntry

    @staticmethod
    def GetAttribute(platformString, typeString, attributeName):
        return TestEventUtils._types[platformString][typeString][attributeName]

    @staticmethod
    def DoesAttributeExist(platformString, typeString, attributeName):
        if attributeName in TestEventUtils._types[platformString][typeString].keys():
            return True
        else:
            return False

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
    def GenerateUuidNoHyphens():
        return Uuid(Uuid4().hex).hex

    @staticmethod
    def GenerateEventUuid():
        return "evt" + Uuid(Uuid4().hex).hex

    @staticmethod
    def GenerateRandomDigits(count):
        number = ""
        for _ in range(count):
            number += str(Random.randint(0, 9))
        return number

    @staticmethod
    def GenerateRandomAlphaDigits(count):
        return ''.join(Random.choices(String.ascii_uppercase + String.digits, k=count))

    # Have to use as the values all come as string in JSON from streamlabs, but we auto convert anything number to a number. So the test event data needs to match this int/string data type.
    @staticmethod
    def TwitchSubscriptionSubPlanValueToString(value):
        if value == "Prime":
            return value
        else:
            return str(int(value))


class TestEventOptions:
    def __init__(self):
        self.globalEventId = True
        self.eventDefaultAttributes = True
