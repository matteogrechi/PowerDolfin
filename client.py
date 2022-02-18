import wx  # pip3 install wxPython
import cv2 # pip3 install opencv-python
import socket

# The following code is taken from 
# https://stackoverflow.com/questions/35009984/get-stream-from-webcam-with-opencv-and-wxpython
class viewWindow(wx.Frame):
    def __init__(self, parent, title="View Window"):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.pnl = wx.Panel(self)
        # Connecting to the camera
        #videoStream = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
        videoStream = "rtsp://192.168.1.10:554/livestream/12"
        self.capture = cv2.VideoCapture(videoStream)
        ret, self.frame = self.capture.read()
        if ret:
            self.wSize = self.frame.shape[:2]
            self.bmp = wx.Bitmap.FromBuffer(self.wSize[1], self.wSize[0], self.frame)

            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.image = wx.Image(self.wSize[1],self.wSize[0])
            self.imageBit = wx.Bitmap(self.image)
            self.staticBit = wx.StaticBitmap(self.pnl, wx.ID_ANY, self.bmp)
            self.vbox.Add(self.staticBit)

            self.timex = wx.Timer(self)
            self.timex.Start(1000.0/24.0)
            self.Bind(wx.EVT_TIMER, self.redraw)
        else:
            print("Error no webcam image")
        
        # Keyboard
        self.pnl.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.pnl.Bind(wx.EVT_KEY_UP, self.keyUp)
        self.kd = None
        self.keyDict = {
                72 : "H",
                74 : "J",
                75 : "K",
                76 : "L",
                70 : "F"
        }
        self.action = {
            "H" : {"on" : "", "off" : ""},
            "J" : {"on" : "", "off" : ""},
            "K" : {"on" : "", "off" : ""},
            "L" : {"on" : "", "off" : ""},
            "F" : {"on" : "fe:04:07:ff:be:aa:64:00:00:00:f5:81", "off" : "fe:04:45:ff:be:aa:00:00:00:00:cf:70"}
        }

        # Command transmission connection
        cmdSocketAddress = ["192.168.1.12", 20002]
        self.commandConnection = socket.create_connection(cmdSocketAddress)

        #
        self.pnl.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.Show()
        #self.pnl.SetFocus()

    def __del__(self):
        self.commandConnection.close()

    def redraw(self,e):
        ret, self.frame = self.capture.read()
        if ret:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(self.frame)
            self.staticBit.SetBitmap(self.bmp)
            self.Refresh()
    
    def keyDown(self, e):
        if self.kd == None:
            key = e.GetKeyCode()
            self.kd = self.keyDict.get(key,None)
            self.sendCommand(self.action[self.kd]["on"])
        
        
       # box = wx.MessageDialog(None, 'Do you like this blog?', 'Titolo box',wx.YES_NO) #Il box appare con due possibili scelte, Yes o No, in alternativa potete utilizzare il parametro wx.OK apparirà un'unica scelta, quella di pigiare il tasto OK.
        #answer=box.ShowModal() #Nel caso di parametro wx.YES_NO, la risposta al quesito visualizzato (appunto si o no) verrà salvata in questo caso nella variabile answer. 
        #box.Destroy()
    
    def keyUp(self, e):
        self.sendCommand(self.action[self.kd]["off"])
        self.kd = None

    def sendCommand(self, command):
        myBytes = bytes.fromhex(command.replace(":"," "))
        self.commandConnection.send(myBytes)

def main():
    app = wx.App()
    frame = viewWindow(None)
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
