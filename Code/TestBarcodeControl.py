import unittest
from BarcodeControl import BarcodeControl
class TestBarcodeControl(unittest.TestCase):

    def test_CheckBarcode(self):
        barcode=BarcodeControl()
        name=barcode.CheckBarcode("qrcode.png").decode("utf-8")
        self.assertEqual("Name:Cantekin;Age:35", name)

   

if __name__ == '__main__':
    unittest.main()
