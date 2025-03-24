import requests
import time

url = "https://api.weatherstack.com/current?access_key=5af80592c3b799cac81d278dc738caed"
querystring = {"query": "New York"}

while True:
    response = requests.get(url, params=querystring)
    data = response.json()
    print(data)
    
    time.sleep(300)
