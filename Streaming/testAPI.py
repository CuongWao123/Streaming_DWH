# import requests
# import json
# from kafka import KafkaProducer

# # Lấy dữ liệu từ API
# url = "https://streaming-availability.p.rapidapi.com/shows/search/filters"

# querystring = {
#     "country": "VN",
#     "series_granularity": "show",
#     "order_direction": "asc",
#     "order_by": "original_title",
#     "genres_relation": "and",
#     "output_language": "en",
#     "show_type": "movie"
# }

# headers = {
#     "x-rapidapi-key": "1615843437msh2dc40e4ba251729p193a49jsnf60fd67ede87",
#     "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# if response.status_code != 200:
#     print(f"❌ Failed to fetch data! Status code: {response.status_code}")
#     exit()

# data = response.json()
# print("Fetched API data!")

# # Kafka producer setup
# producer = KafkaProducer(
#     bootstrap_servers=['127.0.0.1:9092'],  # đổi localhost thành 127.0.0.1
#     value_serializer=lambda v: json.dumps(v).encode('utf-8'),
#     retries=5,
#     request_timeout_ms=5000,
#     api_version_auto_timeout_ms=5000
# )

# topic = 'my-topic'

# try:
#     future = producer.send(topic, value=data)
#     record_metadata = future.get(timeout=10)

#     print(f"✅ Sent data to topic '{record_metadata.topic}' partition {record_metadata.partition} offset {record_metadata.offset}")

#     producer.flush()

# except Exception as e:
#     print(f"❌ Error sending data to Kafka: {e}")

# finally:
#     producer.close()


# from confluent_kafka import Producer

# conf = {
#     'bootstrap.servers': 'kafka:9092'
# }

# producer = Producer(**conf)


# def delivery_report(err, msg):
#     if err is not None:
#         print(f'Message delivery failed: {err}')
#     else:
#         print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

# topic = 'my-topic'

# for i in range(10):
#     message = f'Hello Kafka {i}'
#     print(message) 
#     producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)

# producer.flush()


import requests

url = "https://porn-xnxx-api.p.rapidapi.com/download"

payload = { "video_link": "https://xnxx.com/video-wugb904/fucking_his_step_sister_lexxi_steele_in_high_definition" }
headers = {
	"x-rapidapi-key": "1615843437msh2dc40e4ba251729p193a49jsnf60fd67ede87",
	"x-rapidapi-host": "porn-xnxx-api.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())