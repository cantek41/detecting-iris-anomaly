from BarcodeControl import BarcodeControl

import threading

from DisplayControl import DisplayControl

from CameraControl import CameraControl


from ButtonControl import ButtonControl

from IrisControl import IrisControl

from enum import Enum

class SystemMode(Enum):
    READY = 0
    BARCODE = 1
    IRIS = 2
    BUSSY = 3
    RESET = 4


class CCS:    
    
    def __init__(self):
        self.barcodeControl=BarcodeControl()
        self.cameraControl=CameraControl()        
        self.buttonControl=ButtonControl(self)
        self.displayControl=DisplayControl()
        self.mode = SystemMode.READY
        self.ButtonControl()
        
    

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
        

    def Loop(self):
        self.displayControl.showMessage("READY")
        print("-------------------")
        while not self.stopEvent.is_set():
            while self.buttonControl.stopEvent.is_set():
                if self.mode == SystemMode.READY:
                    self.displayControl.showMessage("READ --> BARCODE")
                    self.mode = SystemMode.BARCODE
                    self.CameraControl()
                    self.buttonControl.run()                    
                    #self.BarcodeControl()
                    break
                if self.mode == SystemMode.BARCODE:
                    name=self.displayControl.getImage()                    
                    info=self.barcodeControl.CheckBarcode(name)
                    if not info:
                        self.displayControl.showMessage("Please READ --> BARCODE")
                    else:
                        info = info.decode("utf-8")
                    print(name)
                    self.mode = SystemMode.IRIS
                    break
                if self.mode == SystemMode.IRIS:
                    iris=IrisControl()
                    name=iris.CheckIris("image/2018-12-20_09-23-59.jpg")  
                    #iriscoıntol
                    print(name)
                    
                    self.mode = SystemMode.READY                  
                    break
                if self.mode == SystemMode.BUSSY:
                    print("BUSSY")
                    break
                if self.mode == SystemMode.RESET:
                    print("RESET")
                    break
                print("çok garip", self.mode)
                break
                
        
if  __name__ == "__main__":

    rootApp = CCS()
    rootApp.Run()
