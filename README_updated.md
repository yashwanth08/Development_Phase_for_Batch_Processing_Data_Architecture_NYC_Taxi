## INTRO
 Architect `batchstream` data processing systems from [nyc-tlc-trip-records-data](httpswww1.nyc.govsitetlcabouttlc-trip-record-data.page), via the ETL `batch process`  
E (extract  tlc-trip-record-data.page - S3 ) - T (transform  S3 - Spark) - L (load  Spark - Mysql) & `stream process`  Event - Event digest - Event storage. The system then can support calculation such as `Top Driver By area`, `Order by time windiw`, `latest-top-driver`, and `Top busy areas`.

 Batch data  [nyc-tlc-trip-records-data](httpswww1.nyc.govsitetlcabouttlc-trip-record-data.page)

 Tech  Spark, Hadoop, Hive, EMR, S3, MySQL, Kinesis, DynamoDB , Scala, Python, ELK, Kafka
 Batch pipeline  [DataLoad](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_TaxitreemastersrcmainscalaDataLoad) - [DataTransform](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_TaxitreemastersrcmainscalaDataTransform) - [CreateView](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_TaxitreemastersrcmainscalaCreateView) - [SaveToDB](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_TaxitreemastersrcmainscalaSaveToDB) - [SaveToHive](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_TaxitreemastersrcmainscalaSaveToHive)
	 Download batch data  [download_sample_data.sh](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterscriptdownload_sample_data.sh)
	 Batch data  [transactional-data](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterdatastagingtransactional-data), [reference-data](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterdatastagingreference-data) - [processed-data](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterdataprocessed) - [output-transactions](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterdataoutputtransactions) - [output-materializedview](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterdataoutputmaterializedview)

## Architecture 
img src =httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterdocpicbatch_architecture_V3.svg width=800 height=400
img src =httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterdocpicstream_architecture_V3.svg width=800 height=400

- Architecture idea (Batch)
- Architecture idea (Stream)

## File structure 
```
├── Dockerfile     Scala spark Dockerfile
├── build.sbt      Scala sbt build file
├── config         configuration files for DBKafkaAWS..
├── data           Rawprocessedoutput data (batchstream)
├── doc            All repo referencedocpic
├── elk            ELK (Elasticsearch, Logstash, Kibana) configscripts 
├── fluentd        Fluentd help scripts
├── kafka          Kafka help scripts
├── pyspark        Legacy pipeline code (Python)
├── requirements.txt
├── script         Help scripts (envservices) 
├── src            Batchstream process scripts (Scala)
└── utility        Help scripts (pipeline)
```

## Prerequisites
details
summaryPrerequisitessummary

- Install (batch)  
	- Spark 2.4.3
	- Java 1.8.0_11 (java 8)
	- Scala 2.11.12
	- sbt 1.3.5
	- Mysql
	- Hive (optional)
	- Hadoop (optional)
	- Python 3  (optional)
	- Pyspark (optional)

- Set up 
	- Run on local
		- na
	- Run on cloud 
		- AWS account and get `key_pair` for access below services
			- EMR
			- EC2
			- S3
			- DYNAMODB
			- Kinesis
- Config
	- update [config](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterconfig) with your creds  
	- update [elk-config](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxitreemasterelk) with your use cases

details

## Quick start 
details
summaryQuick-Start-Batch-Pipeline-Manuallysummary

```bash 
# STEP 1) Download the dataset
bash scriptdownload_sample_data.sh

# STEP 2) sbt build
sbt compile
sbt assembly

# STEP 3) Load data 
spark-submit 
 --class DataLoad.LoadReferenceData 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

spark-submit 
 --class DataLoad.LoadGreenTripData 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

spark-submit 
 --class DataLoad.LoadYellowTripData 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

# STEP 4) Transform data 
spark-submit 
 --class DataTransform.TransformGreenTaxiData 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

spark-submit 
 --class DataTransform.TransformYellowTaxiData 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

# STEP 5) Create view 
spark-submit 
 --class CreateView.CreateMaterializedView 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

# STEP 6) Save to JDBC (mysql)
spark-submit 
 --class SaveToDB.JDBCToMysql 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

# STEP 7) Save to Hive
spark-submit 
 --class SaveToHive.SaveMaterializedviewToHive 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

```
-------------

# STEP 6) Spark process kafka stream
spark-submit 
 --class KafkaEventLoad.LoadTaxiKafkaEventWriteToKafka 
 targetscala-2.11nyc_taxi_pipeline_2.11-1.0.jar

# STEP 7) Run elsacsearch, kibana, logstach
# make sure curl localhost44444 can get the taxi event
cd ~ 
kibana-7.6.1-darwin-x86_64binkibana
elasticsearch-7.6.1binelasticsearch
logstash-7.6.1binlogstash -f Users$USERNYC_Taxi_Pipelineelklogstashlogstash_taxi_event_file.conf

# test insert toy data to logstash 
# (logstash config elklogstash.conf)
#nc 127.0.0.1 5000  dataevent_sample.json

# then visit kibana UI  localhost5601
# then visit management - index_patterns - Create index pattern 
# create new index  logstash- (not select timestamp as filter)
# then visit the discover tag and check the data

```
details

### Dependency 
details
summaryDependencysummary

1. Spark 2.4.3 
2. Java 8
3. Apache Hadoop 2.7
4. Jars 
	- [aws-java-sdk-1.7.4](httpsmvnrepository.comartifactcom.amazonawsaws-java-sdk1.7.4)
	- [hadoop-aws-2.7.6](httpsmvnrepository.comartifactorg.apache.hadoophadoop-aws2.7.6)
	- [spark-streaming-kafka-0-8-assembly_2.11-2.4.3.jar](httpsmvnrepository.comartifactorg.apache.sparkspark-streaming-kafka-0-8-assembly_2.112.4.3)
	- [mysql-connector-java-8.0.15.jar](httpsmvnrepository.comartifactmysqlmysql-connector-java8.0.15)

5. [build.sbt](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterbuild.sbt)

details

### Ref
details
summaryRefsummary

- [ref.md](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterdocref.md) - dataset link ref, code ref, other ref
- [doc](httpsgithub.comyashwanth08Development_Phase_for_Batch_Processing_Data_Architecture_NYC_Taxiblobmasterdoc) - All ref docs


details

### TODO 
details
summaryTODOsummary

```
# 1. Tune the main pipeline for large scale data (to process whole nyc-tlc-trip data)
# 2. Add front-end UI (flask to visualize supply & demand and surging price)
# 3. Add test 
# 4. Dockerize the project 
# 5. Tune the spark batchstream code 
# 6. Tune the kafka, zoopkeeper cluster setting 
```
details
