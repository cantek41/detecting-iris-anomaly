from BarcodeControl import BarcodeControl
from DisplayControl import DisplayControl
from CameraControl import CameraControl
from ButtonControl import ButtonControl
from IrisControl import IrisControl
from enum import Enum
import ApiClient
import threading
import time


class SystemMode(Enum):
    READY = 0
    BARCODE = 1
    IRIS = 2
    BUSSY = 3
    RESET = 4
    IDLE=5

class CCS:    

    token=""
    mMode=None
    
    def __init__(self):
        self.barcodeControl=BarcodeControl()
        self.cameraControl=CameraControl()        
        self.buttonControl=ButtonControl(self)
        self.displayControl=DisplayControl()
        self.mMode = SystemMode.READY
        self.ButtonControl()
        self.timeover=10
        self.startTime=None
        self.currentTime=None

    def mLogin(self):
        return True

    def mCheckBarcode(self,image):        
        return  self.barcodeControl.CheckBarcode(image)

    def mShow(self,message):
        self.displayControl.showMessage(message)

    def mShowCamera(self):        
        vs=self.cameraControl.mCamera()
        self.displayControl.runVideo(vs)

    def mTakeImage(self):
        return self.displayControl.getImage()

    def mButton(self):        
        self.buttonControl.run()    

    def mSendData(self,image):
        return ApiClient.sendFile(image)
    
    def checkTime(self):
        if self.mMode == SystemMode.IDLE :
            return
        t=self.currentTime-self.startTime
        if t>self.timeover:
            self.mMode = SystemMode.IDLE
            print("time",t)
            self.IDLE()
            
    def IDLE(self):
        self.mShow("For Start Press Button")
        self.mMode = SystemMode.READY
        self.startTime=time.time()
        if self.cameraControl.vs:
            self.cameraControl.vs.stop()
        self.mButton()

    def Ready(self):
         self.mShow("READ --> BARCODE")
         self.mMode = SystemMode.BARCODE
         self.mShowCamera()
         self.mButton()
         
    def Barcode(self):
        image=self.mTakeImage()
        info=self.mCheckBarcode(image)                    
        if not info:
            self.mShow("READ --> BARCODE\nBarkode image is not Good!")
        else:
            info = info.decode("utf-8")
            self.mShow(info+"\nREAD --> IRIS")
            print(info)
            self.mMode = SystemMode.IRIS        
        self.mButton()
        
    def Iris(self):
        iris=IrisControl()
        image=self.mTakeImage()
        res=iris.CheckIris("image/"+image)
        if res:
            self.cameraControl.vs.stop()
            self.mMode = SystemMode.BUSSY
            self.Bussy(self,image)
        else:
            self.mShow("Image No Good \n READ --> IRIS")              

    def Bussy(self,image):
        self.mShow("SENDING DATA \n TO SERVER")                    
        result=mSendData("image/"+image)
        result="RESULT:\n"+result
        self.mShow(result)
        self.mMode = SystemMode.RESET
        self.mButton()
        
    def Loop(self):
        self.IDLE()
        print("----------START---------")
        self.startTime=time.time()
        while not self.stopEvent.is_set():
            self.currentTime=time.time()
            self.checkTime()            
            while self.buttonControl.stopEvent.is_set():
                self.startTime=time.time()
                if self.mMode == SystemMode.READY:                                       
                    self.Ready()
                    break
                if self.mMode == SystemMode.BARCODE:
                    self.Barcode()   
                    break
                if self.mMode == SystemMode.IRIS:
                    self.Iris()
                    break
                if self.mMode == SystemMode.BUSSY:
                    self.Bussy()
                    break
                if self.mMode == SystemMode.RESET:
                    print("RESET")
                    self.IDLE()                 
                    break
                print("default", self.mMode)
                break

    def Run(self):
        if self.mLogin():
            self.stopEvent = threading.Event()
            self.mainThread=threading.Thread(target = self.Loop, args = ())
            self.mainThread.start()
            self.displayControl.form.mainloop()

    def onClose(self):
        print("Main Thread Ending...")
        self.stopEvent.set()
                
        
if  __name__ == "__main__":
    rootApp = CCS()
    rootApp.Run()
