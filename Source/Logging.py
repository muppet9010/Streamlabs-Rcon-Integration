import datetime as Datetime


class Logging():
    debugLogging = True

    @staticmethod
    def Setup():
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime("%Y_%m_%d %H_%M_%S")
        Logging.logFileName = "Log " + dtString + ".log"
        Logging.debugLogFileName = "Debug " + Logging.logFileName

    @staticmethod
    def Log(text):
        Logging.DebugLog(text)
        fileName = Logging.logFileName
        with open(fileName, "a") as file:
            file.write(Logging.TimestampText(text) + "\n")
        file.closed

    @staticmethod
    def DebugLog(text):
        if not Logging.debugLogging:
            return
        fileName = Logging.debugLogFileName
        with open(fileName, "a") as file:
            file.write(Logging.TimestampText(text) + "\n")
        file.closed

    @staticmethod
    def TimestampText(text):
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime("%H:%M:%S")
        return dtString + " : " + text


Logging.Setup()
