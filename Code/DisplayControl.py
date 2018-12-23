import tkinter as tki

from PIL import Image, ImageTk

import threading
import imutils
import cv2
import os
import datetime

class DisplayControl():
    
    def __init__(self):
        self.frame = None
        self.thread = None
        self.event = None
        self.vs=None

        self.form = tki.Tk()
        self.form.geometry("240x320")
        self.panel = None
        self.outputPath="image"


       
        self.stopEvent = threading.Event()
        self.text = tki.StringVar()
        self.statusText = tki.Label(self.form, textvariable = self.text)
        self.text.set("STATUS")
        self.statusText.pack()
        self.form.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        
        

    def showMessage(self,msg):
        self.text.set(msg)
        print(msg)

    def runCamera(self,vs):
        self.vs=vs
        self.event=threading.Thread(target = self.showCamera, args = ())
        self.event.start()
        
    def stopViewer(self):
        self.stopEvent.set()
        self.stopEvent = threading.Event()


    def showCamera(self):                
        while not self.stopEvent.is_set():
            self.frame = self.vs.read()            
            self.frame = imutils.resize(self.frame, width=300)
            self.frame = imutils.rotate(self.frame, 180)
            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            if self.panel is None:
                self.panel = tki.Label(image = image)
                self.panel.image = image
                self.panel.pack(side = "left", padx = 10, pady = 10)
            else:
                self.panel.configure(image = image)
                self.panel.image = image

    def getImage(self):
        #self.stopEvent.set()
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, self.frame.copy())
        return filename
            
    

    def onClose(self):
        print("Closing...")
        
        if self.vs:
            self.vs.stop()
        
        self.stopEvent.set()
        self.form.quit()
        
   
