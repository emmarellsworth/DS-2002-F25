import requests
import boto3

# 1. Fetch and save a file from the internet
file_url = "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif"
local_file = "cat.gif"

response = requests.get(file_url)
response.raise_for_status()  # will throw an error if download fails

with open(local_file, "wb") as f:
    f.write(response.content)

# 2. Upload the file to S3
s3 = boto3.client("s3", region_name="us-east-1")

bucket_name = "ds2002-f25-gbp4bh"
object_name = "cat.gif"   # same name in S3

with open(local_file, "rb") as f:
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=f)

# 3. Presign the file with an expiration time (7 days = 604800 seconds)
expires_in = 604800

url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": bucket_name, "Key": object_name},
    ExpiresIn=expires_in,
)

# 4. Output the presigned URL
print(url)
