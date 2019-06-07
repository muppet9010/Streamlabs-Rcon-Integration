from mcrcon import MCRcon


class Rcon:
    def __init__(self, state):
        self.State = state
        self.serverAddress = self.State.Config.GetSetting(
            "Rcon Server Address")
        self.serverPort = self.State.Config.GetSetting("Rcon Server Port")
        self.serverPassword = self.State.Config.GetSetting(
            "Rcon Server Password")

    def TestConnection(self):
        try:
            self.SendCommand('/version')
            return True
        except Exception as ex:
            self.State.Logging.RecordException(ex, "Rcon server test failed")
            self.State.RecordActivity(str(ex))
            return False

    def SendCommand(self, commandString):
        with MCRcon(self.serverAddress, self.serverPassword, self.serverPort) as mcr:
            mcr.command(commandString)
