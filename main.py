import sys
import os
import json

# Add 'src' directory to the module search path
sys.path.insert(0, os.path.abspath('src'))

try:
    from data_preparation import process_lender_offer_dataset 
except ImportError as e:
    raise ImportError(f"Failed to import a module: {e}")

# Define data file path
data_file_path = 'data/raw/lender_offers.json'
output_file_path = 'data/processed/processed_lender_offers.csv'

# Check if the data file exists
if not os.path.exists(data_file_path):
    raise FileNotFoundError(f"Data file not found: {data_file_path}")

import os
from dotenv import load_dotenv
import boto3

load_dotenv()  # Load from .env

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

s3 = session.client('s3')

bucket_name = "crm-ai-ml-mongo-prod"
prefix = "mongodb-backup-prod/"

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

import re
from datetime import datetime

json_files = []
pattern = re.compile(r"lender_offers-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json$")

for obj in response.get("Contents", []):
    key = obj["Key"]
    match = pattern.search(key)
    if match:
        dt_str = match.group(1)
        dt = datetime.strptime(dt_str, "%Y-%m-%d_%H-%M-%S")
        json_files.append((dt, key))

if json_files:
    latest_json = max(json_files, key=lambda x: x[0])[1]
    print(f"Latest JSON file: {latest_json}")
    # Download the latest JSON file from S3
    s3.download_file(bucket_name, latest_json, data_file_path)
    print(f"Downloaded {latest_json} to {data_file_path}")
else:
    print("No lender_offers JSON files found.")

process_lender_offer_dataset(data_file_path, output_file_path)

print(f"Dataset saved to {output_file_path}")