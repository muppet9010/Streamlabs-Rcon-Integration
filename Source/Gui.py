import tkinter as TK


class GuiWindow():
    def __init__(self, state):
        root = TK.Tk()
        root.title("Streamlabs Rcon Integration - " + state.version)
        root.minsize(500, 200)
        root.geometry("1000x400")
        root.protocol("WM_DELETE_WINDOW", state.OnQuitButtonHandler)
        self.state = state
        self.gui = Gui(state, master=root)


class Gui(TK.Frame):
    def __init__(self, state, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.state = state
        self.translations = state.translations

    def CreateWidgets(self):
        self._CreateRunningBar(self.master)
        self._CreateActivityLog(self.master)
        # self._CreateBottomBar(self.master) # Don't bother with for just a quit button

    def _CreateRunningBar(self, parent):
        runningContainer = TK.Frame(parent)
        runningContainer.pack(fill=TK.X, side=TK.TOP)

        self.statusText = TK.StringVar()
        self.state.UpdateStatus()
        statusLabel = TK.Label(
            runningContainer, textvariable=self.statusText, height=1, width=30)
        statusLabel.pack(side=TK.LEFT)

        self.selectedProfileName = TK.StringVar()
        self.sortedProfileNames = sorted(list(
            self.state.profiles.profiles.keys()))
        configProfileDefault = self.state.config.GetSetting("Profile Default")
        if configProfileDefault != "" and configProfileDefault in self.sortedProfileNames:
            self.selectedProfileName.set(configProfileDefault)
        else:
            self.selectedProfileName.set(
                self.translations.GetTranslation("Gui SelectProfile"))
        self.profileList = TK.OptionMenu(
            runningContainer, self.selectedProfileName, *self.sortedProfileNames)
        self.profileList.pack(side=TK.LEFT)

        self.startButton = TK.Button(runningContainer,
                                     text=self.translations.GetTranslation("Gui StartButton"), command=self.state.OnStartButtonHandler)
        self.startButton.pack(side=TK.LEFT)

        self.stopButton = TK.Button(
            runningContainer, text=self.translations.GetTranslation("Gui StopButton"), command=self.state.OnStopButtonHandler)
        self.stopButton.pack(side=TK.LEFT)

        self.OnStopped()

    def _CreateActivityLog(self, parent):
        titleFrame = TK.LabelFrame(
            parent, text=self.translations.GetTranslation("Gui ActivityLogTitle"))
        titleFrame.pack(fill=TK.BOTH, expand=True, side=TK.TOP, padx=3, pady=3)
        yScroll = TK.Scrollbar(titleFrame, orient=TK.VERTICAL)
        yScroll.pack(fill=TK.Y, expand=False, side=TK.RIGHT)
        self.activityLogText = TK.Text(
            titleFrame, height=5, wrap=TK.WORD, yscrollcommand=yScroll.set, state=TK.DISABLED)
        self.activityLogText.pack(fill=TK.BOTH, expand=True, side=TK.LEFT)

    def _CreateBottomBar(self, parent):
        self.bottomBarContainer = TK.Frame(parent)
        self.bottomBarContainer.pack(fill=TK.X, side=TK.TOP)

        quitButton = TK.Button(self.bottomBarContainer, text=self.translations.GetTranslation("Gui QuitButton"), fg="red",
                               command=self.state.OnQuitButtonHandler)
        quitButton.pack(side=TK.LEFT)

    def UpdateStatusText(self, text):
        self.statusText.set(text)

    def AddToActivityLog(self, text):
        self.activityLogText.configure(state=TK.NORMAL)
        self.activityLogText.insert(
            1.0, self.state.logging.TimestampText(text) + "\n")
        self.activityLogText.configure(state=TK.DISABLED)

    def OnStarted(self):
        self.startButton.config(state=TK.DISABLED)
        self.profileList.config(state=TK.DISABLED)
        self.stopButton.config(state=TK.NORMAL)

    def OnStopped(self):
        self.startButton.config(state=TK.NORMAL)
        self.profileList.config(state=TK.NORMAL)
        self.stopButton.config(state=TK.DISABLED)
