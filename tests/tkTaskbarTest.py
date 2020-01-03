import tkinter as tk

root = tk.Tk() 
root.geometry("400x400")
root.overrideredirect(1)
root.resizable(False, False)
root.columnconfigure(0, weight=1)
# root.iconbitmap(default='./Colors/small_red.ico')


def close():
    root.destroy()

def minimizeWindow():
    root.withdraw()
    root.overrideredirect(False)
    root.iconify()

def check_map(event): # apply override on deiconify.
    if str(event) == "<Map event>":
        root.overrideredirect(1)
        print ('Deiconified', event)
    else:
        print ('Iconified', event)

bar_frame = tk.Frame(root)
bar_frame.grid(row=0, column=0, sticky="ew")
bar_frame.columnconfigure(0, weight=1)
# icon = tk.PhotoImage(file='./Colors/small_red.gif')
# This appears to have the same results so not sure what the difference is from iconbitmap.
# root.tk.call('wm', 'iconphoto', root._w, icon) 

tk.Button(bar_frame, text='x', command=close).grid(row=0, column=1)
tk.Button(bar_frame, text='-', command=minimizeWindow).grid(row=0, column=2)

root.bind('<Map>', check_map) # added bindings to pass windows status to function
root.bind('<Unmap>', check_map)

root.mainloop()