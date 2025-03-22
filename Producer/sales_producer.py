from confluent_kafka import Producer
import socket
import pandas as pd
import time

conf = {
    'bootstrap.servers': 'localhost:29092',
    'client.id': socket.gethostname()
}

producer = Producer(conf)

topic = "sales-topic"


csv_file1 = r'C:\Users\LEGION\Desktop\Spark_Kafka\DataSource\sales_2022.csv'
csv_file2 = r'C:\Users\LEGION\Desktop\Spark_Kafka\DataSource\sales_2023.csv'


df1 = pd.read_csv(csv_file1)
df2 = pd.read_csv(csv_file2)


def produce_dataframe(df, year_label):
    for index, row in df.iterrows():
        message = row.to_json()

        sale_id = str(row['sale_id'])

        print(f"Producing message to {topic}: key={sale_id}, value={message}")

        producer.produce(
            topic=topic,
            key=sale_id,
            value=message
        )

        producer.poll(0)


produce_dataframe(df1, "2022")
produce_dataframe(df2, "2023")


producer.flush()


