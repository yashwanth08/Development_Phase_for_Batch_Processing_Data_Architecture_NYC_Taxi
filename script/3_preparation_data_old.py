# preparation_data.py

import os
from io import BytesIO
import pandas as pd
from minio import Minio

# Configuration
file_path = "data/NYC TLC Trip Record.csv"
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password123",
    secure=False
)

# Step 1: Merge main parquet table
merged_data_df = pd.read_csv(file_path)
print(merged_data_df.shape)
print("Merge successfully")

# Step 2: Merge with taxi Zone lookup
taxi_lookup_path = "output_data/taxi_lookup.csv"
df_lookup = pd.read_csv(taxi_lookup_path)



# Merge for pickup locations
merged_data_df = merged_data_df.merge(df_lookup, left_on="PULocationID", right_on="LocationID")



merged_data_df = merged_data_df.drop(columns=['PULocationID', 'LocationID', 'Borough', 'service_zone', 'Zone'])
merged_data_df = merged_data_df.rename(columns={'longitude': 'pickup_longitude', 'latitude': 'pickup_latitude'})

# Merge for dropoff locations
merged_data_df = merged_data_df.merge(df_lookup, left_on="DOLocationID", right_on="LocationID")


merged_data_df = merged_data_df.drop(columns=['DOLocationID', 'LocationID', 'Borough', 'service_zone', 'Zone'])
merged_data_df = merged_data_df.rename(columns={'longitude': 'dropoff_longitude', 'latitude': 'dropoff_latitude'})



# Drop rows with missing values
merged_data_df = merged_data_df.drop(columns=['Unnamed: 0_x','Unnamed: 0_y', 'ehail_fee']).dropna()

from io import BytesIO

# Step 3: Convert to CSV
csv_buffer = BytesIO()
merged_data_df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)
buffer_length = csv_buffer.getbuffer().nbytes
print('Converted to CSV successfully')

# Step 4: Create storage in Minio
raw_bucket_name = "uberstorage"
if not client.bucket_exists(raw_bucket_name):
    client.make_bucket(raw_bucket_name)
    print(f"Bucket {raw_bucket_name} created successfully.")

# Upload the CSV file to Minio
client.put_object(
    bucket_name=raw_bucket_name,
    object_name='raw/uber.csv',
    data=csv_buffer,
    length=buffer_length,
    content_type='text/csv'
)
print("CSV file loaded into storage successfully")
print("Load into storage successfully")

# Step 5: Create Delta Lake bucket in Minio
delta_bucket_name = "delta-uber"
if not client.bucket_exists(delta_bucket_name):
    client.make_bucket(delta_bucket_name)
    print(f"Bucket {delta_bucket_name} created successfully.")