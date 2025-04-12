# **NYC Taxi Batch Processing Data Architecture**  

🚖 **Scalable, Fault-Tolerant Batch Pipeline for NYC Taxi Data**  
📊 **Tech Stack:** Spark (Scala/Python), Docker, PostgreSQL, HDFS, Airflow, Terraform  
🔗 **GitHub:** https://github.com/yashwanth08/Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxi.git  

---

## **📌 Introduction**  
This project implements a **production-grade batch processing pipeline** for NYC Taxi & Limousine Commission (TLC) trip data. Designed for scalability and reliability, the system ingests, cleans, transforms, and aggregates millions of records using **Apache Spark**, **Dockerized microservices**, and **IaC (Infrastructure as Code)** principles. The processed data supports analytics and ML model retraining on a quarterly schedule, as outlined in the original **Data Engineering Portfolio (Part 1: Conception Phase)**.  

---

## **📂 Repository Structure**  
```
├── Dockerfile    : Scala spark Dockerfile
├── build.sbt     : Scala sbt build file
├── config        : configuration files for DB/Kafka/AWS..
├── data          : Raw/processed/output data (batch/stream)
├── doc           : All repo reference/doc/pic
├── elk           : ELK (Elasticsearch, Logstash, Kibana) config/scripts 
├── fluentd       : Fluentd help scripts
├── kafka         : Kafka help scripts
├── pyspark       : Legacy pipeline code (Python)
├── requirements.txt
├── script        : Help scripts (env/services) 
├── src           : Batch/stream process scripts (Scala)
└── utility       : Help scripts (pipeline)
```

---

## **🛠️ Technologies Used**  
| **Category**       | **Tools**                                                                 |
|--------------------|--------------------------------------------------------------------------|
| **Batch Processing** | Apache Spark (Scala/PySpark), Hadoop (HDFS)                              |
| **Orchestration**  | Apache Airflow (DAGs for scheduling)                                     |
| **Storage**        | PostgreSQL (OLAP), MinIO/S3 (data lake), HDFS (distributed storage)      |
| **Infrastructure** | Docker (containerization), Terraform (IaC), Kubernetes (scaling)         |
| **Monitoring**     | Prometheus + Grafana, Spark UI                                           |
| **CI/CD**         | GitHub Actions (automated testing & deployment)                          |

---

## **🚀 Quick Start (Local Deployment)**  

### **1. Prerequisites**  
- Docker & Docker Compose  
- Java 8/11, Scala 2.12, Python 3.8+  
- Terraform (optional, for cloud deployment)  

### **2. Run the Pipeline**  
```bash
# Clone the repo
git clone https://github.com/Omia7814/YASHWAN_Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxi.git
cd YASHWAN_Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxi

# Start services (Spark, Postgres, Airflow)
docker-compose up -d

# Ingest sample data (NYC Taxi 2023)
./scripts/download_sample_data.sh

# Submit Spark job (Scala)
docker exec spark-master spark-submit \
  --class nyctaxi.processing.BatchPipeline \
  /opt/spark-apps/taxi-processing.jar \
  --input-path /data/raw --output-path /data/processed

# Access services:
# - Spark UI: http://localhost:4040
# - Airflow: http://localhost:8080 (admin/admin)
# - PostgreSQL: jdbc:postgresql://localhost:5432/nyctaxi
```

---

## **🔧 Key Features**  

### **✅ Batch Processing Pipeline**  
| **Stage**         | **Description**                                                                 |
|-------------------|-------------------------------------------------------------------------------|
| **Data Ingestion** | Automated downloads from NYC TLC + validation (checksums, schema checks)       |
| **Cleaning**      | Handle missing values, outliers, and incorrect timestamps                      |
| **Transformation**| Feature engineering (trip duration, geospatial zones, time-based aggregations) |
| **Loading**       | Output to PostgreSQL (analytics), HDFS (raw), and S3 (archival)                |

### **✅ Fault Tolerance & Scalability**  
- **Checkpointing** (Spark Structured Streaming)  
- **Data Partitioning** (by date/vendor to avoid skew)  
- **Auto-scaling** (Kubernetes cluster for Spark workers)  

### **✅ Monitoring & Logging**  
- **Spark UI** (job tracking)  
- **Grafana Dashboard** (metrics: CPU, memory, I/O)  
- **Airflow Alerts** (failed DAGs)  

---

## **📊 Sample Use Case: Monthly Aggregations**  
**Business Question:** *"Which NYC zones have the highest average trip durations per month?"*  

**Spark SQL Query:**  
```sql
SELECT 
  pickup_zone, 
  AVG(trip_duration_minutes) AS avg_duration,
  COUNT(*) AS trip_count
FROM nyctaxi.trips 
WHERE trip_month = '2023-11'
GROUP BY pickup_zone
ORDER BY avg_duration DESC
LIMIT 10;
```

**Output (PostgreSQL):**  
| **pickup_zone**       | **avg_duration** | **trip_count** |  
|-----------------------|------------------|----------------|  
| JFK Airport           | 42.5             | 12,540         |  
| LaGuardia Airport     | 38.2             | 9,876          |  

---

## **📜 License**  
MIT License - See [LICENSE](LICENSE).  

---

## **📬 Conclusion**  
This project delivers a **fully automated, scalable batch processing system** for NYC Taxi data, adhering to **reliability, maintainability, and security** best practices. Future enhancements could include:  
- Real-time streaming (Kafka + Spark Streaming)  
- ML integration (Feast for feature stores)  
- Cloud optimization (AWS EMR/Google Dataproc)  

**Feedback & contributions welcome!** 🚀  

--- 

🔗 **Connect:** [Phone](+254718249916)  
📧 **Contact:** yashwanthkrishna98@gmail.com
