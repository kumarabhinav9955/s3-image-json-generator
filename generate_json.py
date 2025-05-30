import boto3
import os
import json
import sys

def main():
    region = os.getenv('AWS_REGION')
    bucket = os.getenv('S3_BUCKET')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not all([region, bucket, access_key, secret_key]):
        print("Error: Missing one or more AWS environment variables.", file=sys.stderr)
        sys.exit(1)

    s3 = boto3.client(
        's3',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    try:
        response = s3.list_objects_v2(Bucket=bucket)
        contents = response.get('Contents', [])

        files = []
        for obj in contents:
            key = obj['Key']
            url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
            files.append({"key": key, "url": url})

        with open("images.json", "w") as f:
            json.dump(files, f, indent=2)

        print(f"Successfully generated images.json with {len(files)} items.")

    except Exception as e:
        print(f"Error listing objects from S3: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
