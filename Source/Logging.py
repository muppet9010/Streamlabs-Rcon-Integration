import datetime as Datetime


class Logging():
    def __init__(self, debugLogging=False):
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime("%Y_%m_%d %H_%M_%S")
        self.logFileName = "Log " + dtString + ".log"
        self.debugLogFileName = "Debug " + self.logFileName
        self.debugLogging = debugLogging

    def Log(self, text):
        self.DebugLog(text)
        fileName = self.logFileName
        with open(fileName, "a") as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def DebugLog(self, text):
        if not self.debugLogging:
            return
        fileName = self.debugLogFileName
        with open(fileName, "a") as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def TimestampText(self, text):
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime("%H:%M:%S")
        return dtString + " : " + text
