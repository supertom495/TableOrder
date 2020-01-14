import common
import updateProducts
import threading
import pusherWebsocket
import pollingDatabase
import api
import json
import posOperation
import wx
import wx.adv
import sys


def loadKeyboardList():
    keyboards = api.listKeyboard()
    keyboards = json.loads(keyboards.text)['keyboards']
    sortedKeyboards = sorted(keyboards, key=lambda k: k['inactive'])
    kb = [keyboard['kb_name'] for keyboard in sortedKeyboards]
    return kb


TRAY_TOOLTIP = 'Table Order'
TRAY_ICON = "./API_data/icon.png"
IS_START = False


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.name = "SingleApp-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Another instance is running", "ERROR")
            sys.exit()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.frame = MyFrame()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Say Hello', self.on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        try:
            self.frame.Show()
        except RuntimeError:
            self.frame = MyFrame()
        print('Tray icon was left-clicked.')

    def on_hello(self, event):
        print('Hello, world!')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Destroy()


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Table Order', size=(350, 250))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Button to sync data
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        l1 = wx.StaticText(panel, -1, "更新菜单(占用大量CPU)")
        hbox1.Add(l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        my_btn = wx.Button(panel, label='sync data')
        my_btn.Bind(wx.EVT_BUTTON, self.checkStock)
        hbox1.Add(my_btn, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox1)

        # select keyboard
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        l2 = wx.StaticText(panel, -1, "选择在手机上展示的keyboard")
        hbox2.Add(l2, 1, wx.ALIGN_LEFT | wx.ALL, 5)
        sampleList = loadKeyboardList()
        comboBox = wx.ComboBox(panel, size=wx.DefaultSize, value=sampleList[0] if len(sampleList) > 1 else 'empty', choices=sampleList)
        comboBox.Bind(wx.EVT_COMBOBOX, self.onSelect)
        hbox2.Add(comboBox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox2)

        # main thread, start syncing data
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        l3 = wx.StaticText(panel, -1, "开始主线程")
        hbox3.Add(l3, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        main_btn = wx.Button(panel, label='Start')
        main_btn.Bind(wx.EVT_BUTTON, self.thread_it)
        hbox3.Add(main_btn, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(hbox3)
        if IS_START:
            main_btn.Disable()
            main_btn.SetLabel("running")

        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def thread_it(self, event):
        #     global buttontext
        btn = event.GetEventObject()
        btn.SetLabel("running")
        btn.Disable()
        global IS_START
        if not IS_START:
            t = threading.Thread(target=pollingDatabase.MyRun)
            t.setDaemon(True)
            t.start()
            IS_START = True

    def checkStock(self, event):
        btn = event.GetEventObject()
        btn.SetLabel("Syncing data")
        btn.Disable()
        updateProducts.updateProducts()
        btn.Enable()
        btn.SetLabel("sync data")

    def onSelect(self, event):
        cb = btn = event.GetEventObject()
        keyboardId = posOperation.getKeyboardByKeyboardName(cb.GetStringSelection())[0][0]
        api.activateKeyboard(keyboardId)
        print("You selected: " + cb.GetStringSelection())

    def widgetMaker(self, widget, objects):
        for obj in objects:
            widget.Append(obj)
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)


def main():
    common.setVar()
    common.setUpTable()

    pusherWebsocket.PusherWebsocket()

    app = wx.App()
    TaskBarIcon()
    app.MainLoop()


if __name__ == "__main__":
    main()
