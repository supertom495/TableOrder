import tkinter as tk


root = tk.Tk() 
# top = tk.Toplevel(root) 
root.overrideredirect(1) #removes border but undesirably from taskbar too (usually for non toplevel windows) 
root.attributes("-alpha",0.0) 

#toplevel follows root taskbar events (minimize, restore) 
# def onRootIconify(event): top.withdraw() 
# root.bind("<Unmap>", onRootIconify) 
# def onRootDeiconify(event): top.deiconify() 
# root.bind("<Map>", onRootDeiconify) 

# window = tk.Frame(master=top) 

printQRCodeButtonText = tk.StringVar()
printQRCodeButtonText.set("get QRCode")
printQRCodeButton = tk.Button(root, textvariable=printQRCodeButtonText, font=('Arial', 12),width=10, height=1)
printQRCodeButton.place(x=0, y=0)

root.mainloop() 