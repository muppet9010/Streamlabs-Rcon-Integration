import json as Json
import os as Os


class Config():
    def __init__(self, state):
        self.state = state
        self._fileName = "config.json"
        self._settings = {}
        if Os.path.isfile(self._fileName):
            with open(self._fileName, "r", encoding='utf-8') as file:
                data = Json.load(file)
            file.closed
            self._settings = data
        self._settingsMissing = []
        self._PopulateMissingConfigDefaults()

    def _PopulateMissingConfigDefaults(self):
        defaults = {
            "Logging DaysLogsToKeep": 7,
            "Logging DebugLogging": True,
            "Currency ApiLayerAccessKey": "",
            "Streamlabs SocketApiToken": "",
            "Profile Default": "",
            "Rcon Server Address": "",
            "Rcon Server Port": 25575,
            "Rcon Server Password": "",
            "Rcon Test Command": "/version",
            "Rcon No Commands": False
        }
        for name, value in defaults.items():
            if not name in self._settings:
                self._settings[name] = value
                self._settingsMissing.append(name)

    def LogMissingSettings(self):
        for name in self._settingsMissing:
            self.state.logging.Log(
                "Config key missing, using default: " + name)

    def GetSetting(self, name):
        return self._settings[name]
