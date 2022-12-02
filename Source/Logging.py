import datetime as Datetime
import os as Os
import traceback as Traceback


class Logging():
    def __init__(self, state):
        self.state = state
        dateFormat = "%Y_%m_%d %H_%M_%S"
        currentDateTime = Datetime.datetime.now()
        dateTimeString = currentDateTime.strftime(dateFormat)
        logFolder = "Logs"
        if Os.path.isdir(logFolder):
            self._TidyUpOldLogFiles(logFolder, currentDateTime, state.config.GetSetting("Logging DaysLogsToKeep"), dateFormat)
        else:
            Os.mkdir(logFolder)
        logFileName = "Log " + dateTimeString + ".log"
        self.logFilePath = logFolder + "/" + logFileName
        self.debugLogFilePath = logFolder + "/Debug" + logFileName
        self.debugLogging = state.config.GetSetting("Logging DebugLogging")
        self.Log("Logging Started - " + self.state.version)

    def _TidyUpOldLogFiles(self, logFolder, currentDateTime, daysLogsToKeep, dateFormat):
        for name in Os.listdir(logFolder):
            if name[-3:] != "log":
                continue
            oldDateString = name[name.find(" ") + 1:-4]
            oldDate = Datetime.datetime.strptime(oldDateString, dateFormat)
            if abs((currentDateTime - oldDate).days) > daysLogsToKeep:
                Os.remove(logFolder + "/" + name)

    def Log(self, text):
        self.DebugLog(text)
        fileName = self.logFilePath
        with open(fileName, "a", encoding='utf-8') as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def LogQuit(self, text):
        self.Log(text)
        exit()

    def DebugLog(self, text):
        if not self.debugLogging:
            return
        fileName = self.debugLogFilePath
        with open(fileName, "a", encoding='utf-8') as file:
            file.write(self.TimestampText(text) + "\n")
        file.closed

    def TimestampText(self, text):
        currentDateTime = Datetime.datetime.now()
        dateTimeString = currentDateTime.strftime("%H:%M:%S")
        return dateTimeString + " : " + text

    def RecordException(self, ex, description):
        text = description + " - See logs for full details"
        stackTrace = Traceback.format_exc()
        try:
            self.state.RecordActivity(text)
        except:
            pass
        try:
            self.Log(stackTrace)
        except:
            pass
