# 🚀 Real-time Data Pipeline: Kafka + Spark + Postgres + Metabase

This project sets up a **real-time data pipeline** using **Kafka**, **Apache Spark**, **PostgreSQL**, and **Metabase**. It streams, processes, and visualizes data using Docker Compose.

---

## ⚙️ Getting Started

### 1. Start All Services
```bash
docker compose up -d
```

---

### 2. Create Kafka Topics
```bash
docker exec -it kafka kafka-topics.sh --create --topic customer-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics.sh --create --topic product-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics.sh --create --topic sales-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

---

### 3. Run Spark Streaming Jobs (in separate terminals)

#### Product ETL Job
```bash
docker exec -it spark-master /bin/bash
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --jars /opt/bitnami/spark/jars/postgresql.jar \
  --total-executor-cores 1 \
  /opt/bitnami/spark/jobs/productETL.py
```

#### Customer ETL Job
```bash
docker exec -it spark-master /bin/bash
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --jars /opt/bitnami/spark/jars/postgresql.jar \
  --total-executor-cores 1 \
  /opt/bitnami/spark/jobs/custETL.py
```

#### Sales ETL Job
```bash
docker exec -it spark-master /bin/bash
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --jars /opt/bitnami/spark/jars/postgresql.jar \
  --total-executor-cores 1 \
  /opt/bitnami/spark/jobs/salesETL.py
```

---

### 4. Run Kafka Data Producers
```bash
python producer/product_producer.py
python producer/cust_producer.py
python producer/sales_producer.py
```

---

### 5. Access Metabase Dashboard
Open your browser and go to:
```
http://localhost:3000
```

#### PostgreSQL Connection Info:
- **Host**: `postgres-db`
- **Port**: `5432`
- **Database**: `mydatabase`
- **Username**: `user`
- **Password**: `example`

Then, create dashboards and visualize your data!

---

## 📦 Services Overview

| Service      | Port(s)         | Description                              |
|--------------|-----------------|------------------------------------------|
| Zookeeper    | `2181`          | Kafka's coordination service             |
| Kafka        | `9092 / 29092`  | Message broker                           |
| Spark Master | `7077 / 8080`   | Spark cluster master & web UI            |
| Spark Worker | `8081+`         | Spark workers (monitor on different ports) |
| PostgreSQL   | `5432`          | Database storing processed data          |
| Metabase     | `3000`          | Visualization & dashboarding tool        |

---

## 📁 Project Structure

```
.
├── docker-compose.yml
├── ProcessingData
│   ├── customer
│   │   └── ETL.py
│   ├── product
│   │   └── ETL.py
│   └── sales
│       └── ETL.py
├── producer
│   ├── product_producer.py
│   ├── cust_producer.py
│   └── sales_producer.py
├── postgresql.jar
└── init.sql
```

---

## 🚀 Quick Summary

1. Start services: `docker compose up -d`
2. Create Kafka topics
3. Run Spark ETL jobs
4. Run Kafka producers
5. Open Metabase at `http://localhost:3000` to explore your data!

---

