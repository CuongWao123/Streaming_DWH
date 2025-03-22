from confluent_kafka import Producer
import socket
import pandas as pd

# Kafka producer config
conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "customer-topic"

csv_file = r'C:\\Users\\LEGION\\Desktop\\Spark_Kafka\\DataSource\\customer_data.csv'
df = pd.read_csv(csv_file)


for index, row in df.iterrows():
    message = row.to_json() 
    
    customer_id = str(row['customer_id']) 

    print(f"Producing message to {topic}: key={customer_id}, value={message}")

    # Send the message
    producer.produce(
        topic=topic,
        key=customer_id,
        value=message
    )

    producer.poll(0)

producer.flush()


