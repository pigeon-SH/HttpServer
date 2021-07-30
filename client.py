import requests
import json

HOST = "http://" + "localhost"
PORT = "9999"
URL = HOST + ":" + PORT #URL should contain "http://" in order to know what protocol to use

def request_get():
    response = requests.get(URL).text
    data = json.loads(response)
    for record in data:
        print(record)

def request_post(name, content):
    response = requests.post(URL, json = {"name": name, "content": content}).text
    print("Result of POST Request")
    request_get()

def request_delete(key, value):
    response = requests.delete(URL + "/" + key + "/" + value).text
    print("Result of DELETE Request")
    request_get()

request_post("DoveSH", "This record will be deleted")
request_post("PigeonSH", "Summer is too hot")
request_delete("name", "DoveSH")
#request_get()
