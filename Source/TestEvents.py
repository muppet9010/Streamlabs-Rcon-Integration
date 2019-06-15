class TestEvents:
    def __init__(self, state):
        self.state = state

    def GenerateTestEvent(self, eventPlatform, eventType, amount):
        if eventPlatform == "Twitch":
            if eventType == "Subscribe":
                return {
                    'type': 'subscription',
                    'message': [
                        {
                            'name': 'user',
                            'display_name': 'UsEr',
                            'months': '4',
                            'message': 'a test subscription',
                            'emotes': '1:25-26',
                            'sub_plan': '1000',
                            'sub_plan_name': 'Channel\\sSubscription\\s(streamer)',
                            'sub_type': 'resub',
                            'gifter': None,
                            'subscriber_twitch_id': '12345678',
                            'streak_months': '2',
                            '_id': 'f5b4860c38313d4564d277ccc521a4a0',
                            'event_id': 'f5b4860c38313d4564d277ccc521a4a0'
                        }
                    ],
                    'for': 'twitch_account'
                }


class TestEventTypes:
    platforms = {
        "Streamlabs": {
            "Donation": {
                "valueInput": True
            }
        },
        "Patreon": {
            "Pledge": {
                "valueInput": True
            }
        },
        "Twitch": {
            "Follow": {
                "valueInput": False
            },
            "Subscribe": {
                "valueInput": False
            },
            "Receive Gift Subscription": {
                "valueInput": False
            },
            "Give Subscription Gifts": {
                "valueInput": True
            },
            "Host": {
                "valueInput": True
            },
            "Raid": {
                "valueInput": True
            }
        },
        "Youtube": {

        },
        "Mixer": {

        }
    }
