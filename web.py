
import boto3

def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3')

    try:
        response = s3_client.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' created successfully.")
        return response['Location']
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")
        return None

bucket_name = 'harsha'
s3_bucket_location = create_s3_bucket(bucket_name)
