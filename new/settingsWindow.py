import wx


class Settings(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.settings = {
        }

        self.panel = wx.Panel(self)
        self.button_ok = wx.Button(self.panel, label="OK")
        self.button_cancel = wx.Button(self.panel, label="Cancel")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)

        self.username = wx.TextCtrl(
            self.panel, value=self.settings.get('username', ''))
        self.username.SetHint("Username")

        self.password = wx.TextCtrl(
            self.panel, value=self.settings.get('password', ''), style=wx.TE_PASSWORD)
        self.password.SetHint("Password")

        self.high_threshold = wx.TextCtrl(
            self.panel, value=self.settings.get('high_threshold', ''))
        self.high_threshold.SetHint("High-Threshold")

        self.low_threshold = wx.TextCtrl(
            self.panel, value=self.settings.get('low_threshold', ''))
        self.low_threshold.SetHint("Low-Threshold")

        self.high_timeout = wx.TextCtrl(
            self.panel, value=self.settings.get('high_timeout', ''))
        self.high_timeout.SetHint("High-Timeout")

        self.low_timeout = wx.TextCtrl(
            self.panel, value=self.settings.get('low_timeout', ''))
        self.low_timeout.SetHint("Low-Timeout")

        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.username)
        self.sizer.Add(self.password)
        self.sizer.Add(0, 10, 0)
        self.sizer.Add(self.high_threshold)
        self.sizer.Add(self.low_threshold)
        self.sizer.Add(0, 10, 0)
        self.sizer.Add(self.high_timeout)
        self.sizer.Add(self.low_timeout)
        self.sizer.Add(0, 10, 0)
        self.sizer.Add(self.button_ok)
        self.sizer.Add(self.button_cancel)

        self.panel.SetSizerAndFit(self.sizer)

        self.Show()

    def onCancel(self, e):
        self.Destroy()

    def onOk(self, e):
        self.settings['username'] = self.username.GetValue()
        self.settings['password'] = self.password.GetValue()
        self.settings['high_threshold'] = self.high_threshold.GetValue()
        self.settings['low_threshold'] = self.low_threshold.GetValue()
        self.settings['high_timeout'] = self.high_timeout.GetValue()
        self.settings['low_timeout'] = self.low_timeout.GetValue()
        print(self.settings)
        self.Destroy()


def startSettings():
    app = wx.App(False)
    win = Settings(None)
    app.MainLoop()
