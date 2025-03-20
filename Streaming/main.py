from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("Spark Kafka Streaming Example") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

kafka_bootstrap_servers = "kafka:9092"  
topic = "my-topic"


df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()


messages = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


query = messages.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
