import tkinter as TK


class GuiWindow():
    def __init__(self, state):
        root = TK.Tk()
        root.minsize(500, 400)
        self.State = state
        self.Gui = Gui(state, master=root)


class Gui(TK.Frame):
    def __init__(self, state, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.State = state
        self.Translations = state.Translations

    def CreateWidgets(self):
        self._CreateRunningBar(self.master)
        self._CreateActivityLog(self.master)
        self._CreateBottomBar(self.master)

    def _CreateRunningBar(self, parent):
        runningContainer = TK.Frame(parent)
        runningContainer.pack(fill=TK.X, side=TK.TOP)

        self.statusText = TK.StringVar()
        self.State.UpdateStatus()
        statusLabel = TK.Label(
            runningContainer, textvariable=self.statusText, height=1, width=30)
        statusLabel.pack(side=TK.LEFT)

        # TODO this doesn't make a list of multiple items...
        self.selectedProfileName = TK.StringVar()
        self.sortedProfileNames = sorted(list(
            self.State.Profiles.profiles.keys()))
        configProfileDefault = self.State.Config.GetSetting("Profile Default")
        if configProfileDefault != "" and configProfileDefault in self.sortedProfileNames:
            self.selectedProfileName.set(configProfileDefault)
        else:
            self.selectedProfileName.set(
                self.Translations.currentTexts["Gui SelectProfile"])
        profileList = TK.OptionMenu(
            runningContainer, self.selectedProfileName, self.sortedProfileNames)
        profileList.pack(side=TK.LEFT)

        startButton = TK.Button(runningContainer,
                                text=self.Translations.currentTexts["Gui StartButton"], command=self.State.OnStartButtonHandler)
        startButton.pack(side=TK.LEFT)

        stopButton = TK.Button(
            runningContainer, text=self.Translations.currentTexts["Gui StopButton"], command=self.State.OnStopButtonHandler)
        stopButton.pack(side=TK.LEFT)

    def _CreateActivityLog(self, parent):
        titleFrame = TK.LabelFrame(
            parent, text=self.Translations.currentTexts["Gui ActivityLogTitle"])
        titleFrame.pack(fill=TK.BOTH, expand=True, side=TK.TOP, padx=3, pady=3)
        yScroll = TK.Scrollbar(titleFrame, orient=TK.VERTICAL)
        yScroll.pack(fill=TK.Y, expand=True, side=TK.RIGHT)
        self.activityLogText = TK.Text(
            titleFrame, height=5, wrap=TK.WORD, yscrollcommand=yScroll.set, state=TK.DISABLED)
        self.activityLogText.pack(fill=TK.BOTH, expand=True, side=TK.LEFT)

    def _CreateBottomBar(self, parent):
        self.bottomBarContainer = TK.Frame(parent)
        self.bottomBarContainer.pack(fill=TK.X, side=TK.TOP)

        quitButton = TK.Button(self.bottomBarContainer, text=self.Translations.currentTexts["Gui QuitButton"], fg="red",
                               command=self.State.OnQuitButtonHandler)
        quitButton.pack(side=TK.LEFT)

    def UpdateStatusText(self, text):
        self.statusText.set(text)

    def AddToActivityLog(self, text):
        self.activityLogText.configure(state="normal")
        self.activityLogText.insert(
            1.0, self.State.Logging.TimestampText(text) + "\n")
        self.activityLogText.configure(state="disabled")
