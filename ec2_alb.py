import boto3

def register_instances_with_alb(alb_arn, instance_ids):
    elbv2_client = boto3.client('elbv2')

    try:
        # Register EC2 instances with ALB
        elbv2_client.register_targets(
            TargetGroupArn=alb_arn,  # Replace with your ALB ARN
            Targets=[{'Id': instance_id} for instance_id in instance_ids]
        )

        print(f"EC2 instances {instance_ids} registered with ALB successfully.")
    except Exception as e:
        print(f"Error registering instances with ALB: {e}")
