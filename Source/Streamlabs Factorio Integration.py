from StreamlabsClass import Streamlabs
#import Streamlabs as obs
from GUI import *

obs = Streamlabs()
root = tk.Tk()
app = Application(obs, master=root)
app.mainloop()
