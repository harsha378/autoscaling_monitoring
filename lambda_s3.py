import boto3

def create_lambda_function(lambda_function_name, s3_bucket_name, sns_topic_arn):
    lambda_client = boto3.client('lambda')

    try:
        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime='python3.8',
            Role='your-lambda-execution-role-arn',  # Replace with your Lambda execution role ARN
            Handler='lambda_function.handler',
            Code={
                'S3Bucket': 'your-lambda-code-bucket',  # Replace with your Lambda code bucket
                'S3Key': 'lambda_function.zip',  # Replace with your Lambda code ZIP file
            },
            Environment={
                'Variables': {
                    'S3_BUCKET': s3_bucket_name,
                    'SNS_TOPIC_ARN': sns_topic_arn,
                },
            },
            Timeout=30,
        )

        print(f"Lambda function '{lambda_function_name}' created successfully.")
    except Exception as e:
        print(f"Error creating Lambda function: {e}")
