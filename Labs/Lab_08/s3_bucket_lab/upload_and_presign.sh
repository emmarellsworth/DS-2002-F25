#!/bin/bash

# Script usage:
# ./upload_and_presign.sh <local_file> <bucket_name> <expiration_seconds>

# Positional arguments
LOCAL_FILE=$1
BUCKET=$2
EXPIRE=$3

# Check positional arguments
if [ -z "$LOCAL_FILE" ] || [ -z "$BUCKET" ] || [ -z "$EXPIRE" ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    exit 1
fi

echo "Uploading $LOCAL_FILE to s3://$BUCKET/ ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/"

echo "Generating presigned URL (expires in $EXPIRE seconds) ..."
URL=$(aws s3 presign --expires-in "$EXPIRE" "s3://$BUCKET/$(basename 
$LOCAL_FILE)")

echo "Presigned URL:"
echo "$URL"
