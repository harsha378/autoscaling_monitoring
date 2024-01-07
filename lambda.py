import boto3

def lambda_handler(event, context):
    # Replace with your ALB ARN, target group name, and SNS topic ARN
    alb_arn = 'your-alb-arn'
    target_group_name = 'your-target-group-name'
    sns_topic_arn = 'your-sns-topic-arn'

    elbv2_client = boto3.client('elbv2')
    autoscaling_client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    # Perform health check by querying the ALB
    health_check_response = elbv2_client.describe_target_health(
        TargetGroupArn=alb_arn,
    )

    unhealthy_targets = [target['Target']['Id'] for target in health_check_response['TargetHealthDescriptions']
                         if target['TargetHealth']['State'] != 'healthy']

    # Check if health check consistently fails for any targets
    if unhealthy_targets:
        print(f"Unhealthy targets: {unhealthy_targets}")

        # Capture a snapshot of the failing instance
        for instance_id in unhealthy_targets:
            snapshot_response = ec2_client.create_snapshot(
                VolumeId=get_volume_id_from_instance_id(instance_id),
                Description=f"Health check failed for instance {instance_id}"
            )
            snapshot_id = snapshot_response['SnapshotId']
            print(f"Snapshot created for instance {instance_id}: {snapshot_id}")

            # Terminate the failing instance
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} terminated.")

            # Send notification through SNS to administrators
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject="Web Application Health Check Failure",
                Message=f"The web application health check failed for instance {instance_id}. "
                        f"Snapshot ID: {snapshot_id}. Instance terminated.",
            )

# Helper function to get volume ID from EC2 instance ID
def get_volume_id_from_instance_id(instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    volume_id = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    return volume_id
