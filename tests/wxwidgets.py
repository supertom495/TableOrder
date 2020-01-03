import wx
import wx.adv 
import os
import time

TRAY_TOOLTIP = 'Table Order'
TRAY_ICON = "./API_data/icon.png"


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.frame = MyFrame()
        # self.frame.Show()


    # def loadFrame(self):
    #     return wx.Frame(parent=None, title='Hello World')

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


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Table Order')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)         
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)    


        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.OnClicked)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)        
        panel.SetSizer(my_sizer)       

        self.Show()
    

    def OnClicked(self, event):
        btn = event.GetEventObject()
        btn.Disable()
        time.sleep(2)
        btn.Enable()
        print("button clicked {}".format(btn.GetLabel()))


def main():
    app = wx.App()
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()