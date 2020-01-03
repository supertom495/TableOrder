import tkinter as tk 
import tkinter.messagebox as msg 
import ctypes 

MB_OK = 0x0 
ICON_STOP = 0x10 


root = tk.Tk() 

# non-transient app-wide version 
native_showerror = lambda: ctypes.windll.user32.MessageBoxW(0, "Oh please work oh please work oh please", 
                  "Show up on taskbar! ... *sigh", MB_OK | ICON_STOP) 
# transient version if we pass hWnd of the root window 
native_showerror_transient = lambda: ctypes.windll.user32.MessageBoxW(root.winfo_id(), 
                     "Oh please work oh please work oh please", 
                     "Show up on taskbar! ... *sigh", MB_OK | ICON_STOP) 

if root._windowingsystem == 'win32': 
    # windows showerror 
    root.update_idletasks() 
    native_showerror() 

else: 
    # non-windows showerror 
    msg.showerror("Oh please work oh please work oh please", "Show up on taskbar! ... *sigh") 

root.mainloop() 