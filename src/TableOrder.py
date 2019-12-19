import json
import pymssql
import time
import common
import posOperation
import updateStock
import threading
import tkinter as tk
import tkinter.font as tkFont
import api
import websocket
import pusherWebsocket
import pollingDatabase
from datetime import datetime


def thread_it(button, buttontext):
    #     global buttontext
    buttontext.set("Working")
    button.config(state="disabled")
    button.update()
    t = threading.Thread(target=pollingDatabase.MyRun)
    t.setDaemon(True)
    t.start()


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
    syncStockButtonText.set("update stock")

    syncStockButton = tk.Button(
        window, textvariable=syncStockButtonText, font=(
            'Arial', 12), width=10, height=1, command=lambda: updateStock.checkStock(syncStockButton, syncStockButtonText))
    syncStockButton.place(x=150, y=330)

    print("function initialization successful")
    window.mainloop()
