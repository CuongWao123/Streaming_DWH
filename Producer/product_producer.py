from confluent_kafka import Producer
import socket
import pandas as pd

# Kafka producer config
conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "product-topic"

csv_file = r'C:\\Users\\LEGION\\Desktop\\Spark_Kafka\\DataSource\\product_data.csv'
df = pd.read_csv(csv_file)


for index, row in df.iterrows():
    message = row.to_json() 
    
    product_id = str(row['product_id']) 

    print(f"Producing message to {topic}: key={product_id}, value={message}")

    # Send the message
    producer.produce(
        topic=topic,
        key=product_id,
        value=message
    )

    producer.poll(0)

producer.flush()


