from Logging import Logging
from Obs import Obs
from Gui import Gui, GuiWindow
from Currency import Currency


class State():
    pass


State = State()
State.Logging = Logging(True)
State.Currency = Currency(State)
State.Obs = Obs(State)
State.GuiWindow = GuiWindow(State)
State.Gui = State.GuiWindow.Gui
State.Obs.UpdateReferences()
State.Logging.DebugLog("App Started")
State.Gui.mainloop()
