import requests
import json

url="http://192.168.0.34:5000/"

def sendRequest(api):
    response=requests.get(url+api)
    return response.content.decode("utf-8")

def sendFile(file):
    files = {'file': open(file, 'rb')}
    #files = {'file': open('image/gozcan.jpg', 'rb')}
    response=requests.post(url+"takeImage",files=files)
    print(response.content)
    response=response.content.decode("utf-8")
    response=json.loads(response)
    response="Hasta    ="+response["hasta"]+"\nSaglıklı ="+response["saglikli"]    
    print(response)
    return response
