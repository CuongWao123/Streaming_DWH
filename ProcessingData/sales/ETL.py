from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, expr
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType, DateType

# 1. Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("Spark Kafka Streaming to Postgres - Sales") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

kafka_bootstrap_servers = "kafka:9092"
topic = "sales-topic"


sales_schema = StructType() \
    .add("sale_id", StringType()) \
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

messages = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

parsed_messages = messages.select(
    from_json(col("value"), sales_schema).alias("data")
).select(
    expr("uuid()").alias("id"),          
    col("data.sale_id"),
    col("data.product_id"),
    col("data.customer_id"),
    col("data.quantity"),
    col("data.sale_date").cast(DateType()), 
    col("data.price")
)

parsed_messages.printSchema()

# 7. Hàm ghi vào PostgreSQL
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

# 8. Viết stream vào Postgres
query = parsed_messages.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", "/tmp/spark_checkpoints_kafka_postgres_sales") \
    .start()

query.awaitTermination()
