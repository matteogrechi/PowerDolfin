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
        videoStream = "rtsp://192.168.1.10:554/livestream/12"
        self.capture = cv2.VideoCapture(videoStream)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 25)
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
            self.timex.Start(17) #1000/24)
            self.Bind(wx.EVT_TIMER, self.redraw)
        else:
            print("Error no webcam image")
        
        # Keyboard
        self.pnl.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.pnl.Bind(wx.EVT_KEY_UP, self.keyUp)
        self.keyDown = None
        self.keyDict = {
                72 : "H",
                74 : "J",
                75 : "K",
                76 : "L",
                70 : "F"
        }
        self.action = {
            "H" : {"on" : "fe:0b:c9:ff:be:45:00:00:88:13:00:00:18:fc:00:00:04:b0:ae", "off" : "fe:0b:ec:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:bd:c8"},
            "J" : {"on" : "fe:0b:ba:ff:be:45:db:fe:88:13:00:00:00:00:00:00:04:12:27", "off" : "fe:0b:c8:ff:be:45:2a:fc:88:13:00:00:00:00:00:00:04:17:a6"},
            "K" : {"on" : "fe:0b:1e:ff:be:45:67:00:88:13:00:00:00:00:00:00:04:5a:7a", "off" : "fe:0b:45:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:7d:79"},
            "L" : {"on" : "fe:0b:20:ff:be:45:00:00:88:13:00:00:6f:03:00:00:04:f8:a5", "off" : "fe:0b:22:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:3d:16"}, # ?
            "F" : {"on" : "fe:04:07:ff:be:aa:64:00:00:00:f5:81", "off" : "fe:04:45:ff:be:aa:00:00:00:00:cf:70"}
        }

        # Command transmission connection
        cmdSocketAddress = ["192.168.1.12", 20002]
        self.commandConnection = socket.create_connection(cmdSocketAddress)

        #
        self.pnl.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.Show()
    
    def __del__(self):
        if self.commandConnection != None:
            self.commandConnection.close()
    

    def redraw(self,e):
        ret, self.frame = self.capture.read()
        if ret:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(self.frame)
            self.staticBit.SetBitmap(self.bmp)
            self.Refresh()
    
    def keyDown(self, e):
        if self.keyDown == None:
            key = e.GetKeyCode()
            self.keyDown = self.keyDict.get(key,None)
            if self.keyDown != None:
                self.sendCommand(self.action[self.keyDown]["on"])
    
    def keyUp(self, e):
        if self.keyDown != None:
            self.sendCommand(self.action[self.keyDown]["off"])
            self.keyDown = None

    def sendCommand(self, command):
        if self.commandConnection != None:
            if command != None:
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