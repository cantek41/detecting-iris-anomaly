import requests

url="http://192.168.0.14:5000/upload_file"

files = {'file': open('image/gozcan.jpg', 'rb')} 

response=requests.post(url,files=files)
print(response.content)
