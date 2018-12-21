from PIL import Image
import cv2

EYES_CASCADE = 'eyecascade.xml'

class IrisControl:

    def CheckIris(self,img):
        resim=cv2.imread(img)
        yuztani = cv2.CascadeClassifier(EYES_CASCADE)
        griton=cv2.cvtColor(resim,cv2.COLOR_BGR2GRAY)
        yuzbul=yuztani.detectMultiScale(griton,1.1,4)
        print(len(yuzbul))

        if len(yuzbul)>0:
            return True
        return False

        for (x,y,w,h) in yuzbul:
            cv2.rectangle(resim,(x,y),(x+w,y+h),(0,0,0),10)
        cv2.imshow("Yuz Tanima",resim)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        

if __name__ == "__main__":
    iris=IrisControl()
    name=iris.CheckIris("ggg.jpg")   
    print(name)
    


