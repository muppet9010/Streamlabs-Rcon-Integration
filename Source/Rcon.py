from mcrcon import MCRcon


class Rcon:
    def __init__(self, state):
        self.state = state
        self.serverAddress = self.state.config.GetSetting(
            "Rcon Server Address")
        self.serverPort = self.state.config.GetSetting("Rcon Server Port")
        self.serverPassword = self.state.config.GetSetting(
            "Rcon Server Password")
        self.testCommand = self.state.config.GetSetting("Rcon Test Command")

    def TestConnection(self):
        if self.state.config.GetSetting("Test Mode"):
            return True
        try:
            self.SendCommand(self.testCommand)
            return True
        except Exception as ex:
            self.state.logging.RecordException(ex, "Rcon server test failed")
            self.state.RecordActivity(
                self.state.translations.GetTranslation("Rcon TestErrorMessage") + str(ex))
            return False

    def SendCommand(self, commandString):
        if self.state.config.GetSetting("Test Mode"):
            self.state.RecordActivity(
                self.state.translations.GetTranslation("Rcon TestMode") + commandString)
            return ""
        with MCRcon(self.serverAddress, self.serverPassword, self.serverPort) as mcr:
            return mcr.command(commandString)
