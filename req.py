import requests


response = requests.post(url="http://127.0.0.1:8000/", data=None)

if response.status_code != 200:
    print("erro")

else: 
    print("ok")

