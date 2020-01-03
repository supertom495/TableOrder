import common
import updateProducts
import threading
import tkinter as tk
import tkinter.font as tkFont
import pusherWebsocket
import pollingDatabase
import qrCode
import api
import json
import posOperation

def thread_it(button, buttontext):
    #     global buttontext
    buttontext.set("Working")
    button.config(state="disabled")
    button.update()
    t = threading.Thread(target=pollingDatabase.MyRun)
    t.setDaemon(True)
    t.start()


def checkStock(button, buttontext):
    buttontext.set("Updating")
    button.config(state="disabled")
    button.update()

    updateProducts.updateProducts()

    buttontext.set("update stock")
    button.config(state="active")
    button.update()

def getQrCode():
    t = threading.Thread(target=qrCode.getQrCode)
    t.setDaemon(True)
    t.start()


def loadKeyboardList():
    keyboards = api.listKeyboard()
    keyboards = json.loads(keyboards.text)['keyboards']
    sortedKeyboards = sorted(keyboards, key=lambda k: k['inactive']) 
    kb = [keyboard['kb_name'] for keyboard in sortedKeyboards]
    return kb


if __name__ == "__main__":
    
    common.setVar()
    common.setUpTable()
    
    pusherWebsocket.PusherWebsocket()

    # set up window widget
    # root = tk.Tk() 
    # top = tk.Toplevel(root) 
    # top.overrideredirect(1) #removes border but undesirably from taskbar too (usually for non toplevel windows) 
    # root.attributes("-alpha",0.0) 

    # #toplevel follows root taskbar events (minimize, restore) 
    # def onRootIconify(event): top.withdraw() 
    # root.bind("<Unmap>", onRootIconify) 
    # def onRootDeiconify(event): top.deiconify() 
    # root.bind("<Map>", onRootDeiconify) 

    # window = tk.Frame(master=top) 

    
    window = tk.Tk()
    # window.overrideredirect(1)
    window.title("Table Order")
    window.geometry('400x400')

    # main process button
    ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
    w = tk.Label(window, text="Start plugin.", font=ft).place(x=120, y=60)
    buttontext = tk.StringVar()
    buttontext.set('Start')
    b = tk.Button(window, textvariable=buttontext, font=(
        'Arial', 12), width=10, height=1, command=lambda: thread_it(b, buttontext))
    b.place(x=150, y=130)

    # need a button to sync stock
    syncStockButtonText = tk.StringVar()
    syncStockButtonText.set("update products")

    syncStockButton = tk.Button(
        window, textvariable=syncStockButtonText, font=(
            'Arial', 12), width=12, height=1, command=lambda: checkStock(syncStockButton, syncStockButtonText))
    syncStockButton.place(x=150, y=230)


    # select activate keyboard
    def ok():
        keyboardId = posOperation.getKeyboardByKeyboardName(variable.get())[0][0]
        api.activateKeyboard(keyboardId)
        print ("value is:" + variable.get())

    OPTIONS = loadKeyboardList()
    variable = tk.StringVar()
    variable.set(OPTIONS[0]) # default value
    w = tk.OptionMenu(window, variable, *OPTIONS)
    w.place(x=60, y=300)
    selectKeyboardButton = tk.Button(window, text="OK", command=ok)
    selectKeyboardButton.place(x=123, y=303)



    print("function initialization successful")
    window.mainloop()
