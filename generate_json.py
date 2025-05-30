import boto3
import json
import os

def main():
    bucket_name = os.environ['S3_BUCKET']
    region = os.environ.get('AWS_REGION', 'us-east-1')

    s3 = boto3.client('s3', region_name=region)

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = []

        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{key}"
                files.append({'key': key, 'url': url})

        # Save JSON locally
        with open('images.json', 'w') as f:
            json.dump(files, f, indent=2)

        print(f"Found {len(files)} files in bucket {bucket_name}")

    except Exception as e:
        print("Error listing objects from S3:", e)
        exit(1)

if __name__ == "__main__":
    main()
