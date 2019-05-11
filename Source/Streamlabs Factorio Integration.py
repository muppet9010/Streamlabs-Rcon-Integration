from Logging import Logging
from Obs import Obs
from Gui import Gui, GuiWindow


Obs = Obs(Logging)
Gui = GuiWindow(Logging, Obs).gui
Obs.UpdateGuiReference(Gui)
Logging.DebugLog("App Started")
Gui.mainloop()
