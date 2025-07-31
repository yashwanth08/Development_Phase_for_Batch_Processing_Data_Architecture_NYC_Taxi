from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CSV Reader") \
    .getOrCreate()

# Set MinIO / S3a config
#hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
#hadoop_conf.set("fs.s3a.access.key", "admin")
#hadoop_conf.set("fs.s3a.secret.key", "password123")
#hadoop_conf.set("fs.s3a.endpoint", "http://localhost:9000")
#hadoop_conf.set("fs.s3a.path.style.access", "true")
#hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")
#hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") #


conf = SparkConf()

conf.set('spark.hadoop.fs.s3a.endpoint', "http://localhost:9000")
conf.set('spark.hadoop.fs.s3a.access.key', "admin")
conf.set('spark.hadoop.fs.s3a.secret.key', "password123")
conf.set('spark.hadoop.fs.s3a.path.style.access', 'true')
conf.set('spark.jars', '/Users/yash/Desktop/minio_project/libs/*')
conf.set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.260')
conf.set('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')

# Read CSV from MinIO
df = spark.read.format("csv") \
    .option("header", "true") \
    .load("s3a://uberstorage/raw/uber.csv")


df.show()


# from pyspark.sql import SparkSession

# # Initialize Spark session with required package (optional, see note)
# spark = SparkSession.builder \
#     .appName("CSV Reader") \
#     .getOrCreate()

# # Set MinIO / S3a config
# hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
# hadoop_conf.set("fs.s3a.access.key", "admin")
# hadoop_conf.set("fs.s3a.secret.key", "password123")
# hadoop_conf.set("fs.s3a.endpoint", "http://localhost:9000")
# hadoop_conf.set("fs.s3a.path.style.access", "true")
# hadoop_conf.set("fs.s3a.connection.ssl.enabled", "false")
# hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# # Read CSV from MinIO
# df = spark.read \
#     .format("csv") \
#     .option("header", "true") \
#     .load("s3a://uberstorage/raw/uber.csv")

# df.show()


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CSV Reader") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
    .getOrCreate()

hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "admin")
hadoop_conf.set("fs.s3a.secret.key", "123456789")
hadoop_conf.set("fs.s3a.endpoint", "http://localhost:9000")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .load("s3a://uberstorage/raw/uber.csv")

df.show(5)