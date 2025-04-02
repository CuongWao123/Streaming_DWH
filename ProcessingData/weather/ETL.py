from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, expr, from_json, to_timestamp, date_format, monotonically_increasing_id
)
from pyspark.sql.types import *

# ==========================
# 1. SparkSession khởi tạo
# ==========================
spark = SparkSession.builder \
    .appName("Spark Kafka Streaming to Postgres - Weather") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

kafka_bootstrap_servers = "kafka:9092"
topic = "weather-topic"

# ==========================
# 2. Định nghĩa SCHEMA cho weather-topic
# ==========================
weather_schema = StructType([
    StructField("request", StructType([
        StructField("type", StringType()),
        StructField("query", StringType()),
        StructField("language", StringType()),
        StructField("unit", StringType())
    ])),
    StructField("location", StructType([
        StructField("name", StringType()),
        StructField("country", StringType()),
        StructField("region", StringType()),
        StructField("lat", StringType()),
        StructField("lon", StringType()),
        StructField("timezone_id", StringType()),
        StructField("localtime", StringType()),
        StructField("localtime_epoch", LongType()),
        StructField("utc_offset", StringType())
    ])),
    StructField("current", StructType([
        StructField("observation_time", StringType()),
        StructField("temperature", IntegerType()),
        StructField("weather_code", IntegerType()),
        StructField("weather_icons", ArrayType(StringType())),
        StructField("weather_descriptions", ArrayType(StringType())),
        StructField("astro", StructType([
            StructField("sunrise", StringType()),
            StructField("sunset", StringType()),
            StructField("moonrise", StringType()),
            StructField("moonset", StringType()),
            StructField("moon_phase", StringType()),
            StructField("moon_illumination", IntegerType())
        ])),
        StructField("air_quality", StructType([
            StructField("co", StringType()),
            StructField("no2", StringType()),
            StructField("o3", StringType()),
            StructField("so2", StringType()),
            StructField("pm2_5", StringType()),
            StructField("pm10", StringType()),
            StructField("us-epa-index", StringType()),
            StructField("gb-defra-index", StringType())
        ])),
        StructField("wind_speed", IntegerType()),
        StructField("wind_degree", IntegerType()),
        StructField("wind_dir", StringType()),
        StructField("pressure", IntegerType()),
        StructField("precip", IntegerType()),
        StructField("humidity", IntegerType()),
        StructField("cloudcover", IntegerType()),
        StructField("feelslike", IntegerType()),
        StructField("uv_index", IntegerType()),
        StructField("visibility", IntegerType())
    ]))
])

# ==========================
# 3. Kafka Streaming
# ==========================
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

messages = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

parsed_messages = messages.select(
    from_json(col("value"), weather_schema).alias("data")
)

# ==========================
# 4. Xử lý dữ liệu & ghi vào PostgreSQL
# ==========================
def process_and_write_weather(batch_df, batch_id):
    print(f"\n=== Processing Batch {batch_id} ===")

    df_request = batch_df.select("data.request.*") \
        .drop('query') \
        .withColumn("request_id", expr("uuid()"))

    df_location = batch_df.select("data.location.*") \
        .withColumn("location_id", expr("uuid()")) \
        .withColumn("localtime", to_timestamp("localtime", "yyyy-MM-dd HH:mm"))

    df_current_raw = batch_df.select("data.current.*") \
        .withColumn("current_id", expr("uuid()")) \
        .withColumn("observation_time", to_timestamp("observation_time", "hh:mm a")) \
        .withColumn("observation_time", date_format("observation_time", "HH:mm:ss"))

    df_astro = df_current_raw.select("astro.*") \
        .withColumn("astro_id", expr("uuid()")) \
        .withColumn("sunrise", to_timestamp("sunrise", "hh:mm a").cast("timestamp")) \
        .withColumn("sunset", to_timestamp("sunset", "hh:mm a").cast("timestamp")) \
        .withColumn("moonrise", to_timestamp("moonrise", "hh:mm a").cast("timestamp")) \
        .withColumn("moonset", to_timestamp("moonset", "hh:mm a").cast("timestamp"))

    df_air_quality = df_current_raw.select("air_quality.*") \
        .withColumn("quality_id", expr("uuid()")) \
        .drop("us-epa-index", "gb-defra-index") \
        .withColumn("co", col("co").cast(DoubleType())) \
        .withColumn("no2", col("no2").cast(DoubleType())) \
        .withColumn("o3", col("o3").cast(DoubleType())) \
        .withColumn("so2", col("so2").cast(DoubleType())) \
        .withColumn("pm2_5", col("pm2_5").cast(DoubleType())) \
        .withColumn("pm10", col("pm10").cast(DoubleType()))

    df_current_indexed = df_current_raw.withColumn("idx", monotonically_increasing_id())
    df_air_quality_indexed = df_air_quality.withColumn("idx", monotonically_increasing_id())
    df_astro_indexed = df_astro.withColumn("idx", monotonically_increasing_id())

    df_current = df_current_indexed.join(
        df_air_quality_indexed.select("idx", "quality_id"), on="idx"
    ).join(
        df_astro_indexed.select("idx", "astro_id"), on="idx"
    ).drop("idx", "air_quality", "astro")

    df_request_indexed = df_request.withColumn("idx", monotonically_increasing_id())
    df_location_indexed = df_location.withColumn("idx", monotonically_increasing_id())
    df_current_final_indexed = df_current_raw.withColumn("idx", monotonically_increasing_id())

    df_data = df_request_indexed.join(
        df_location_indexed.select("idx", "location_id"), on="idx"
    ).join(
        df_current_final_indexed.select("idx", "current_id"), on="idx"
    ).select("request_id", "location_id", "current_id").withColumn("data_id", expr("uuid()"))

    print(df_data) 

    for dataframe, table in [
        (df_request.drop("idx"), "request"),
        (df_location.drop("idx"), "location"),
        (df_current.drop("idx"), "current"),
        (df_air_quality.drop("idx"), "current_air_quality"),
        (df_astro.drop("idx"), "current_astro"),
        (df_data.drop("idx"), "datas")
    ]:
        print(f"Writing {table} for batch {batch_id}...")

        try:
            dataframe.write \
                .format("jdbc") \
                .mode("append") \
                .option("url", "jdbc:postgresql://postgres-db:5432/mydatabase") \
                .option("dbtable", table) \
                .option("user", "user") \
                .option("password", "example") \
                .option("driver", "org.postgresql.Driver") \
                .save()

            print(f"Batch {batch_id}: {table} saved successfully!")

        except Exception as e:
            print(f"Error writing batch {batch_id} - table {table}: {e}")

# ==========================
# 5. Gửi kết quả vào foreachBatch
# ==========================
query = parsed_messages.writeStream \
    .outputMode("append") \
    .foreachBatch(process_and_write_weather) \
    .option("checkpointLocation", "/tmp/spark_checkpoints_kafka_postgres_weather") \
    .start()

query.awaitTermination()
