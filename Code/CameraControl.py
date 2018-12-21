from imutils.video import VideoStream
import time

class CameraControl():

    
    def getCamera(self):
        vs=VideoStream(usePiCamera = 1).start()
        time.sleep(1.0)
        return vs
