import requests
import time
import json
from confluent_kafka import Producer
import socket

# Cấu hình Kafka
conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

# API Key của WeatherStack (thay bằng API key của bạn)
API_KEY = "e4bf7fd21ef18b24000fb21094f494ea"
BASE_URL = "https://api.weatherstack.com/current"

# Danh sách 30 thành phố lớn trên thế giới
cities = [
     "Seoul", "Shanghai", "Cairo", "Lagos", "Rome", "Madrid", "Johannesburg", "Singapore", "Hong Kong" ,"Viet Nam",
    "New York", "Los Angeles", "Chicago", "Houston", "Miami", "London", "Paris",
    "Tokyo", "Beijing", "Sydney", "Berlin", "Toronto", "Mexico City", "Moscow",
    "Mumbai", "Bangkok", "Jakarta", "Dubai", "Istanbul", "São Paulo", "Buenos Aires"
   
]

topic = 'weather-topic'

while True:
    for city in cities:
        try:
            querystring = {"access_key": API_KEY, "query": city}
            response = requests.get(BASE_URL, params=querystring)

            if response.status_code == 200:
                data = response.json()

                if "current" in data:
                    message = json.dumps(data)

                    producer.produce(topic, value=message)
                    producer.flush()

                    print(f"✅ Sent message for {city}: {message}")
                else:
                    print(f"⚠️ Invalid data for {city}: {data}")

            else:
                print(f"❌ Failed to get data for {city}, status code: {response.status_code}")

        except Exception as e:
            print(f"❌ Error fetching data for {city}: {e}")

        time.sleep(60)  

    time.sleep(300) 
