import boto3

def configure_alb_logging(alb_arn, s3_bucket_name):
    elbv2_client = boto3.client('elbv2')

    try:
        response = elbv2_client.modify_load_balancer_attributes(
            LoadBalancerArn=alb_arn,
            Attributes=[
                {
                    'Key': 'access_logs.s3.enabled',
                    'Value': 'true',
                },
                {
                    'Key': 'access_logs.s3.bucket',
                    'Value': s3_bucket_name,
                },
            ]
        )

        print(f"ALB logging configured successfully.")
    except Exception as e:
        print(f"Error configuring ALB logging: {e}")

# Example Usage
alb_arn = 'your-alb-arn'
s3_bucket_name = 'your-s3-bucket-name'

configure_alb_logging(alb_arn, s3_bucket_name)
