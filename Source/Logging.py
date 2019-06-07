import datetime as Datetime
import os as Os
import traceback as Traceback


class Logging():
    def __init__(self, state):
        self.State = state
        dateFormat = "%Y_%m_%d %H_%M_%S"
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime(dateFormat)
        logFolder = "Logs"
        if Os.path.isdir(logFolder):
            self._TidyUpOldLogFiles(
                logFolder, currentDT, state.Config.GetSetting("Logging DaysLogsToKeep"), dateFormat)
        else:
            Os.mkdir(logFolder)
        logFileName = "Log " + dtString + ".log"
        self.logFilePath = logFolder + "/" + logFileName
        self.debugLogFilePath = logFolder + "/Debug" + logFileName
        self.debugLogging = state.Config.GetSetting("Logging DebugLogging")

    def _TidyUpOldLogFiles(self, logFolder, currentDT, daysLogsToKeep, dateFormat):
        for name in Os.listdir(logFolder):
            if name[-3:] != "log":
                continue
            oldDateString = name[name.find(" ") + 1:-4]
            oldDate = Datetime.datetime.strptime(oldDateString, dateFormat)
            if abs((currentDT - oldDate).days) > daysLogsToKeep:
                Os.remove(logFolder + "/" + name)

    def Log(self, text):
        self.DebugLog(text)
        fileName = self.logFilePath
        with open(fileName, "a") as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def LogQuit(self, text):
        self.Log(text)
        exit()

    def DebugLog(self, text):
        if not self.debugLogging:
            return
        fileName = self.debugLogFilePath
        with open(fileName, "a") as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def TimestampText(self, text):
        currentDT = Datetime.datetime.now()
        dtString = currentDT.strftime("%H:%M:%S")
        return dtString + " : " + text

    def RecordException(self, ex, description):
        text = description + " - See logs for full details"
        stackTrace = Traceback.format_exc()
        try:
            self.State.RecordActivity(text)
        except:
            pass
        try:
            self.Log(stackTrace)
        except:
            pass
