import json as Json
import os as Os
import requests as Requests
import datetime as Datetime


class Currency():
    rates = {}
    cacheFileName = "CurrencyDataCache.json"

    @staticmethod
    def GetRates(logging, gui):
        Currency.logging = logging
        Currency.gui = gui
        if len(Currency.rates) > 0:
            return True
        if Os.path.isfile("./" + Currency.cacheFileName):
            Currency.logging.DebugLog(
                "Trying to get currancy rates from cache file")
            with open(Currency.cacheFileName, "r") as file:
                data = Json.load(file)
            file.closed
            cacheDateTime = Datetime.date.fromtimestamp(data["timestamp"])
            currentDateTime = Datetime.date.fromtimestamp(
                Datetime.datetime.utcnow().timestamp())
            if currentDateTime <= cacheDateTime:
                for name, rate in data["quotes"].items():
                    currency = name[3:]
                    Currency.rates[currency] = rate
                if len(Currency.rates) > 0:
                    Currency.logging.DebugLog(
                        "Got currency rates from cache file")
                    return True

        Currency._SourceRateData()
        if len(Currency.rates) > 0:
            Currency.logging.DebugLog("Got currency rates from website")
            return True
        else:
            Currency.logging.DebugLog(
                "Failed to get any currency rates from website")
            return False

    @staticmethod
    def _SourceRateData():
        Currency.logging.DebugLog("Sourcing currency rates from website")
        url = "http://www.apilayer.net/api/live"
        params = {"access_key": "bf92c65503f807f9abd65b83d39c2c6c"}
        request = Requests.get(url=url, params=params)
        response = request.json()
        if not response["success"]:
            Currency.gui.AddToActivityLog(
                "ERROR: Can't get currency conversion data")
            return False
        with open(Currency.cacheFileName, "w") as file:
            file.write(Json.dumps(response))
        file.closed
        for name, rate in response["quotes"].items():
            currency = name[3:]
            Currency.rates[currency] = rate

    @staticmethod
    def GetNormalisedValue(currency, amount):
        return amount / Currency.rates[currency]
