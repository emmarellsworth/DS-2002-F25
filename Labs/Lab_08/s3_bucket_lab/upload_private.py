import boto3

s3 = boto3.client('s3', region_name="us-east-1")

bucket = "ds2002-f25-gbp4bh"
local_file = "puppy.webp"
key = "puppy.webp"

with open(local_file, "rb") as f:
    s3.put_object(Bucket=bucket, Key=key, Body=f)
