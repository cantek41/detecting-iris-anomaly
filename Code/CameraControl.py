from imutils.video import VideoStream
import time

class CameraControl():
    
    def __init__(self):
        self.vs=None
    
    
    def getCamera(self):
        if not self.vs:
            self.vs=VideoStream(usePiCamera = 1).start()
            time.sleep(1.0)
        else:
            self.vs.stop()
            self.vs=VideoStream(usePiCamera = 1).start()
            time.sleep(1.0)
        return self.vs
