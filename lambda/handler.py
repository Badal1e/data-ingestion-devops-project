import boto3
import csv
from validation.validate_data import validate_row
from db.db_writer import insert_records

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if not key.startswith("raw/"):
            return

        response = s3.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(lines)

        valid, invalid = [], []

        for row in reader:
            if validate_row(row):
                valid.append(row)
            else:
                invalid.append(row)

        upload_csv(bucket, "processed/processed.csv", valid)
        upload_csv(bucket, "error/error.csv", invalid)

        insert_records(valid)

def upload_csv(bucket, key, rows):
    if not rows:
        return
    csv_data = ",".join(rows[0].keys()) + "\n"
    for r in rows:
        csv_data += ",".join(r.values()) + "\n"
    s3.put_object(Bucket=bucket, Key=key, Body=csv_data)
