from glob import glob
from random import randrange
from time import localtime, strftime
from os.path import expanduser
import wx

class Kiosk(wx.Frame):

    def __init__(self, parent, title):
        super(Kiosk, self).__init__(parent, title=title,
            size=wx.GetDisplaySize())
        self.filepath = None

        self.panel = wx.Panel(self)
        self.ShowFullScreen(True)
        self.createWidgets()

        self.panel.Layout()
        self.createTimers()
        cursor = wx.StockCursor(wx.CURSOR_BLANK)
        self.SetCursor(cursor)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.onKeypress)

    def onKeypress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.Close()

    def createTimers(self):
        self.cycleTimer = wx.Timer(self, 100);
        self.DateTimer = wx.Timer(self, 200);
        self.cycleTimer.Start(6000);
        self.DateTimer.Start(1000);
        wx.EVT_TIMER(self, 100, lambda x: self.chooseFile())
        wx.EVT_TIMER(self, 200, lambda x: self.setTime())
        self.setTime()
        self.chooseFile()


    def chooseFile(self):
        imgs = glob(expanduser('~/Pictures/*.png'))
        choice = randrange(len(imgs))
        self.filepath = imgs[choice]
        self.onView()

    def setTime(self):
        now = localtime();
        timeString = strftime('%H:%M', now)
        self.TimeText.SetLabel(timeString)
        for shadow in self.TimeShadow:
            shadow.SetLabel(timeString)
        dateString = strftime('%A, %B %d', now)
        self.DateText.SetLabel(dateString)
        for shadow in self.DateShadow:
            shadow.SetLabel(dateString)

    def createTime(self):
        right = 5
        top = self.GetSize()[1] - 150
        self.TimeFont = wx.Font(72, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.TimeShadow = []
        for r, t in [(-1,-1),(-1,2),(2,-1),(2,2)]:
            shadow = wx.StaticText(self.panel, label='', pos=(right+r, top+t))
            shadow.SetForegroundColour((0,0,0))
            shadow.SetFont(self.TimeFont)
            self.TimeShadow.append(shadow)
        self.TimeText = wx.StaticText(self.panel, label='', pos=(right, top))
        self.TimeText.SetForegroundColour((255,255,255))
        self.TimeText.SetFont(self.TimeFont)

    def createDate(self):
        right = 5
        top = self.GetSize()[1] - 50
        self.DateFont = wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.DateShadow = []
        for r, t in [(-1,-1),(-1,2),(2,-1),(2,2)]:
            shadow = wx.StaticText(self.panel, label='', pos=(right+r, top+t))
            shadow.SetForegroundColour((0,0,0))
            shadow.SetFont(self.DateFont)
            self.DateShadow.append(shadow)
        self.DateText = wx.StaticText(self.panel, label='', pos=(right, top))
        self.DateText.SetForegroundColour((255,255,255))
        self.DateText.SetFont(self.DateFont)


    def createWidgets(self):
	self.SetBackgroundColour((0,0,0))
        self.panel.SetBackgroundColour((0,0,0))

        # Create initial, blank, image
        width,height = self.GetSize()
        img = wx.EmptyImage(width, height)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))
        self.imageCtrl.SetBackgroundColour((0,0,0))

        # Create date/time overlay
        self.createTime()
        self.createDate()

        # Create sizer to center main image
        self.panel.Layout()


    def onView(self):
        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        width,height = self.GetSize()
        W = float(img.GetWidth())
        H = float(img.GetHeight())
        # Resize to fit screen
        if W > width:
            H = H * width / W
            W = width
        if H > height:
            W = W * height / H
            H = height
        img = img.Scale(W,H)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
	
	left = width / 2 - W / 2
	top = height / 2 - H / 2

	self.imageCtrl.SetPosition((left, top ))
        self.panel.Refresh()

if __name__ == '__main__':
    app = wx.App()
    Kiosk(None, title='Kiosk')
    app.MainLoop()

