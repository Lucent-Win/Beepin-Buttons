from beepin import beepin
from pynput import keyboard # GNU Lesser General Public License v3.0

bpr = beepin()

listener = keyboard.Listener(on_press=bpr.on_press,on_release= bpr.on_release)
listener.start()

bpr.root.protocol("WM_DELETE_WINDOW", bpr.close_window)
bpr.root.mainloop()
	

	