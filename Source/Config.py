import json as Json
import os as Os


class Config():
    def __init__(self, state):
        self.state = state
        self.fileName = "config.json"
        self.settings = {}
        if Os.path.isfile(self.fileName):
            with open(self.fileName, "r") as file:
                data = Json.load(file)
            file.closed
            self.settings = data
        self.settingsMissing = []
        self._PopulateMissingConfigDefaults()

    def _PopulateMissingConfigDefaults(self):
        defaults = {
            "Logging DaysLogsToKeep": 7,
            "Logging DebugLogging": True,
            "Currency ApiLayerAccessKey": "",
            "Streamlabs SocketApiToken": "",
            "Profile Default": "",
            "Factorio PlayerName": "",
            "Rcon Server Address": "",
            "Rcon Server Port": 25575,
            "Rcon Server Password": ""
        }
        for name, value in defaults.items():
            if not name in self.settings:
                self.settings[name] = value
                self.settingsMissing.append(name)

    def LogMissingSettings(self):
        for name in self.settingsMissing:
            self.state.logging.Log(
                "Config key missing, using default: " + name)

    def GetSetting(self, name):
        return self.settings[name]
