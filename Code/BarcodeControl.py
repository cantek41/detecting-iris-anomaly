from pyzbar.pyzbar import decode
from PIL import Image

class BarcodeControl:

    def CheckBarcode(self,img):
        try:
            data= decode(Image.open("image/"+img))
            return data[0].data
        except:
            return None

if __name__ == "__main__":
    barcode=BarcodeControl()
    name=barcode.CheckBarcode("image/qq.jpg")   
    if not name:
        print("Please READ --> BARCODE")
    else:
        name = name.decode("utf-8")
        print(name)
    
