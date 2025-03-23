import requests
import time
import json
from confluent_kafka import Producer
import socket

conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

url = "https://api.weatherstack.com/current?access_key=5af80592c3b799cac81d278dc738caed"
querystring = {"query": "New York"}

topic = 'weather-topic'

while True:
    response = requests.get(url, params=querystring)
    data = response.json()
    
    key = data['location']['name'] 
    
    message = json.dumps(data)

    producer.produce(topic, key=key, value=message)
    producer.flush()  
    
    print(f"Send message : {key} và data: {message}")
    
    # Đợi 5 phút
    time.sleep(300)
