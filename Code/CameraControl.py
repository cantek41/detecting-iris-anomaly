from imutils.video import VideoStream
import time

class CameraControl():
    
    def __init__(self):
        self.vs=None #S2.1
    
    
    def mCamera(self): #T2.1
        if not self.vs:
            self.vs=VideoStream(usePiCamera = 1).start()
            time.sleep(1.0)
        else:
            self.vs.stop()
            self.vs=VideoStream(usePiCamera = 1).start()
            time.sleep(1.0)
        return self.vs
