import common
import updateProducts
import threading
import tkinter as tk
import tkinter.font as tkFont
import pusherWebsocket
import pollingDatabase



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


if __name__ == "__main__":
    
    common.setVar()
    pusherWebsocket.PusherWebsocket()

    window = tk.Tk()
    window.title("Table Order")
    window.geometry('400x400')

    ft = tkFont.Font(family='Fixdsys', size=20, weight=tkFont.BOLD)
    w = tk.Label(window, text="Start plugin.", font=ft).place(x=120, y=160)
    buttontext = tk.StringVar()
    buttontext.set('Start')
    b = tk.Button(window, textvariable=buttontext, font=(
        'Arial', 12), width=10, height=1, command=lambda: thread_it(b, buttontext))
    b.place(x=150, y=230)

    # need a button to sync stock
    syncStockButtonText = tk.StringVar()
    syncStockButtonText.set("update products")

    syncStockButton = tk.Button(
        window, textvariable=syncStockButtonText, font=(
            'Arial', 12), width=12, height=1, command=lambda: checkStock(syncStockButton, syncStockButtonText))
    syncStockButton.place(x=150, y=330)

    print("function initialization successful")
    window.mainloop()
