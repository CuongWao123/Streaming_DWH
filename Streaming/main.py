from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, when

# 1. Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("Spark Kafka Streaming to Postgres") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# 2. Kafka config
kafka_bootstrap_servers = "kafka:9092"
topic = "my-topic"

# 3. Đọc dữ liệu từ Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

# 4. Parse key và value (convert từ binary -> string)
messages = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# 5. Xử lý key NULL => generate UUID
messages_with_id = messages.select(
    when(col("key").isNull(), expr("uuid()")).otherwise(col("key")).alias("id"),
    col("value")
)

messages_with_id.printSchema()

# 6. Hàm ghi từng batch vào PostgreSQL
def write_to_postgres(batch_df, batch_id):
    print(f"\n=== Batch {batch_id} ===")

    count = batch_df.count()
    if count == 0:
        print(f"Batch {batch_id} is empty. Skipping write.")
        return

    batch_df.show(truncate=False)

    try:
        batch_df.write \
            .format("jdbc") \
            .mode("append") \
            .option("url", "jdbc:postgresql://postgres-db:5432/mydatabase") \
            .option("dbtable", "kafka_messages") \
            .option("user", "user") \
            .option("password", "example") \
            .option("driver", "org.postgresql.Driver") \
            .save()

        print(f"Batch {batch_id} written to PostgreSQL successfully!")

    except Exception as e:
        print(f"Error writing batch {batch_id} to PostgreSQL: {e}")

# 7. Khởi động writeStream đến PostgreSQL
query = messages_with_id.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "/tmp/spark_checkpoints_kafka_postgres") \
    .start()

query.awaitTermination()
