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
        self.buttonControl=ButtonControl()
        self.displayControl=DisplayControl()
        self.mMode = SystemMode.READY
        self.mButton()
        self.timeover=15
        self.startTime=None
        self.currentTime=None
        self.mLogin()

    def mLogin(self):
        self.token=ApiClient.sendRequest("login")
        return True

    def mCheckBarcode(self,image):     #4.1   
        return  self.barcodeControl.CheckBarcode(image)

    def mShow(self,message): #T3.2
        self.displayControl.showMessage(message)#S3.2

    def mShowCamera(self): #S2.3       
        vs=self.cameraControl.mCamera()
        self.displayControl.runVideo(vs)

    def mTakeImage(self): #T2.2
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
            
    def IDLE(self): #S1.3
        self.mShow("For Start Press Button")
        self.mMode = SystemMode.READY
        self.startTime=time.time()
        if self.cameraControl.vs:
            self.cameraControl.vs.stop()
        self.mButton()

    def Ready(self): #S1.4
         self.mShow("READ --> BARCODE")
         self.mMode = SystemMode.BARCODE
         self.mShowCamera()
         self.mButton()
         
    def Barcode(self): #S1.5
        image=self.mTakeImage()
        print(image)
        info=self.mCheckBarcode(image) #T.41
        if not info:
            self.mShow("READ --> BARCODE\nBarkode image is not Good!")
        else:
            info = info.decode("utf-8")
            self.mShow(info+"\nREAD --> IRIS")
            print(info)
            self.mMode = SystemMode.IRIS
        self.mButton()

    def Iris(self): #S1.6
        iris=IrisControl() 
        image=self.mTakeImage()
        res=iris.CheckIris("image/"+image) #T5.1
        if res:
            self.cameraControl.vs.stop()
            self.mMode = SystemMode.BUSSY
            self.Bussy(image)
        else:
            self.mShow("Image No Good \n READ --> IRIS")
            self.mButton()
	    

    def Bussy(self,image): #S1.7
        self.mShow("SENDING DATA \n TO SERVER")
        result=self.mSendData("image/"+image)
        result="RESULT:\n"+result
        self.mShow(result)
        self.startTime=time.time()
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
                if self.mMode == SystemMode.READY:   #T1.3                                    
                    self.Ready()
                    break
                if self.mMode == SystemMode.BARCODE: #T1.4
                    self.Barcode()   
                    break
                if self.mMode == SystemMode.IRIS: #T1.5
                    self.Iris()
                    break
                if self.mMode == SystemMode.BUSSY: #T1.6
                    self.Bussy()
                    break
                if self.mMode == SystemMode.RESET: #T1.7
                    print("RESET") #s1.8
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
