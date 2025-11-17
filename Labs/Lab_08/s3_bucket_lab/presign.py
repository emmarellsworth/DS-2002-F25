import boto3

s3 = boto3.client('s3', region_name="us-east-1")

bucket = "ds2002-f25-gbp4bh"
key = "puppy.webp"
expire = 604800  # 7 days

url = s3.generate_presigned_url(
    ClientMethod="get_object",
    Params={"Bucket": bucket, "Key": key},
    ExpiresIn=expire,
)

print(url)
