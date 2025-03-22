from confluent_kafka import Producer
import socket
import pandas as pd
import time

conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "my-topic"

csv_file = 'C:\\Users\\LEGION\\Desktop\\Spark_Kafka\\DataSource\\weatherHistory.csv'
df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    message = row.to_json() 
    print(f"Producing message to {topic}: {message}")

    producer.produce(topic, key='weather', value=message)
    producer.poll(0)

producer.flush()

print("Done sending messages.")
