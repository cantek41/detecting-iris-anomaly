import unittest
from IrisControl import IrisControl
class TestIrisControl(unittest.TestCase):

    def test_CheckIris(self):
        iris=IrisControl()
        re=iris.CheckIris("ggg.jpg")
        self.assertTrue(re)

   

if __name__ == '__main__':
    unittest.main()
