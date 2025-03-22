from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, expr
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
#LOAD
spark = SparkSession.builder \
    .appName("Spark Kafka Streaming Sales") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

kafka_bootstrap_servers = "kafka:9092"
topic = "sales-topic"

sales_schema = StructType() \
    .add("product_id", StringType()) \
    .add("customer_id", StringType()) \
    .add("quantity", IntegerType()) \
    .add("sale_date", StringType()) \
    .add("price", DoubleType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

messages = df.selectExpr("CAST(value AS STRING) as raw_value")

from pyspark.sql.functions import split
# TRANSFORM
split_cols = split(col("raw_value"), ",")

parsed_messages = messages.select(
    expr("uuid()").alias("sale_id"),          
    split_cols.getItem(1).alias("product_id"),
    split_cols.getItem(2).alias("customer_id"),
    split_cols.getItem(3).cast(IntegerType()).alias("quantity"),
    split_cols.getItem(4).alias("sale_date"),
    split_cols.getItem(5).cast(DoubleType()).alias("price")
)

parsed_messages.printSchema()

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
            .option("dbtable", "sales") \
            .option("user", "user") \
            .option("password", "example") \
            .option("driver", "org.postgresql.Driver") \
            .save()

        print(f"Batch {batch_id} written to PostgreSQL successfully!")

    except Exception as e:
        print(f"Error writing batch {batch_id} to PostgreSQL: {e}")

# Start stream processing
#LOAD 
query = parsed_messages.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "/tmp/spark_checkpoints_kafka_postgres_sales") \
    .start()

query.awaitTermination()
