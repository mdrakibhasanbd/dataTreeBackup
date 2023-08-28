import requests
import json

url = "http://192.168.100.2:5009/treemap"
data = {"routerName": "example"}

response = requests.post(url, json=data)

print(response.text)
