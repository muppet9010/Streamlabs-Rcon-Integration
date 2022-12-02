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

    def Setup(self):
        self._CreateRunningBar(self.master)
        self._CreateActivityLog(self.master)
        self._CreateBottomBar(self.master)
        self.OnStopped()

    def _CreateRunningBar(self, parent):
        runningContainer = TK.Frame(parent)
        runningContainer.pack(fill=TK.X, side=TK.TOP)

        self.statusText = TK.StringVar()
        self.state.UpdateStatus()
        statusLabel = TK.Label(runningContainer, textvariable=self.statusText, height=1, width=30)
        statusLabel.pack(side=TK.LEFT)

        self.selectedProfileName = TK.StringVar()
        sortedProfileNames = sorted(list(self.state.profiles.profiles.keys()))
        configProfileDefault = self.state.config.GetSetting("Profile Default")
        if configProfileDefault != "" and configProfileDefault in sortedProfileNames:
            self.selectedProfileName.set(configProfileDefault)
        else:
            self.selectedProfileName.set(self.translations.GetTranslation("Gui SelectProfile"))
        self.profileList = TK.OptionMenu(runningContainer, self.selectedProfileName, *sortedProfileNames)
        self.profileList.pack(side=TK.LEFT)

        self.startButton = TK.Button(runningContainer,text=self.translations.GetTranslation("Gui StartButton"), command=self.state.OnStartButtonHandler)
        self.startButton.pack(side=TK.LEFT)

        self.stopButton = TK.Button(runningContainer, text=self.translations.GetTranslation("Gui StopButton"), command=self.state.OnStopButtonHandler)
        self.stopButton.pack(side=TK.LEFT)

    def _CreateActivityLog(self, parent):
        titleFrame = TK.LabelFrame(parent, text=self.translations.GetTranslation("Gui ActivityLogTitle"))
        titleFrame.pack(fill=TK.BOTH, expand=True, side=TK.TOP, padx=3, pady=3)
        yScroll = TK.Scrollbar(titleFrame, orient=TK.VERTICAL)
        yScroll.pack(fill=TK.Y, expand=False, side=TK.RIGHT)
        self.activityLogText = TK.Text(titleFrame, height=5, wrap=TK.WORD, yscrollcommand=yScroll.set, state=TK.DISABLED)
        self.activityLogText.pack(fill=TK.BOTH, expand=True, side=TK.LEFT)

    def _CreateBottomBar(self, parent):
        bottomBarContainer = TK.Frame(parent)
        bottomBarContainer.pack(fill=TK.X, side=TK.TOP)

        self.selectedTestEventPlatform = TK.StringVar()
        self.selectedTestEventPlatform.trace_variable(TK.W, self.OnTestEventPlatformChanged)
        orderedTestEventPlatforms = self.state.testEventUtils.GetPlatforms()
        self.testEventPlatformList = TK.OptionMenu(bottomBarContainer, self.selectedTestEventPlatform, *orderedTestEventPlatforms)
        self.testEventPlatformList.pack(side=TK.LEFT)

        self.selectedTestEventType = TK.StringVar()
        self.selectedTestEventType.trace_variable(TK.W, self.OnTestEventTypeChanged)
        self.orderedTestEventTypes = [""]
        self.testEventTypeList = TK.OptionMenu(bottomBarContainer, self.selectedTestEventType, *self.orderedTestEventTypes)
        self.testEventTypeList.pack(side=TK.LEFT)

        self.testEventValueLabel = TK.Label(bottomBarContainer, text="event value:")
        self.testEventValueLabel.pack(side=TK.LEFT)
        self.testEventValue = TK.StringVar()
        self.testEventValueInput = TK.Entry(bottomBarContainer, textvariable=self.testEventValue, width=10)
        self.testEventValueInput.pack(side=TK.LEFT)

        self.testEventQuantityLabel = TK.Label(bottomBarContainer, text="quantity:")
        self.testEventQuantityLabel.pack(side=TK.LEFT)
        self.testEventQuantity = TK.StringVar()
        self.testEventQuantityInput = TK.Entry(bottomBarContainer, textvariable=self.testEventQuantity, width=10)
        self.testEventQuantityInput.pack(side=TK.LEFT)

        self.testEventPayloadCountLabel = TK.Label(bottomBarContainer, text="payload count:")
        self.testEventPayloadCountLabel.pack(side=TK.LEFT)
        self.testEventPayloadCount = TK.StringVar()
        self.testEventPayloadCount.set("1")
        self.testEventPayloadCountInput = TK.Entry(bottomBarContainer, textvariable=self.testEventPayloadCount, width=10)
        self.testEventPayloadCountInput.pack(side=TK.LEFT)

        self.testEventButton = TK.Button(bottomBarContainer, text=self.translations.GetTranslation("Gui TestEventButton"), command=self.state.OnTestEventButtonHandler)
        self.testEventButton.pack(side=TK.LEFT)

        self.selectedTestEventPlatform.set(self.translations.GetTranslation("Gui SelectTestEventPlatform"))
        self.selectedTestEventType.set(self.translations.GetTranslation("Gui SelectTestEventType"))

        self.testEventPlatformList.config(state=TK.DISABLED)
        self.testEventTypeList.config(state=TK.DISABLED)
        self.testEventValueLabel.config(state=TK.DISABLED)
        self.testEventValueInput.config(state=TK.DISABLED)
        self.testEventQuantityLabel.config(state=TK.DISABLED)
        self.testEventQuantityInput.config(state=TK.DISABLED)
        self.testEventPayloadCountLabel.config(state=TK.DISABLED)
        self.testEventPayloadCountInput.config(state=TK.DISABLED)
        self.testEventButton.config(state=TK.DISABLED)

    def UpdateStatusText(self, text):
        self.statusText.set(text)

    def AddToActivityLog(self, text):
        self.activityLogText.configure(state=TK.NORMAL)
        self.activityLogText.insert(1.0, self.state.logging.TimestampText(text) + "\n")
        self.activityLogText.configure(state=TK.DISABLED)

    def OnStarted(self):
        self.startButton.config(state=TK.DISABLED)
        self.profileList.config(state=TK.DISABLED)
        self.stopButton.config(state=TK.NORMAL)
        self.testEventPlatformList.config(state=TK.NORMAL)

    def OnStopped(self):
        self.startButton.config(state=TK.NORMAL)
        self.profileList.config(state=TK.NORMAL)
        self.stopButton.config(state=TK.DISABLED)
        self.testEventPlatformList.config(state=TK.DISABLED)

    def OnTestEventPlatformChanged(self, *args):
        self.testEventTypeList["menu"].delete(0, TK.END)
        orderedTestEventTypes = []
        if self.selectedTestEventPlatform.get() != self.translations.GetTranslation("Gui SelectTestEventPlatform"):
            orderedTestEventTypes = self.state.testEventUtils.GetPlatformTypes(self.selectedTestEventPlatform.get())
        for testEventType in orderedTestEventTypes:
            self.testEventTypeList["menu"].add_command(label=testEventType, command=TK._setit(self.selectedTestEventType, testEventType))
        self.selectedTestEventType.set(self.translations.GetTranslation("Gui SelectTestEventType"))
        self.testEventTypeList.config(state=TK.NORMAL)
        self.testEventValueLabel.config(state=TK.DISABLED)
        self.testEventValueInput.config(state=TK.DISABLED)
        self.testEventQuantityLabel.config(state=TK.DISABLED)
        self.testEventQuantityInput.config(state=TK.DISABLED)
        self.testEventPayloadCountLabel.config(state=TK.DISABLED)
        self.testEventPayloadCountInput.config(state=TK.DISABLED)
        self.testEventButton.config(state=TK.DISABLED)

    def OnTestEventTypeChanged(self, *args):
        amountEnabled = False
        quantityEnabled = False
        payloadCountEnabled = False
        if self.selectedTestEventType.get() != self.translations.GetTranslation("Gui SelectTestEventType"):
            amountEnabled = self.state.testEventUtils.GetAttribute(self.selectedTestEventPlatform.get(), self.selectedTestEventType.get(), "valueInput")
            quantityEnabled = self.state.testEventUtils.GetAttribute(self.selectedTestEventPlatform.get(), self.selectedTestEventType.get(), "quantityInput")
            payloadCountEnabled = self.state.testEventUtils.GetAttribute(self.selectedTestEventPlatform.get(), self.selectedTestEventType.get(), "payloadInput")
        if amountEnabled:
            self.testEventValueLabel.config(state=TK.NORMAL)
            self.testEventValueInput.config(state=TK.NORMAL)
        else:
            self.testEventValueLabel.config(state=TK.DISABLED)
            self.testEventValueInput.config(state=TK.DISABLED)
        if quantityEnabled:
            self.testEventQuantityLabel.config(state=TK.NORMAL)
            self.testEventQuantityInput.config(state=TK.NORMAL)
        else:
            self.testEventQuantityLabel.config(state=TK.DISABLED)
            self.testEventQuantityInput.config(state=TK.DISABLED)
        if payloadCountEnabled:
            self.testEventPayloadCountLabel.config(state=TK.NORMAL)
            self.testEventPayloadCountInput.config(state=TK.NORMAL)
        else:
            self.testEventPayloadCountLabel.config(state=TK.DISABLED)
            self.testEventPayloadCountInput.config(state=TK.DISABLED)
        self.testEventButton.config(state=TK.NORMAL)
