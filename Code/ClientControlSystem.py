from BarcodeControl import BarcodeControl

import threading

from DisplayControl import DisplayControl

from CameraControl import CameraControl


from ButtonControl import ButtonControl

from IrisControl import IrisControl

from enum import Enum

import ApiClient
import time

class SystemMode(Enum):
    READY = 0
    BARCODE = 1
    IRIS = 2
    BUSSY = 3
    RESET = 4
    IDLE=5


class CCS:    
    
    def __init__(self):
        self.barcodeControl=BarcodeControl()
        self.cameraControl=CameraControl()        
        self.buttonControl=ButtonControl(self)
        self.displayControl=DisplayControl()
        self.mode = SystemMode.READY
        self.ButtonControl()
        self.iris=None
        self.timeover=10
        self.startTime=None
        self.currentTime=None
    

    def BarcodeControl(self):
        #b=BarcodeControl()
        info=self.barcodeControl.CheckBarcode("qrcode.png").decode("utf-8")       
        print(info)
        self.buttonControl.run()

    def DisplayControl(self):
        #formThread=threading.Thread(target=display.form.mainloop,args=())
        #display.form.mainloop()
        self.displayControl.showMessage("IRIS")

    def CameraControl(self):        
        vs=self.cameraControl.getCamera()
        self.displayControl.runCamera(vs)

    def ButtonControl(self):        
        self.buttonControl.run()

    def Run(self):
        self.stopEvent = threading.Event()
        self.mainThread=threading.Thread(target = self.Loop, args = ())
        self.mainThread.start()
        self.displayControl.form.mainloop()

    def onClose(self):
        print("Main Thread Ending...")
        self.stopEvent.set() 

    def checkTime(self):
        if self.mode == SystemMode.IDLE :
            return
        t=self.currentTime-self.startTime
        if t>self.timeover:
            self.mode = SystemMode.IDLE
            print("time",t)
            self.IDLE()
            
    def IDLE(self):
        self.displayControl.showMessage("IDLE")
        self.displayControl.showMessage("For Start Press Button")
        self.mode = SystemMode.READY
        self.startTime=time.time()
        if self.cameraControl.vs:
            self.cameraControl.vs.stop()
        self.buttonControl.run()

    def Loop(self):
        self.IDLE()
        print("-------------------")
        self.startTime=time.time()
        while not self.stopEvent.is_set():
            self.currentTime=time.time()
            self.checkTime()            
            while self.buttonControl.stopEvent.is_set():                                                              
                if self.mode == SystemMode.READY:
                    self.displayControl.showMessage("READ --> BARCODE")
                    self.mode = SystemMode.BARCODE
                    self.CameraControl()
                    self.startTime=time.time()
                    self.buttonControl.run()                    
                    #self.BarcodeControl()
                    break
                if self.mode == SystemMode.BARCODE:
                    name=self.displayControl.getImage()
                    print(name)
                    info=self.barcodeControl.CheckBarcode(name)                    
                    if not info:
                        self.displayControl.showMessage("READ --> BARCODE"+
                                                        "Barkode image is not Good!")
                    else:
                        info = info.decode("utf-8")
                        self.displayControl.showMessage(info+"\n"+
                                                        "READ --> IRIS")
                        print(info)
                        self.mode = SystemMode.IRIS
                    self.startTime=time.time()
                    self.buttonControl.run()   
                    break
                if self.mode == SystemMode.IRIS:
                    iris=IrisControl()
                    image=self.displayControl.getImage()
                    res=iris.CheckIris("image/"+image)
                    if res:
                        self.cameraControl.vs.stop()
                        self.iris=image
                        self.mode = SystemMode.BUSSY
                    else:
                        self.displayControl.showMessage("Image No Good \n READ --> BARCODE")              
                    self.startTime=time.time()
                    break
                if self.mode == SystemMode.BUSSY:
                    self.displayControl.showMessage("SENDING DATA \n TO SERVER")                    
                    result=ApiClient.sendFile("image/"+self.iris)
                    result="RESULT:\n"+result
                    self.displayControl.showMessage(result)
                    self.buttonControl.run()
                    self.mode = SystemMode.RESET 
                    self.startTime=time.time()
                    break
                if self.mode == SystemMode.RESET:
                    print("RESET")
                    self.IDLE()
                    #self.buttonControl.run()
                    #self.mode = SystemMode.READY                    
                    break
                print("çok garip", self.mode)
                break
                
        
if  __name__ == "__main__":
    rootApp = CCS()
    rootApp.Run()
