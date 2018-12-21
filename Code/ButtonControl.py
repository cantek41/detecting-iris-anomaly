#ButtonControl
import RPi.GPIO as GPIO
import time
import threading

class ButtonControl:

    def __init__(self,ccs):
        self.ccs = ccs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        self.stopEvent = threading.Event()
        #self.stopEvent.set()
        self.event=threading.Thread(target = self.buttonListener, args = ())        
        self.event.start()     

    def onClose(self):
        print("ButtonControl Ending...")
        self.stopEvent.set()        
            

    def run(self):                        
        self.stopEvent.clear()
        if not self.event.is_alive():
            self.event=threading.Thread(target = self.buttonListener, args = ())
            self.event.start()
       

    def buttonListener(self):
        while not self.stopEvent.is_set():
            btnRead = GPIO.input(16)
            #print("Btn Bası")
            if btnRead == False:
                print("Btn Basıldı")                
                #self.display.showMessage("btn")                
                self.stopEvent.set()

if  __name__ == "__main__":
    b=ButtonControl()
    b.run()
