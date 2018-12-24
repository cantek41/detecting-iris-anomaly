import unittest
import ApiClient
import hashlib


class TestApiClient(unittest.TestCase):

    def test_sendRequest(self):
        hash_object = hashlib.md5("192.168.0.14".encode("utf-8"))
        id = hash_object.hexdigest()
        response=ApiClient.sendRequest("login")
        self.assertEqual(id, response)

    def test_sendFile(self):
        response=ApiClient.sendFile('ggg.jpg')
        self.assertIn("Hasta", response)


if __name__ == '__main__':
    unittest.main()
